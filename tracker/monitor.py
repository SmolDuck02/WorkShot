"""Core activity monitoring logic using Windows APIs."""

import time
import threading
import ctypes
from datetime import datetime
from typing import Optional, Callable
from dataclasses import dataclass, field

import win32gui
import win32process
import win32api
import win32con
import psutil
from screeninfo import get_monitors

from . import db
from .utils import sanitize_app_name


# Windows API structure for idle detection
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_uint),
        ('dwTime', ctypes.c_uint),
    ]


def get_idle_duration() -> float:
    """Get the number of seconds since the last user input (keyboard/mouse)."""
    try:
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        
        # GetTickCount returns milliseconds since system start
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    except Exception:
        return 0.0


@dataclass
class ActivityState:
    """Current activity state."""
    app_name: str
    window_title: str
    monitor: int
    session_id: Optional[int] = None
    start_time: Optional[datetime] = None
    is_idle: bool = False
    
    def matches(self, other: 'ActivityState') -> bool:
        """Check if this state matches another (same app, title, monitor)."""
        return (
            self.app_name == other.app_name and
            self.window_title == other.window_title and
            self.monitor == other.monitor and
            self.is_idle == other.is_idle
        )


class ActivityMonitor:
    """Monitors active window and tracks time spent."""
    
    # Idle threshold in seconds (user is considered idle after this much inactivity)
    IDLE_THRESHOLD = 60.0
    
    def __init__(self, poll_interval: float = 1.0):
        self.poll_interval = poll_interval
        self.current_state: Optional[ActivityState] = None
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._listeners: list[Callable] = []
        self._monitors_info = self._get_monitors_info()
        self._is_idle = False
        self._idle_start_time: Optional[datetime] = None
        self._pre_idle_state: Optional[ActivityState] = None  # State before going idle
    
    def _get_monitors_info(self) -> list[dict]:
        """Get information about connected monitors."""
        monitors = []
        try:
            for i, m in enumerate(get_monitors(), 1):
                monitors.append({
                    'id': i,
                    'x': m.x,
                    'y': m.y,
                    'width': m.width,
                    'height': m.height,
                    'x_end': m.x + m.width,
                    'y_end': m.y + m.height,
                    'is_primary': m.is_primary
                })
        except Exception:
            # Fallback to single monitor
            monitors = [{
                'id': 1,
                'x': 0,
                'y': 0,
                'width': 1920,
                'height': 1080,
                'x_end': 1920,
                'y_end': 1080,
                'is_primary': True
            }]
        return monitors
    
    def _get_window_monitor(self, hwnd: int) -> int:
        """Determine which monitor a window is on based on its position."""
        try:
            rect = win32gui.GetWindowRect(hwnd)
            # Get center point of window
            center_x = (rect[0] + rect[2]) // 2
            center_y = (rect[1] + rect[3]) // 2
            
            for monitor in self._monitors_info:
                if (monitor['x'] <= center_x < monitor['x_end'] and
                    monitor['y'] <= center_y < monitor['y_end']):
                    return monitor['id']
            
            # Default to monitor 1 if not found
            return 1
        except Exception:
            return 1
    
    def _get_active_window_info(self) -> Optional[ActivityState]:
        """Get information about the currently active window."""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None
            
            # Get window title
            window_title = win32gui.GetWindowText(hwnd)
            if not window_title:
                window_title = "(No Title)"
            
            # Get process name
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                app_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                app_name = "Unknown"
            
            # Get monitor
            monitor = self._get_window_monitor(hwnd)
            
            return ActivityState(
                app_name=app_name,
                window_title=window_title,
                monitor=monitor
            )
        except Exception as e:
            print(f"Error getting window info: {e}")
            return None
    
    def add_listener(self, callback: Callable[[ActivityState, int], None]):
        """Add a listener for activity updates. Callback receives (state, elapsed_seconds)."""
        self._listeners.append(callback)
    
    def remove_listener(self, callback: Callable):
        """Remove a listener."""
        if callback in self._listeners:
            self._listeners.remove(callback)
    
    def _notify_listeners(self, state: ActivityState, elapsed: int, is_idle: bool = False):
        """Notify all listeners of state update."""
        for listener in self._listeners:
            try:
                listener(state, elapsed, is_idle)
            except Exception as e:
                print(f"Listener error: {e}")
    
    def _monitoring_loop(self):
        """Main monitoring loop with idle detection."""
        while self.running:
            idle_seconds = get_idle_duration()
            
            # Check if user is idle
            if idle_seconds >= self.IDLE_THRESHOLD:
                if not self._is_idle:
                    # Just became idle - transition to idle state
                    self._is_idle = True
                    self._idle_start_time = datetime.now()
                    
                    # Save current state before going idle
                    if self.current_state and not self.current_state.is_idle:
                        self._pre_idle_state = self.current_state
                        # End current active session
                        if self.current_state.session_id:
                            db.end_session(self.current_state.session_id)
                    
                    # Start idle session
                    idle_state = ActivityState(
                        app_name="Idle",
                        window_title="User is idle",
                        monitor=0,
                        is_idle=True
                    )
                    session_id = db.start_session(
                        idle_state.app_name,
                        idle_state.window_title,
                        idle_state.monitor,
                        is_idle=True
                    )
                    idle_state.session_id = session_id
                    idle_state.start_time = self._idle_start_time
                    self.current_state = idle_state
                
                # Notify listeners about idle state
                elapsed = 0
                if self._idle_start_time:
                    elapsed = int((datetime.now() - self._idle_start_time).total_seconds())
                self._notify_listeners(self.current_state, elapsed, is_idle=True)
            
            else:
                # User is active
                if self._is_idle:
                    # Just came back from idle - end idle session
                    self._is_idle = False
                    if self.current_state and self.current_state.session_id:
                        db.end_session(self.current_state.session_id)
                    self.current_state = None
                    self._idle_start_time = None
                
                # Normal activity tracking
                new_state = self._get_active_window_info()
                
                if new_state:
                    if self.current_state is None or not self.current_state.matches(new_state):
                        # Activity changed - end old session, start new one
                        if self.current_state and self.current_state.session_id:
                            db.end_session(self.current_state.session_id)
                        
                        # Start new session
                        session_id = db.start_session(
                            new_state.app_name,
                            new_state.window_title,
                            new_state.monitor,
                            is_idle=False
                        )
                        new_state.session_id = session_id
                        new_state.start_time = datetime.now()
                        self.current_state = new_state
                    
                    # Calculate elapsed time for current session
                    elapsed = 0
                    if self.current_state.start_time:
                        elapsed = int((datetime.now() - self.current_state.start_time).total_seconds())
                    
                    # Notify listeners
                    self._notify_listeners(self.current_state, elapsed)
            
            time.sleep(self.poll_interval)
    
    def start(self):
        """Start monitoring."""
        if self.running:
            return
        
        # Initialize database
        db.init_db()
        
        self.running = True
        self._thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._thread.start()
        print("🔍 Activity monitoring started...")
    
    def stop(self):
        """Stop monitoring."""
        self.running = False
        
        # End current session
        if self.current_state and self.current_state.session_id:
            db.end_session(self.current_state.session_id)
        
        if self._thread:
            self._thread.join(timeout=2.0)
        
        print("⏹️ Activity monitoring stopped.")
    
    def get_current_activity(self) -> Optional[dict]:
        """Get current activity as dictionary."""
        if not self.current_state:
            return {'status': 'idle', 'is_idle': False}
        
        elapsed = 0
        if self.current_state.start_time:
            elapsed = int((datetime.now() - self.current_state.start_time).total_seconds())
        
        result = {
            'app_name': self.current_state.app_name,
            'app_display': sanitize_app_name(self.current_state.app_name),
            'window_title': self.current_state.window_title,
            'monitor': self.current_state.monitor,
            'elapsed_seconds': elapsed,
            'start_time': self.current_state.start_time.isoformat() if self.current_state.start_time else None,
            'is_idle': self.current_state.is_idle
        }
        
        if self.current_state.is_idle:
            result['status'] = 'idle'
            result['idle_duration_formatted'] = self._format_duration(elapsed)
        
        return result
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration for display."""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m {seconds % 60}s"
        else:
            h = seconds // 3600
            m = (seconds % 3600) // 60
            return f"{h}h {m}m"


# Global monitor instance
_monitor: Optional[ActivityMonitor] = None


def get_monitor() -> ActivityMonitor:
    """Get or create the global monitor instance."""
    global _monitor
    if _monitor is None:
        _monitor = ActivityMonitor()
    return _monitor



