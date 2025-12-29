# This is VibeCoded
# ⚡ WorkShot

> **Your Digital Activity Guardian** - A next-generation activity monitoring system with a sleek, futuristic interface that transforms how you track and understand your computer usage.

[![Status](https://img.shields.io/badge/status-active-5b8def?style=for-the-badge)](https://github.com/yourusername/workshot)
[![Python](https://img.shields.io/badge/python-3.10+-5b8def?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/windows-10%2F11-5b8def?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-5b8def?style=for-the-badge)](LICENSE)

<!-- ![WorkShot Dashboard Preview](https://via.placeholder.com/1200x600/0c0c0f/5b8def?text=WorkShot+Dashboard) -->

---

## 🌟 Overview

**WorkShot** is a powerful **local desktop application** for Windows that captures every moment of your digital workflow. With **real-time monitoring**, **multi-monitor support**, and a **stunning sci-fi dashboard**, WorkShot gives you unprecedented insight into how you spend your time.

> 🔒 **Privacy-First Design**: WorkShot runs entirely on your machine. All tracking data stays local - no cloud servers, no data uploads, no subscriptions. Your activity data is yours alone.

Unlike basic time trackers, WorkShot provides:
- 🎯 **Pixel-perfect accuracy** - Tracks down to the second
- 🖥️ **Multi-monitor awareness** - Knows which screen you're working on
- 💤 **Smart idle detection** - Automatically pauses when you're away
- 📊 **Beautiful visualizations** - Data that's actually enjoyable to explore
- 🚀 **Lightning-fast exports** - CSV, JSON, and styled HTML reports
- 🎨 **Mobile-responsive** - Access your data anywhere

---

## ✨ Key Features

### 🔴 Live Activity Monitoring
- **Real-time tracking** of active applications and window titles
- **Live timer** showing current session duration
- **Monitor detection** - Identifies which physical monitor displays each app
- **Instant updates** via Server-Sent Events (SSE)

### 📊 Comprehensive Analytics
- **Today's summary** - Total time, apps used, session count
- **App breakdown** - Visual progress bars showing time per application
- **Monitor usage** - See how time is distributed across your displays
- **Session history** - Detailed log of recent activities

### 💤 Smart Idle Detection
- **Context-aware inactivity** - Detects idle time after 45 seconds of no keyboard/mouse input
- **Intelligent window title analysis** - Checks if you're actually watching/reading (not just having a browser open)
- **Media consumption tracking** - YouTube, Netflix, anime sites, video players count as active usage
- **3-minute grace period** - After watching media, you won't go idle even if you switch windows briefly
- **Reading detection** - PDFs and documents recognized as active time
- **Always-active apps** - Video players (VLC), music (Spotify), and video calls (Zoom, Teams) never trigger idle
- **Separate idle tracking** - True idle time is logged but excluded from productivity stats
- **Smart resume** - Seamlessly continues tracking when you return
- **Example**: Watching anime in browser, then check Discord briefly = still counts as watching (not idle) ✓

### 📤 Flexible Data Export
- **Multiple formats**: CSV (raw data), JSON (structured), HTML (styled reports)
- **Date filtering**: Export specific dates, weeks, months, or custom ranges
- **Auto-export on shutdown**: Automatically saves today's HTML report when stopping (if running > 5 hours)
- **Mobile-friendly reports** - HTML exports adapt to any screen size
- **Fast processing** - Optimized for large datasets

### 🎨 Futuristic Dashboard Design
- **Minimal & clean** aesthetic with high-tech vibes
- **Dark theme** with accent colors (blue/purple palette)
- **Smooth animations** and transitions
- **Responsive layout** - Works on desktop, tablet, and mobile
- **App icons** - Real logos fetched from CDN (100+ apps supported)

### 🔄 Smart Instance Management
- **Auto-restart** - Running WorkShot again automatically stops the previous instance
- **Clean shutdown** - Graceful termination saves all data before exiting
- **No conflicts** - Port and database locking handled automatically
- **Global command** - Run `workshot` from anywhere in your terminal

---

## 🚀 Quick Start

### Prerequisites

- **Windows 10 or 11** (64-bit)
- **Python 3.10+** ([Download here](https://www.python.org/downloads/))

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/workshot.git
cd workshot/WorkShot

# Install dependencies
pip install -r requirements.txt
```

### Running WorkShot

**Option 1: Direct Python**
```bash
python main.py
```

**Option 2: Global Command (Recommended)**

For easy access from anywhere, set up the global `workshot` command:

1. **Edit the launcher script** - Open `workshot.bat` and update the path:
   ```batch
   cd /d "C:\Users\YOUR_USERNAME\WorkShot\WorkShot"
   ```
   Replace `YOUR_USERNAME` with your actual Windows username.

2. **Set up global access** (PowerShell as Administrator):
   ```powershell
   # Create a bin directory for user scripts
   mkdir C:\Users\YOUR_USERNAME\bin
   
   # Copy the launcher script
   copy workshot.bat C:\Users\YOUR_USERNAME\bin\
   
   # Add to PATH (run once)
   [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Users\YOUR_USERNAME\bin", "User")
   ```

3. **Restart your terminal** to apply PATH changes

4. **Run from anywhere**:
   ```bash
   workshot
   ```

**Benefits:**
- ✅ Run from any directory
- ✅ Automatically stops previous instances
- ✅ Clean Ctrl+C shutdown
- ✅ No port conflicts or database locks

The dashboard will automatically open in your default browser at:
**http://127.0.0.1:8787**

### Command-Line Options

```bash
python main.py --no-browser  # Start without opening browser
```

### Stopping WorkShot

Simply press **Ctrl+C** in the terminal to stop tracking and shut down gracefully.

---

## 📸 Screenshots

### Main Dashboard
*Live activity tracking with real-time updates*

### App Breakdown
*Visual representation of time spent per application*

### Export Modal
*Flexible date range selection for data exports*

### Mobile View
*Fully responsive design for on-the-go access*

---

## 🏗️ Project Structure

```
WorkShot/
├── tracker/                  # Core monitoring engine
│   ├── __init__.py
│   ├── monitor.py           # Windows API activity tracking
│   ├── db.py                # SQLite database operations
│   ├── export.py            # Data export (CSV/JSON/HTML)
│   └── utils.py             # Helper utilities
│
├── dashboard/               # Web interface
│   ├── app.py              # FastAPI backend server
│   ├── static/
│   │   ├── style.css       # Futuristic UI styling
│   │   └── script.js       # Live dashboard logic
│   └── templates/
│       └── index.html      # Dashboard HTML template
│
├── exports/                 # Generated export files (auto-created)
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── workshot.db             # SQLite database (auto-created)
└── README.md
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.10+, FastAPI, Uvicorn |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Database** | SQLite3 (lightweight, serverless) |
| **Windows APIs** | pywin32, psutil, screeninfo |
| **Icons** | Iconify API (logos, fluent-ui) |
| **Real-time** | Server-Sent Events (SSE) |

---

## 📊 Dashboard Sections

### 🔴 Live Activity
Displays the currently active application with:
- App name and icon
- Window title
- Active monitor
- Live duration timer

### 📈 Today's Usage
Quick stats:
- Total active time
- Number of apps used
- Total sessions recorded

### 📱 App Breakdown
Interactive list showing:
- App name with official logo
- Session count
- Visual progress bar
- Total duration

### 🖥️ Monitor Breakdown
Time distribution across:
- Monitor 1
- Monitor 2

### 📋 Session Log
Recent activity with:
- Start time
- App name
- Window title
- Duration
- Monitor

---

## 📤 Exporting Data

WorkShot offers three export formats:

### 📄 CSV Export
Raw session data in spreadsheet format:
```csv
ID,App Name,Window Title,Monitor,Start Time,Duration
1,Chrome,GitHub - WorkShot,1,2025-12-11 14:30:00,125
```

### 🔗 JSON Export
Structured data for programmatic access:
```json
{
  "metadata": {
    "generated": "2025-12-11 15:24:59",
    "date_range": "All Time"
  },
  "sessions": [...]
}
```

### 🎨 HTML Report
Beautiful, mobile-responsive report with:
- Summary statistics
- App breakdown with progress bars
- Session details
- Custom date ranges

---

## 🔒 Privacy & Security

### Local-First Design
- **All data stays on your machine** - No cloud servers, no external APIs (except icon CDN)
- **SQLite database** stored in project directory
- **No telemetry** or usage tracking

### What We Track
✅ Active window title  
✅ Application name  
✅ Monitor number  
✅ Session duration  
✅ Idle periods  

### What We DON'T Track
❌ Keystrokes  
❌ Screenshots  
❌ Network traffic  
❌ File contents  
❌ Personal data  

---

## ⚙️ Configuration

### Idle Detection
Default: 5 minutes of inactivity

To adjust, modify `tracker/monitor.py`:
```python
self.idle_detector = IdleDetector(threshold_seconds=300)  # 5 minutes
```

### Monitoring Interval
Default: 1 second poll rate

Adjust in `tracker/monitor.py`:
```python
await asyncio.sleep(1)  # Poll interval
```

### Database Location
By default, `workshot.db` is created in the project root. To change:
```python
# In tracker/db.py
DB_PATH = Path("custom/path/workshot.db")
```

---

## 🐛 Troubleshooting

### Dashboard won't load
- **Check if port 8787 is available**
  ```bash
  netstat -an | findstr 8787
  ```
- **Try restarting** the application
- **Check firewall** settings

### Tracker not detecting apps
- **Run as Administrator** (some apps require elevated permissions)
- **Check Windows API access** - Ensure pywin32 is installed correctly

### Export is slow
- **Large datasets** can take time to process
- Use **date filters** to limit export size
- **CSV/JSON** formats are faster than HTML

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. Create a **feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. Open a **Pull Request**

---

## 📝 To-Do / Roadmap

- [ ] **Productivity insights** - AI-powered analysis
- [ ] **Custom categories** - Tag apps as "Work", "Entertainment", etc.
- [ ] **Goals & limits** - Set time limits per app/category
- [ ] **Weekly/Monthly reports** - Automated email summaries
- [ ] **Dark/Light theme toggle**
- [ ] **App blocking** - Temporarily block distracting apps
- [ ] **Cross-platform support** (macOS, Linux)

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Iconify** - For comprehensive app icon library
- **FastAPI** - Lightning-fast Python web framework
- **Fluent UI** - Microsoft's modern icon system
- **Python Community** - For excellent Windows API bindings

---

## 💬 Support

- 🐛 **Bug reports**: [Open an issue](https://github.com/yourusername/workshot/issues)
- 💡 **Feature requests**: [Start a discussion](https://github.com/yourusername/workshot/discussions)
- 📧 **Contact**: your.email@example.com

---

<div align="center">

**⚡ Built with passion for productivity ⚡**

[⭐ Star this repo](https://github.com/yourusername/workshot) • [🍴 Fork it](https://github.com/yourusername/workshot/fork) • [📢 Share it](https://twitter.com/intent/tweet?text=Check%20out%20WorkShot%20-%20A%20beautiful%20activity%20tracker%20for%20Windows!&url=https://github.com/yourusername/workshot)

</div>
