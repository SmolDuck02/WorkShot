"""FastAPI dashboard server with SSE for live updates."""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator
from pydantic import BaseModel
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from tracker.db import get_db
from tracker import db
from tracker.monitor import get_monitor
from tracker.utils import format_duration, format_duration_compact, sanitize_app_name
from tracker.export import export_csv, export_json, export_html

from main import record_daily_note

# Paths
DASHBOARD_DIR = Path(__file__).parent
STATIC_DIR = DASHBOARD_DIR / "static"
TEMPLATES_DIR = DASHBOARD_DIR / "templates"

# FastAPI app
app = FastAPI(title="WorkShot Dashboard")

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

class SessionLabelCreate(BaseModel):
    name: str
    color: str = "#5b8def"

class StatusUpdate(BaseModel):
    status: str # 'done', 'todo', or 'partial'

class LabelEdit(BaseModel):
    name: str
    color: str

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Serve the main dashboard page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/current")
async def get_current_activity():
    """Get current activity state."""
    monitor = get_monitor()
    activity = monitor.get_current_activity()
    
    if activity:
        activity['elapsed_formatted'] = format_duration(activity['elapsed_seconds'])
    
    return activity or {"status": "idle", "elapsed_seconds": 0, "elapsed_formatted": "00:00:00"}


@app.get("/api/today")
async def get_today_data():
    """Get today's activity summary."""
    summary = db.get_today_summary()
    
    # Add formatted durations and display names
    for item in summary:
        item['duration_formatted'] = format_duration(item['total_seconds'])
        item['app_display'] = sanitize_app_name(item['app_name'])
    
    return {
        "summary": summary,
        "total_seconds": sum(item['total_seconds'] for item in summary),
        "total_formatted": format_duration_compact(sum(item['total_seconds'] for item in summary))
    }


@app.get("/api/monitors")
async def get_monitor_data():
    """Get monitor breakdown data."""
    breakdown = db.get_monitor_breakdown()
    
    for item in breakdown:
        item['duration_formatted'] = format_duration(item['total_seconds'])
    
    return breakdown


@app.get("/api/sessions")
async def get_recent_sessions(limit: int = 20):
    """Get recent activity sessions."""
    sessions = db.get_recent_sessions(limit)
    
    for session in sessions:
        session['duration_formatted'] = format_duration(session['duration_seconds'] or 0)
        session['app_display'] = sanitize_app_name(session['app_name'])
        
        # Format times
        if session['start_time']:
            st = datetime.fromisoformat(session['start_time'])
            session['start_formatted'] = st.strftime("%H:%M:%S")
    
    return sessions


@app.get("/api/stream")
async def stream_updates():
    """Server-Sent Events stream for live updates."""
    
    async def event_generator() -> AsyncGenerator[str, None]:
        monitor = get_monitor()
        
        while True:
            try:
                # Get current activity
                activity = monitor.get_current_activity()
                
                if activity:
                    raw_seconds = activity.get('elapsed_seconds', 0)
                    
                    activity['elapsed_seconds'] = raw_seconds
                    activity['elapsed_formatted'] = format_duration(raw_seconds)
                    
                    data = json.dumps(activity)
                else:
                    data = json.dumps({
                        "status": "idle", 
                        "elapsed_seconds": 0, 
                        "elapsed_formatted": "00:00:00"
                    })
                
                yield f"data: {data}\n\n"
                
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"SSE Error: {repr(e)}") 
                await asyncio.sleep(1)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/api/export/{format_type}")
async def export_data(
    format_type: str, 
    start: str = None, 
    end: str = None
):
    """
    Export activity data in various formats.
    
    Args:
        format_type: 'csv', 'json', or 'html'
        start: Start date filter (YYYY-MM-DD), inclusive
        end: End date filter (YYYY-MM-DD), inclusive. Defaults to start if not provided.
    """
    from fastapi.responses import FileResponse
    
    # If only start is provided, use it for both (single day export)
    if start and not end:
        end = start
    
    try:
        if format_type == "csv":
            filepath = export_csv(start, end)
            return FileResponse(
                path=str(filepath),
                filename=filepath.name,
                media_type="text/csv"
            )
        elif format_type == "json":
            filepath = export_json(start, end)
            return FileResponse(
                path=str(filepath),
                filename=filepath.name,
                media_type="application/json"
            )
        elif format_type == "html":
            filepath = export_html(start, end)
            return FileResponse(
                path=str(filepath),
                filename=filepath.name,
                media_type="text/html"
            )
        else:
            return {"error": f"Unknown format: {format_type}. Use 'csv', 'json', or 'html'."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/session-labels")
async def get_session_labels():
    """Fetch all available task session labels."""
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM session_labels ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

@app.post("/api/session-labels")
async def create_session_label(session_label: SessionLabelCreate):
    """Create a new project session label."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO session_labels (name, color) VALUES (?, ?)", 
                      (session_label.name, session_label.color))
        return {"id": cursor.lastrowid}

@app.post("/api/monitor/set-session-label/{session_label_id}")
async def set_monitor_session_label(session_label_id: int):
    """Tell the monitor to start tagging sessions with this session label."""
    # Use 0 or -1 to represent 'None/General'
    actual_id = None if session_label_id <= 0 else session_label_id
    get_monitor().set_active_session_label(actual_id)
    return {"status": "success", "active_session_label_id": actual_id}

@app.put("/api/session-labels/{label_id}/status")
async def update_label_status(label_id: int, payload: StatusUpdate):
    """Updates a label's status and logs it to the Dailies markdown file."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM session_labels WHERE id = ?", (label_id,))
            row = cursor.fetchone()
            print(row)
            if not row:
                raise HTTPException(status_code=404, detail="Label not found")
            
            label_name = row[0]

            cursor.execute("UPDATE session_labels SET status = ? WHERE id = ?", 
                          (payload.status, label_id))
            conn.commit()

        log_message = f"Task: {label_name}"
        record_daily_note(payload.status, log_message)

        # If you mark the currently active task as 'done', reset the monitor to 'General'
        monitor = get_monitor()
        if monitor.current_session_label_id == label_id and payload.status == 'done':
            monitor.set_active_session_label(None)
            return {"status": "success", "message": "Logged to dailies. Monitor reset to General."}

        return {"status": "success", "message": "Logged to dailies."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/session-labels/{label_id}")
async def edit_label(label_id: int, payload: LabelEdit):
    print("hrtht",payload)
    """Edits a task's name and color."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE session_labels SET name = ?, color = ? WHERE id = ?", 
                          (payload.name, payload.color, label_id))
            conn.commit()
        return {"status": "success", "message": "Label updated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/session-labels/{label_id}")
async def delete_label(label_id: int):
    """Deletes a task and resets the monitor if it was active."""
    try:
        # Safety Check: If we are deleting the active task, reset monitor to General
        monitor = get_monitor()
        if monitor.current_session_label_id == label_id:
            monitor.set_active_label(None)

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM session_labels WHERE id = ?", (label_id,))
            conn.commit()
            
        return {"status": "success", "message": "Label deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_server(host: str = "127.0.0.1", port: int = 8787):
    """Run the dashboard server."""
    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level="info")


