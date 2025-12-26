"""Export functionality for activity data."""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from . import db
from .utils import format_duration, sanitize_app_name


# Icon sources for HTML export - using Iconify API (same as dashboard)
APP_ICON_SOURCES = {
    # Browsers
    'chrome': 'https://api.iconify.design/logos:chrome.svg',
    'firefox': 'https://api.iconify.design/logos:firefox.svg',
    'edge': 'https://api.iconify.design/logos:microsoft-edge.svg',
    'msedge': 'https://api.iconify.design/logos:microsoft-edge.svg',
    'opera': 'https://api.iconify.design/logos:opera.svg',
    'brave': 'https://api.iconify.design/logos:brave.svg',
    'safari': 'https://api.iconify.design/logos:safari.svg',
    'arc': 'https://api.iconify.design/simple-icons:arc.svg',
    # Code Editors
    'vs code': 'https://api.iconify.design/logos:visual-studio-code.svg',
    'cursor': 'https://api.iconify.design/simple-icons:cursor.svg',
    'visual studio': 'https://api.iconify.design/logos:visual-studio.svg',
    'sublime': 'https://api.iconify.design/logos:sublime-text-icon.svg',
    'notepad++': 'https://api.iconify.design/simple-icons:notepadplusplus.svg',
    'intellij': 'https://api.iconify.design/logos:intellij-idea.svg',
    'pycharm': 'https://api.iconify.design/logos:pycharm.svg',
    # Communication
    'discord': 'https://api.iconify.design/logos:discord-icon.svg',
    'slack': 'https://api.iconify.design/logos:slack-icon.svg',
    'teams': 'https://api.iconify.design/logos:microsoft-teams.svg',
    'zoom': 'https://api.iconify.design/logos:zoom-icon.svg',
    'telegram': 'https://api.iconify.design/logos:telegram.svg',
    'whatsapp': 'https://api.iconify.design/logos:whatsapp-icon.svg',
    # Entertainment
    'spotify': 'https://api.iconify.design/logos:spotify-icon.svg',
    'youtube': 'https://api.iconify.design/logos:youtube-icon.svg',
    'netflix': 'https://api.iconify.design/logos:netflix-icon.svg',
    'twitch': 'https://api.iconify.design/logos:twitch.svg',
    # Gaming
    'steam': 'https://api.iconify.design/logos:steam-icon.svg',
    'valorant': 'https://api.iconify.design/simple-icons:valorant.svg',
    'epic': 'https://api.iconify.design/simple-icons:epicgames.svg',
    # Design
    'figma': 'https://api.iconify.design/logos:figma.svg',
    'photoshop': 'https://api.iconify.design/logos:adobe-photoshop.svg',
    'illustrator': 'https://api.iconify.design/logos:adobe-illustrator.svg',
    'blender': 'https://api.iconify.design/logos:blender.svg',
    'canva': 'https://api.iconify.design/simple-icons:canva.svg',
    # Dev Tools
    'github': 'https://api.iconify.design/logos:github-icon.svg',
    'docker': 'https://api.iconify.design/logos:docker-icon.svg',
    'postman': 'https://api.iconify.design/logos:postman-icon.svg',
    'powershell': 'https://api.iconify.design/devicon-plain:powershell.svg',
    'windowsterminal': 'https://api.iconify.design/simple-icons:windowsterminal.svg',
    'windows terminal': 'https://api.iconify.design/simple-icons:windowsterminal.svg',
    # Productivity
    'notion': 'https://api.iconify.design/logos:notion-icon.svg',
    'obsidian': 'https://api.iconify.design/simple-icons:obsidian.svg',
    'asana': 'https://api.iconify.design/logos:asana-icon.svg',
    'trello': 'https://api.iconify.design/logos:trello.svg',
    'jira': 'https://api.iconify.design/logos:jira.svg',
    'outlook': 'https://api.iconify.design/logos:microsoft-outlook.svg',
    'word': 'https://api.iconify.design/vscode-icons:file-type-word.svg',
    'excel': 'https://api.iconify.design/vscode-icons:file-type-excel.svg',
    # Windows System Apps
    'file explorer': 'https://api.iconify.design/fluent:folder-24-filled.svg',
    'explorer': 'https://api.iconify.design/fluent:folder-24-filled.svg',
    'notepad': 'https://api.iconify.design/fluent:notepad-24-regular.svg',
    'snipping': 'https://api.iconify.design/fluent:screenshot-24-regular.svg',
    'snippingtool': 'https://api.iconify.design/fluent:screenshot-24-regular.svg',
    'calculator': 'https://api.iconify.design/fluent:calculator-24-regular.svg',
    'photos': 'https://api.iconify.design/fluent:image-24-filled.svg',
    'paint': 'https://api.iconify.design/fluent:paint-brush-24-regular.svg',
    'settings': 'https://api.iconify.design/fluent:settings-24-filled.svg',
    'shellexperiencehost': 'https://api.iconify.design/fluent:window-24-filled.svg',
    'microsoft store': 'https://api.iconify.design/fluent:store-microsoft-24-filled.svg',
    'store': 'https://api.iconify.design/fluent:store-microsoft-24-filled.svg',
    # Special states
    'idle': 'https://api.iconify.design/icon-park-outline:sleep-one.svg',
    # Other
    'deepl': 'https://api.iconify.design/simple-icons:deepl.svg',
    'openvpn': 'https://api.iconify.design/simple-icons:openvpn.svg',
    'norton': 'https://api.iconify.design/simple-icons:norton.svg',
}

# Generic fallback icons
GENERIC_ICONS = {
    'terminal': 'https://api.iconify.design/fluent:window-console-20-filled.svg',
    'shell': 'https://api.iconify.design/fluent:window-console-20-filled.svg',
    'cmd': 'https://api.iconify.design/fluent:window-console-20-filled.svg',
    'bash': 'https://api.iconify.design/fluent:window-console-20-filled.svg',
}


def get_app_icon_html(app_name: str) -> str:
    """Get HTML for app icon - uses specific icons, generic fallbacks, or final generic app icon."""
    lower = app_name.lower()
    
    # Try specific app icons
    for key, url in APP_ICON_SOURCES.items():
        if key in lower:
            return f'<img src="{url}" alt="" class="app-icon">'
    
    # Try generic category icons
    for key, url in GENERIC_ICONS.items():
        if key in lower:
            return f'<img src="{url}" alt="" class="app-icon">'
    
    # Final fallback: generic app icon
    return f'<img src="https://api.iconify.design/fluent:app-generic-24-filled.svg" alt="" class="app-icon">'

# Export directory
EXPORTS_DIR = Path(__file__).parent.parent / "exports"


def ensure_exports_dir():
    """Create exports directory if it doesn't exist."""
    EXPORTS_DIR.mkdir(exist_ok=True)
    return EXPORTS_DIR


def get_export_filename(prefix: str, extension: str) -> Path:
    """Generate timestamped export filename."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return ensure_exports_dir() / f"{prefix}_{timestamp}.{extension}"


def get_all_sessions(
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None,
    limit: Optional[int] = None
) -> list[dict]:
    """
    Get all sessions, optionally filtered by date range.
    
    Args:
        start_date: Start date filter (YYYY-MM-DD), inclusive
        end_date: End date filter (YYYY-MM-DD), inclusive
        limit: Maximum number of sessions to return (for performance)
    """
    with db.get_db() as conn:
        cursor = conn.cursor()
        
        # Build query with optional limit
        limit_clause = f" LIMIT {limit}" if limit else ""
        
        if start_date and end_date:
            # Date range query (inclusive of both dates)
            cursor.execute(f"""
                SELECT * FROM sessions 
                WHERE DATE(start_time) >= ? AND DATE(start_time) <= ?
                ORDER BY start_time DESC{limit_clause}
            """, (start_date, end_date))
        elif start_date:
            # Single date (start only = that specific day)
            cursor.execute(f"""
                SELECT * FROM sessions 
                WHERE DATE(start_time) = ?
                ORDER BY start_time DESC{limit_clause}
            """, (start_date,))
        else:
            # All sessions - limit for performance when no date filter
            if not limit:
                limit_clause = " LIMIT 2000"  # Default limit for "All Time" (reduced for performance)
            cursor.execute(f"""
                SELECT * FROM sessions 
                ORDER BY start_time DESC{limit_clause}
            """)
        
        return [dict(row) for row in cursor.fetchall()]


def get_date_range_label(start_date: Optional[str], end_date: Optional[str]) -> str:
    """Generate a human-readable label for the date range."""
    if not start_date and not end_date:
        return "All Time"
    elif start_date == end_date or (start_date and not end_date):
        return start_date
    else:
        return f"{start_date} to {end_date}"


def export_csv(
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
) -> Path:
    """
    Export sessions to CSV file.
    
    Args:
        start_date: Start date filter (YYYY-MM-DD)
        end_date: End date filter (YYYY-MM-DD)
    
    Returns the path to the created file.
    """
    sessions = get_all_sessions(start_date, end_date)
    filepath = get_export_filename("sessions", "csv")
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'ID',
            'App Name',
            'App Display Name',
            'Window Title',
            'Monitor',
            'Start Time',
            'End Time',
            'Duration (seconds)',
            'Duration (formatted)'
        ])
        
        # Data rows
        for session in sessions:
            writer.writerow([
                session['id'],
                session['app_name'],
                sanitize_app_name(session['app_name']),
                session['window_title'],
                session['monitor'],
                session['start_time'],
                session['end_time'] or '',
                session['duration_seconds'] or 0,
                format_duration(session['duration_seconds'] or 0)
            ])
    
    return filepath


def export_json(
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
) -> Path:
    """
    Export sessions to detailed JSON file.
    
    Args:
        start_date: Start date filter (YYYY-MM-DD)
        end_date: End date filter (YYYY-MM-DD)
    
    Returns the path to the created file.
    """
    sessions = get_all_sessions(start_date, end_date)
    
    # Calculate summary statistics
    total_seconds = sum(s['duration_seconds'] or 0 for s in sessions)
    
    # Group by app
    app_totals = {}
    for session in sessions:
        app = session['app_name']
        if app not in app_totals:
            app_totals[app] = {
                'app_name': app,
                'app_display': sanitize_app_name(app),
                'total_seconds': 0,
                'session_count': 0
            }
        app_totals[app]['total_seconds'] += session['duration_seconds'] or 0
        app_totals[app]['session_count'] += 1
    
    # Sort by total time
    by_app = sorted(app_totals.values(), key=lambda x: x['total_seconds'], reverse=True)
    for item in by_app:
        item['total_formatted'] = format_duration(item['total_seconds'])
    
    # Group by monitor
    monitor_totals = {}
    for session in sessions:
        m = session['monitor']
        if m <= 0:
            continue
        if m not in monitor_totals:
            monitor_totals[m] = {'monitor': m, 'total_seconds': 0, 'session_count': 0}
        monitor_totals[m]['total_seconds'] += session['duration_seconds'] or 0
        monitor_totals[m]['session_count'] += 1
    
    by_monitor = sorted(monitor_totals.values(), key=lambda x: x['monitor'])
    for item in by_monitor:
        item['total_formatted'] = format_duration(item['total_seconds'])
    
    # Enrich sessions
    enriched_sessions = []
    for session in sessions:
        enriched_sessions.append({
            'id': session['id'],
            'app_name': session['app_name'],
            'app_display': sanitize_app_name(session['app_name']),
            'window_title': session['window_title'],
            'monitor': session['monitor'],
            'start_time': session['start_time'],
            'end_time': session['end_time'],
            'duration_seconds': session['duration_seconds'] or 0,
            'duration_formatted': format_duration(session['duration_seconds'] or 0)
        })
    
    # Build export object
    export_data = {
        'exported_at': datetime.now().isoformat(),
        'date_range': get_date_range_label(start_date, end_date),
        'start_date': start_date,
        'end_date': end_date,
        'summary': {
            'total_sessions': len(sessions),
            'total_seconds': total_seconds,
            'total_formatted': format_duration(total_seconds),
            'unique_apps': len(app_totals),
            'monitors_used': len(monitor_totals)
        },
        'by_app': by_app,
        'by_monitor': by_monitor,
        'sessions': enriched_sessions
    }
    
    filepath = get_export_filename("sessions", "json")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return filepath


def export_html(
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
) -> Path:
    """
    Export sessions to a styled HTML report.
    
    Args:
        start_date: Start date filter (YYYY-MM-DD)
        end_date: End date filter (YYYY-MM-DD)
    
    Returns the path to the created file.
    """
    sessions = get_all_sessions(start_date, end_date)
    
    # Calculate stats
    total_seconds = sum(s['duration_seconds'] or 0 for s in sessions)
    
    # Group by app
    app_totals = {}
    for session in sessions:
        app = session['app_name']
        display = sanitize_app_name(app)
        if display not in app_totals:
            app_totals[display] = {'total_seconds': 0, 'count': 0}
        app_totals[display]['total_seconds'] += session['duration_seconds'] or 0
        app_totals[display]['count'] += 1
    
    by_app_sorted = sorted(app_totals.items(), key=lambda x: x[1]['total_seconds'], reverse=True)
    max_app_time = by_app_sorted[0][1]['total_seconds'] if by_app_sorted else 1
    
    # Limit apps shown for performance (top 30 apps)
    by_app_sorted = by_app_sorted
    
    # Group by monitor
    monitor_totals = {1: 0, 2: 0}
    for session in sessions:
        m = session['monitor']
        monitor_totals[m] = monitor_totals.get(m, 0) + (session['duration_seconds'] or 0)
    
    # Generate HTML
    date_str = get_date_range_label(start_date, end_date)
    export_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build app cards with icons
    app_cards = ""
    for app_name, data in by_app_sorted:
        pct = (data['total_seconds'] / max_app_time * 100) if max_app_time > 0 else 0
        icon_html = get_app_icon_html(app_name)
        app_cards += f"""
            <div class="app-card">
                <div class="app-icon-container">{icon_html}</div>
                <div class="app-card-info">
                    <div class="app-card-name">{app_name}</div>
                    <div class="app-card-meta">{data['count']} session{'s' if data['count'] != 1 else ''}</div>
                    <div class="app-card-bar">
                        <div class="bar-container">
                            <div class="bar" style="width: {pct}%"></div>
                        </div>
                    </div>
                </div>
                <div class="app-card-time">{format_duration(data['total_seconds'])}</div>
            </div>"""
    
    # Build session cards (limit to 50 most recent for performance)
    session_cards = ""
    for s in sessions:
        start_time = s['start_time'][11:16] if s['start_time'] and len(s['start_time']) > 16 else '--:--'
        title = s['window_title'][:40] if s['window_title'] else '-'
        monitor = '-' if s['is_idle'] else 'M' + str(s['monitor'])
        if s['window_title'] and len(s['window_title']) > 40:
            title += '...'
        session_cards += f"""
            <div class="session-card">
                <span class="session-card-time">{start_time}</span>
                <span class="session-card-app">{sanitize_app_name(s['app_name'])}</span>
                <span class="session-card-title">{title}</span>
                <span class="session-card-duration">{format_duration(s['duration_seconds'] or 0)}</span>
                <span class="session-card-monitor">{monitor}</span>
            </div>"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>WorkShot Report - {date_str}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --bg: #0c0c0f;
            --card: #141418;
            --elevated: #1a1a1f;
            --border: #27272a;
            --border-light: #3f3f46;
            --accent: #5b8def;
            --purple: #8b7cf6;
            --text-primary: #e4e4e7;
            --text-secondary: #a1a1aa;
            --text-muted: #52525b;
        }}
        
        html {{ font-size: 16px; }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg);
            color: var(--text-secondary);
            min-height: 100vh;
            padding: 1rem;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg); }}
        ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
        
        .container {{
            max-width: 700px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            padding: 1.25rem 1rem;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 10px;
            margin-bottom: 0.75rem;
        }}
        
        .header h1 {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }}
        
        .header .subtitle {{
            color: var(--text-muted);
            font-size: 0.75rem;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.5rem;
            margin-bottom: 0.75rem;
        }}
        
        .stat-card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.75rem 0.5rem;
            text-align: center;
        }}
        
        .stat-value {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-primary);
        }}
        
        .stat-label {{
            font-size: 0.6rem;
            font-weight: 500;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-top: 0.125rem;
        }}
        
        .section {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.875rem;
            margin-bottom: 0.75rem;
        }}
        
        .section h2 {{
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.75rem;
            padding-bottom: 0.625rem;
            border-bottom: 1px solid var(--border);
        }}
        
        /* App icons */
        .app-icon-container {{
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        
        .app-icon {{
            width: 24px;
            height: 24px;
            object-fit: contain;
            filter: brightness(0) saturate(100%) invert(55%) sepia(52%) saturate(682%) hue-rotate(190deg) brightness(97%) contrast(92%);
        }}
        
        .app-letter {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--accent);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        /* App cards - mobile first */
        .app-card {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.625rem;
            background: var(--elevated);
            border-radius: 6px;
            margin-bottom: 0.375rem;
        }}
        
        .app-card-info {{
            flex: 1;
            min-width: 0;
        }}
        
        .app-card-name {{
            font-weight: 500;
            color: var(--text-primary);
            font-size: 0.85rem;
        }}
        
        .app-card-meta {{
            font-size: 0.7rem;
            color: var(--text-muted);
            margin-top: 0.125rem;
        }}
        
        .app-card-time {{
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent);
            font-weight: 500;
            font-size: 0.85rem;
            white-space: nowrap;
        }}
        
        .app-card-bar {{
            width: 100%;
            margin-top: 0.375rem;
        }}
        
        .bar-container {{
            background: var(--border);
            border-radius: 2px;
            height: 3px;
            width: 100%;
        }}
        
        .bar {{
            background: var(--accent);
            height: 100%;
            border-radius: 2px;
        }}
        
        /* Session cards */
        .session-card {{
            display: flex;
            align-items: center;
            gap: 0.625rem;
            padding: 0.5rem 0.625rem;
            border-radius: 4px;
            margin-bottom: 0.25rem;
        }}
        
        .session-card:nth-child(odd) {{
            background: var(--elevated);
        }}
        
        .session-card-time {{
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-muted);
            font-size: 0.7rem;
            min-width: 45px;
        }}
        
        .session-card-app {{
            font-weight: 500;
            color: var(--text-primary);
            font-size: 0.8rem;
            min-width: 80px;
        }}
        
        .session-card-title {{
            flex: 1;
            font-size: 0.7rem;
            color: var(--text-muted);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .session-card-duration {{
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent);
            font-size: 0.7rem;
            min-width: 40px;
            text-align: right;
        }}
        
        .session-card-monitor {{
            font-size: 0.6rem;
            color: var(--text-muted);
            background: var(--border);
            padding: 0.125rem 0.3rem;
            border-radius: 3px;
        }}
        
        /* Monitor grid */
        .monitor-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
        }}
        
        .monitor-card {{
            background: var(--elevated);
            border-radius: 6px;
            padding: 0.75rem;
            text-align: center;
            border-top: 2px solid transparent;
        }}
        
        .monitor-card.m1 {{ border-top-color: var(--accent); }}
        .monitor-card.m2 {{ border-top-color: var(--purple); }}
        
        .monitor-card .label {{
            font-size: 0.6rem;
            font-weight: 500;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.25rem;
        }}
        
        .monitor-card .value {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            font-weight: 600;
        }}
        
        .monitor-card.m1 .value {{ color: var(--accent); }}
        .monitor-card.m2 .value {{ color: var(--purple); }}
        
        .footer {{
            text-align: center;
            padding: 1rem;
            color: var(--text-muted);
            font-size: 0.7rem;
        }}
        
        /* Mobile */
        @media (max-width: 500px) {{
            html {{ font-size: 14px; }}
            body {{ padding: 0.5rem; }}
            
            .header {{ padding: 1rem 0.75rem; }}
            .header h1 {{ font-size: 1.1rem; }}
            
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            
            .session-card-title {{ display: none; }}
            .session-card {{ gap: 0.5rem; }}
        }}
        
        @media print {{
            body {{ background: #fff; color: #333; padding: 0.5rem; }}
            .header, .section, .stat-card, .app-card, .session-card, .monitor-card {{ 
                background: #f9fafb; border-color: #e5e7eb; 
            }}
            .stat-value, .app-card-time, .session-card-duration {{ color: #2563eb; }}
            .monitor-card.m1 .value {{ color: #2563eb; }}
            .monitor-card.m2 .value {{ color: #7c3aed; }}
        }}
        
        @media print {{
            body {{ 
                background: #fff; 
                color: #333; 
                padding: 1rem;
            }}
            .stat-value, td.time, .app-card-time, .session-card-duration {{ 
                color: #2563eb; 
            }}
            .header, .section, .stat-card, .monitor-card {{ 
                background: #f9fafb; 
                border-color: #e5e7eb; 
            }}
            .bar {{
                background: #2563eb;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>WorkShot Report</h1>
            <p class="subtitle">Activity Report for {date_str} | Generated: {export_time}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{format_duration(total_seconds)}</div>
                <div class="stat-label">Total Time</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(sessions)}</div>
                <div class="stat-label">Sessions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(app_totals)}</div>
                <div class="stat-label">Apps Used</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len([m for m in monitor_totals.values() if m > 0])}</div>
                <div class="stat-label">Monitors</div>
            </div>
        </div>
        
        <div class="section">
            <h2>App Breakdown</h2>
            {app_cards}
        </div>
        
        <div class="section">
            <h2>Monitor Usage</h2>
            <div class="monitor-grid">
                <div class="monitor-card m1">
                    <div class="label">Monitor 1</div>
                    <div class="value">{format_duration(monitor_totals.get(1, 0))}</div>
                </div>
                <div class="monitor-card m2">
                    <div class="label">Monitor 2</div>
                    <div class="value">{format_duration(monitor_totals.get(2, 0))}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Session Log</h2>
            {session_cards}
        </div>
        
        <div class="footer">
            Generated by WorkShot Activity Tracker
        </div>
    </div>
</body>
</html>"""
    
    filepath = get_export_filename("report", "html")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath


