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
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from tracker.monitor import get_monitor
from tracker.db import init_db


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print("\n⏹️ Shutting down WorkShot...")
    monitor = get_monitor()
    monitor.stop()
    sys.exit(0)


def start_dashboard_server(host: str = "127.0.0.1", port: int = 8787):
    """Start the FastAPI dashboard server in a thread."""
    import uvicorn
    from dashboard.app import app
    
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
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     ⚡ W O R K S H O T ⚡                                  ║
    ║                                                           ║
    ║     Activity Tracker & Time Analytics Dashboard           ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point."""
    print_banner()
    
    # Parse args
    open_browser = "--no-browser" not in sys.argv
    host = "127.0.0.1"
    port = 8787
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize database
    print("📦 Initializing database...")
    init_db()
    
    # Start activity monitor
    print("🔍 Starting activity monitor...")
    monitor = get_monitor()
    monitor.start()
    
    # Start dashboard server in background thread
    print(f"🌐 Starting dashboard server at http://{host}:{port}")
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
        print("🚀 Opening dashboard in browser...")
        webbrowser.open(f"http://{host}:{port}")
    
    print("\n✅ WorkShot is running!")
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



