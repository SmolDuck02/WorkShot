"""SQLite database operations for activity tracking."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

# Database file location
DB_PATH = Path(__file__).parent.parent / "workshot.db"


def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory."""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Initialize database tables."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Sessions table - stores each activity session
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT NOT NULL,
                window_title TEXT,
                monitor INTEGER DEFAULT 1,
                start_time DATETIME NOT NULL,
                end_time DATETIME,
                duration_seconds INTEGER DEFAULT 0,
                is_idle INTEGER DEFAULT 0
            )
        """)
        
        # Add is_idle column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE sessions ADD COLUMN is_idle INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Index for faster date-based queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_start_time 
            ON sessions(start_time)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_app_name 
            ON sessions(app_name)
        """)


def start_session(app_name: str, window_title: str, monitor: int, is_idle: bool = False) -> int:
    """Start a new activity session. Returns session ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sessions (app_name, window_title, monitor, start_time, is_idle)
            VALUES (?, ?, ?, ?, ?)
        """, (app_name, window_title, monitor, datetime.now(), 1 if is_idle else 0))
        return cursor.lastrowid


def end_session(session_id: int):
    """End an activity session and calculate duration."""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.now()
        
        # Get start time to calculate duration
        cursor.execute("SELECT start_time FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        
        if row:
            start_time = datetime.fromisoformat(row['start_time'])
            duration = int((now - start_time).total_seconds())
            
            cursor.execute("""
                UPDATE sessions 
                SET end_time = ?, duration_seconds = ?
                WHERE id = ?
            """, (now, duration, session_id))


def get_today_sessions() -> list[dict]:
    """Get all sessions from today."""
    with get_db() as conn:
        cursor = conn.cursor()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        cursor.execute("""
            SELECT * FROM sessions 
            WHERE start_time >= ?
            ORDER BY start_time DESC
        """, (today,))
        
        return [dict(row) for row in cursor.fetchall()]


def get_today_summary(include_idle: bool = False) -> list[dict]:
    """Get aggregated time per app for today."""
    with get_db() as conn:
        cursor = conn.cursor()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Exclude idle sessions from app summary unless specified
        idle_filter = "" if include_idle else "AND (is_idle = 0 OR is_idle IS NULL)"
        
        cursor.execute(f"""
            SELECT 
                app_name,
                SUM(duration_seconds) as total_seconds,
                COUNT(*) as session_count
            FROM sessions 
            WHERE start_time >= ? AND duration_seconds > 0 {idle_filter}
            GROUP BY app_name
            ORDER BY total_seconds DESC
        """, (today,))
        
        return [dict(row) for row in cursor.fetchall()]


def get_monitor_breakdown() -> list[dict]:
    """Get time breakdown by monitor for today (excludes idle sessions)."""
    with get_db() as conn:
        cursor = conn.cursor()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        cursor.execute("""
            SELECT 
                monitor,
                SUM(duration_seconds) as total_seconds,
                COUNT(*) as session_count
            FROM sessions 
            WHERE start_time >= ? AND duration_seconds > 0 
                AND (is_idle = 0 OR is_idle IS NULL) AND monitor > 0
            GROUP BY monitor
            ORDER BY monitor
        """, (today,))
        
        return [dict(row) for row in cursor.fetchall()]


def get_today_idle_time() -> int:
    """Get total idle time for today in seconds."""
    with get_db() as conn:
        cursor = conn.cursor()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        cursor.execute("""
            SELECT COALESCE(SUM(duration_seconds), 0) as total_idle
            FROM sessions 
            WHERE start_time >= ? AND is_idle = 1
        """, (today,))
        
        row = cursor.fetchone()
        return row['total_idle'] if row else 0


def get_recent_sessions(limit: int = 20) -> list[dict]:
    """Get most recent sessions (includes idle sessions)."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, app_name, window_title, monitor, start_time, 
                   end_time, duration_seconds, COALESCE(is_idle, 0) as is_idle
            FROM sessions 
            ORDER BY start_time DESC
            LIMIT ?
        """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]


def get_current_session() -> Optional[dict]:
    """Get the currently active (unclosed) session."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM sessions 
            WHERE end_time IS NULL
            ORDER BY start_time DESC
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        return dict(row) if row else None



