"""Utility functions for time formatting and data processing."""

from datetime import datetime, timedelta


def format_duration(seconds: int) -> str:
    """Convert seconds to human-readable format like '2h 15m 30s'."""
    if seconds < 0:
        return "0s"
    
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{int(hours)}h")
    if minutes > 0:
        parts.append(f"{int(minutes)}m")
    if secs > 0 or not parts:
        parts.append(f"{int(secs)}s")
    
    return " ".join(parts)


def format_duration_compact(seconds: int) -> str:
    """Convert seconds to compact format like '02:15:30'."""
    if seconds < 0:
        seconds = 0
    
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    
    if hours > 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}"
    else:
        return f"{int(minutes):02d}:{int(secs):02d}"


def get_today_range() -> tuple[datetime, datetime]:
    """Get start and end datetime for today."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    return today, tomorrow


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis if too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def sanitize_app_name(app_name: str) -> str:
    """Clean up application name for display."""
    # Remove .exe extension
    if app_name.lower().endswith('.exe'):
        app_name = app_name[:-4]
    
    # Common app name mappings for cleaner display
    app_mappings = {
        'chrome': 'Chrome',
        'firefox': 'Firefox',
        'msedge': 'Edge',
        'code': 'VS Code',
        'devenv': 'Visual Studio',
        'discord': 'Discord',
        'spotify': 'Spotify',
        'slack': 'Slack',
        'teams': 'Teams',
        'explorer': 'File Explorer',
        'notepad': 'Notepad',
        'cmd': 'Command Prompt',
        'powershell': 'PowerShell',
        'windowsterminal': 'Windows Terminal',
        'cursor': 'Cursor',
    }
    
    lower_name = app_name.lower()
    return app_mappings.get(lower_name, app_name)




