"""
WorkShot - Activity Tracker & Dashboard
=======================================
Main entry point that starts the activity monitor and dashboard server.

Usage:
    python main.py              # Start both tracker and dashboard
    python main.py --no-browser # Start without opening browser
"""

import sys
import time
import signal
import threading
import webbrowser
import os
import psutil
import warnings
import asyncio
from datetime import datetime
from typing import Optional
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from tracker.monitor import get_monitor
from tracker.db import init_db
from tracker.export import export_html


# Global variable to track app start time
app_start_time: Optional[datetime] = None


def check_and_stop_previous_instances():
    """Check for and stop any previous WorkShot instances."""
    current_pid = os.getpid()
    script_dir = Path(__file__).resolve().parent
    stopped_count = 0
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
            try:
                # Skip current process
                if proc.info['pid'] == current_pid:
                    continue
                
                # Check if it's a Python process running main.py
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    cwd = proc.info.get('cwd', '')
                    
                    # Check if it's running main.py
                    if cmdline and any('main.py' in str(arg) for arg in cmdline):
                        # Check if it's THIS main.py (WorkShot) by checking:
                        # 1. Working directory matches our script directory
                        # 2. Or full path to our main.py in cmdline
                        is_workshot = (
                            (cwd and str(script_dir) in str(cwd)) or
                            any(str(script_dir) in str(arg) for arg in cmdline)
                        )
                        
                        if is_workshot:
                            print(f"[*] Stopping previous instance (PID: {proc.info['pid']})...")
                            try:
                                process = psutil.Process(proc.info['pid'])
                                process.terminate()  # Try graceful termination first
                                process.wait(timeout=3)  # Wait up to 3 seconds
                            except psutil.TimeoutExpired:
                                process.kill()  # Force kill if graceful fails
                            stopped_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        # If checking fails, just continue - better to allow startup than block it
        print(f"[!] Warning: Could not check for previous instances: {e}")
    
    if stopped_count > 0:
        print(f"[+] Stopped {stopped_count} previous instance(s)")
        time.sleep(1)  # Brief pause to ensure clean shutdown


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print("\n[*] Shutting down WorkShot...")
    monitor = get_monitor()
    monitor.stop()
    
    # Auto-export today's data if running > 5 hours
    if app_start_time:
        runtime_seconds = (datetime.now() - app_start_time).total_seconds()
        if runtime_seconds > 18000:  # 5 hours = 18000 seconds
            try:
                print("[*] Auto-exporting today's data...")
                today = datetime.now().strftime("%Y-%m-%d")
                filepath = export_html(start_date=today, end_date=today)
                print(f"[+] Report saved: {filepath}")
            except Exception as e:
                print(f"[!] Auto-export failed: {e}")
    
    # Give server thread a brief moment to clean up
    time.sleep(0.3)
    sys.exit(0)


def start_dashboard_server(host: str = "127.0.0.1", port: int = 8787):
    """Start the FastAPI dashboard server in a thread."""
    import uvicorn
    from dashboard.app import app
    
    # Set exception handler for this thread's event loop
    if sys.platform == "win32":
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.set_exception_handler(suppress_asyncio_errors)
        except Exception:
            pass
    
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level="warning",  # Reduce noise
        access_log=False
    )
    server = uvicorn.Server(config)
    server.run()


def print_banner():
    """Print startup banner."""
    banner = """
    ===================================================
                   W O R K S H O T
    ===================================================
         Activity Tracker & Time Analytics Dashboard
    ===================================================
    """
    print(banner)


def suppress_asyncio_errors(loop, context):
    """Suppress specific asyncio errors during shutdown."""
    exception = context.get("exception")
    if exception:
        # Suppress ConnectionResetError during shutdown (harmless)
        if isinstance(exception, (ConnectionResetError, ConnectionAbortedError)):
            return
    # For other exceptions, use default handler
    loop.default_exception_handler(context)


def main():
    """Main entry point."""
    global app_start_time
    
    # Suppress annoying asyncio warnings on Windows during shutdown
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="asyncio")
    
    # Suppress specific connection errors during shutdown
    if sys.platform == "win32":
        # Set asyncio event loop policy for Windows
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        # Set custom exception handler to suppress connection errors
        try:
            # Create and set a new event loop for the main thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.set_exception_handler(suppress_asyncio_errors)
        except Exception:
            pass  # If setting up event loop fails, continue anyway
    
    print_banner()
    
    # Check for and stop any previous instances
    check_and_stop_previous_instances()
    
    # Track app start time for auto-export
    app_start_time = datetime.now()
    
    # Parse args
    open_browser = "--no-browser" not in sys.argv
    host = "127.0.0.1"
    port = 8787
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize database
    print("[+] Initializing database...")
    init_db()
    
    # Start activity monitor
    print("[+] Starting activity monitor...")
    monitor = get_monitor()
    monitor.start()
    
    # Start dashboard server in background thread
    print(f"[+] Starting dashboard server at http://{host}:{port}")
    server_thread = threading.Thread(
        target=start_dashboard_server,
        args=(host, port),
        daemon=True
    )
    server_thread.start()
    
    # Wait a moment for server to start
    time.sleep(1.5)
    
    # Open browser
    if open_browser:
        print("[+] Opening dashboard in browser...")
        webbrowser.open(f"http://{host}:{port}")
    
    print("\n[+] WorkShot is running!")
    print("   Dashboard: http://127.0.0.1:8787")
    print("   Press Ctrl+C to stop\n")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()




