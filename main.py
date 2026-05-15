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
from upload import upload_file


# Constants
APP_START_TIME: Optional[datetime] = None
LOCK_FILE = Path(__file__).parent / "workshot.pid"
DAILIES_FILE = Path(__file__).parent / "logs" / "dailies.md"

def manage_single_instance():
    """Ensure mutual exclusion using a PID lock file."""
    if LOCK_FILE.exists():
        try:
            old_pid = int(LOCK_FILE.read_text().strip())
            if psutil.pid_exists(old_pid):
                print(f"[*] Stopping previous instance (PID: {old_pid})...")
                proc = psutil.Process(old_pid)
                proc.terminate()
                # Wait for process to actually exit to release DB locks
                try:
                    proc.wait(timeout=5)
                except psutil.TimeoutExpired:
                    proc.kill()
                time.sleep(1)
        except (ValueError, psutil.NoSuchProcess, psutil.AccessDenied):
            # If PID is invalid or we can't touch it, just move on
            pass
    
    LOCK_FILE.parent.mkdir(exist_ok=True)
    LOCK_FILE.write_text(str(os.getpid()))

def record_daily_note(status, message):
    """
    Records a task status to a monthly dailies markdown file. 
    Ensures only one entry per task per day (Idempotent).
    """
    os.makedirs("logs", exist_ok=True)
    
    now = datetime.now()
    
    # Format the Month for the filename (e.g., "2026_05")
    month_str = now.strftime("%Y_%m")
    log_path = f"logs/dailies_{month_str}.md"
    
    # Format the Day for the Header
    today_str = now.strftime("%Y-%m-%d")
    header = f"# {today_str}"
    
    # Format the entry with a markdown bullet for clean rendering
    entry = f"- [{status}] {message}"
    
    lines = []
    # added encoding="utf-8" to prevent Windows character mapping errors
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    # Find the section for today
    today_index = -1
    for i, line in enumerate(lines):
        if line.strip() == header:
            today_index = i
            break

    if today_index == -1:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n{header}\n{entry}\n")
    else:
        # Check if this task is already in today's section.
        task_found_at = -1
        end_of_section = len(lines)
        
        for i in range(today_index + 1, len(lines)):
            if lines[i].startswith("#"):
                end_of_section = i
                break
            if message in lines[i]:
                task_found_at = i
                break
        
        if task_found_at != -1:
            lines[task_found_at] = f"{entry}\n"
        else:
            lines.insert(today_index + 1, f"{entry}\n")

        with open(log_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    print(f"[DAILIES] Logged {status} to {log_path}")

def signal_handler(signum, frame):
    """Graceful shutdown sequence."""
    global APP_START_TIME
    print("\n[*] Shutting down WorkShot...")
    
    monitor = get_monitor()
    monitor.stop()
    
    # Auto-export today's data if running > 5 hours
    if APP_START_TIME:
        runtime_seconds = (datetime.now() - APP_START_TIME).total_seconds()
        if runtime_seconds > 18000:  # 5 hours = 18000 seconds
            try:
                print("[*] Auto-exporting today's data...")
                today = datetime.now().strftime("%Y-%m-%d")
                filepath = export_html(start_date=today, end_date=today)
                print(f"[+] Report saved: {filepath}")
                
                try:
                    print("[*] Uploading to Google Drive...")
                    upload_file(str(filepath))
                except Exception as e:
                    print(f"[!] Upload failed: {e}")
            except Exception as e:
                print(f"[!] Auto-export failed: {e}")
    
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    
    sys.exit(0)


def start_dashboard_server(host: str, port: int):
    """Runs the FastAPI app via Uvicorn."""
    import uvicorn
    from dashboard.app import app
    
    if sys.platform == "win32":
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.set_exception_handler(suppress_asyncio_errors)
        except Exception: pass
    
    config = uvicorn.Config(app, host=host, port=port, log_level="warning", access_log=False)
    uvicorn.Server(config).run()

def suppress_asyncio_errors(loop, context):
    """Mute harmless shutdown noise."""
    exception = context.get("exception")
    if isinstance(exception, (ConnectionResetError, ConnectionAbortedError)):
        return
    loop.default_exception_handler(context)

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

def main():
    global APP_START_TIME
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="asyncio")
    
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # Show Workshot banner
    print_banner()

    manage_single_instance()
    APP_START_TIME = datetime.now()
    
    # Config
    open_browser = "--no-browser" not in sys.argv
    host, port = "127.0.0.1", 8787
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    init_db()
    
    # Start Monitor
    monitor = get_monitor()
    monitor.start()
    
    # Start Dashboard
    threading.Thread(target=start_dashboard_server, args=(host, port), daemon=True).start()
    
    time.sleep(1.5)
    if open_browser:
        webbrowser.open(f"http://{host}:{port}")
    
    print(f"\n[+] WorkShot Running\n    Dashboard: http://{host}:{port}\n    Dailies: {DAILIES_FILE}\n")
    
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()



