#!/usr/bin/env python3
"""
Opportunity Hunter — SQLite Database Module
Manages local persistence for Student Profile, Kanban Applications,
Saved Opportunities, and Activity Logs using Python standard library.
"""

import os
import sqlite3
import json
from datetime import datetime, timezone

def utc_now_iso():
    try:
        return datetime.now(timezone.utc).isoformat()
    except Exception:
        return datetime.utcnow().isoformat()

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "opportunity_hunter.db")

_MEM_HOLDER = None

def get_connection(db_path=DEFAULT_DB_PATH):
    global _MEM_HOLDER
    if db_path == ":memory:":
        if _MEM_HOLDER is None:
            _MEM_HOLDER = sqlite3.connect("file:memdb_shared?mode=memory&cache=shared", uri=True)
        conn = sqlite3.connect("file:memdb_shared?mode=memory&cache=shared", uri=True)
    else:
        conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=DEFAULT_DB_PATH):
    """Initialize database tables with optimal indexing."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        
        # 1. Student Profile Table (single-tenant local profile)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                name TEXT DEFAULT 'Student',
                degree TEXT DEFAULT '',
                year TEXT DEFAULT '',
                graduation_year TEXT DEFAULT '',
                skills TEXT DEFAULT '[]',
                location TEXT DEFAULT '',
                opportunity_type TEXT DEFAULT 'any',
                work_mode TEXT DEFAULT 'any',
                interests TEXT DEFAULT '',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Application Tracker Table (8 Kanban Stages)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                organization TEXT DEFAULT '',
                url TEXT DEFAULT '',
                stage TEXT NOT NULL DEFAULT 'interested',
                notes TEXT DEFAULT '',
                deadline TEXT DEFAULT '',
                applied_date TEXT DEFAULT '',
                interview_date TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_apps_stage ON applications(stage)")

        # 3. Saved Opportunities Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_opportunities (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                organization TEXT DEFAULT '',
                url TEXT NOT NULL,
                data_json TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 4. Activity Log Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                details TEXT DEFAULT '',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Ensure default empty profile row exists
        cursor.execute("SELECT id FROM profiles WHERE id = 1")
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO profiles (id, name, degree, year, graduation_year, skills, location, opportunity_type, work_mode, interests)
                VALUES (1, 'Student', '', '', '', '[]', '', 'any', 'any', 'Software Engineering')
            """)
            
        conn.commit()
    finally:
        conn.close()

# -------------------------------------------------------------
# Profile Queries
# -------------------------------------------------------------
def get_profile(db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        row = conn.execute("SELECT * FROM profiles WHERE id = 1").fetchone()
        if not row:
            return None
        res = dict(row)
        try:
            res["skills"] = json.loads(res["skills"])
        except Exception:
            res["skills"] = [s.strip() for s in res["skills"].split(",") if s.strip()]
        return res
    finally:
        conn.close()

def save_profile(data, db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        skills = data.get("skills", [])
        if isinstance(skills, list):
            skills_json = json.dumps(skills)
        else:
            skills_json = json.dumps([s.strip() for s in str(skills).split(",") if s.strip()])
            
        now = utc_now_iso()
        conn.execute("""
            INSERT INTO profiles (id, name, degree, year, graduation_year, skills, location, opportunity_type, work_mode, interests, updated_at)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                degree=excluded.degree,
                year=excluded.year,
                graduation_year=excluded.graduation_year,
                skills=excluded.skills,
                location=excluded.location,
                opportunity_type=excluded.opportunity_type,
                work_mode=excluded.work_mode,
                interests=excluded.interests,
                updated_at=excluded.updated_at
        """, (
            data.get("name", "Student") or "Student",
            data.get("degree", ""),
            data.get("year", ""),
            data.get("graduation_year", ""),
            skills_json,
            data.get("location", ""),
            data.get("opportunity_type", "any"),
            data.get("work_mode", "any"),
            data.get("interests", ""),
            now
        ))
        
        # Log profile update
        conn.execute(
            "INSERT INTO activity_log (action, details, timestamp) VALUES (?, ?, ?)",
            ("profile_updated", f"Updated student profile ({data.get('degree', 'degree')} - {data.get('year', 'year')})", now)
        )
        conn.commit()
        return get_profile(db_path)
    finally:
        conn.close()

# -------------------------------------------------------------
# Application Tracker Queries (8 Kanban Stages)
# -------------------------------------------------------------
VALID_STAGES = {"interested", "planning", "applied", "assessment", "interviewing", "selected", "rejected", "withdrawn"}

def list_applications(stage=None, db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        if stage and stage in VALID_STAGES:
            rows = conn.execute("SELECT * FROM applications WHERE stage = ? ORDER BY updated_at DESC", (stage,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM applications ORDER BY updated_at DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def save_application(app_data, db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        app_id = app_data.get("id") or str(int(datetime.utcnow().timestamp() * 1000))
        title = app_data.get("title", "").strip() or "Untitled Opportunity"
        stage = app_data.get("stage", "interested")
        if stage not in VALID_STAGES:
            stage = "interested"
            
        now = utc_now_iso()
        conn.execute("""
            INSERT INTO applications (id, title, organization, url, stage, notes, deadline, applied_date, interview_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                organization=excluded.organization,
                url=excluded.url,
                stage=excluded.stage,
                notes=excluded.notes,
                deadline=excluded.deadline,
                applied_date=excluded.applied_date,
                interview_date=excluded.interview_date,
                updated_at=excluded.updated_at
        """, (
            app_id,
            title,
            app_data.get("organization", ""),
            app_data.get("url", ""),
            stage,
            app_data.get("notes", ""),
            app_data.get("deadline", ""),
            app_data.get("applied_date", ""),
            app_data.get("interview_date", ""),
            now,
            now
        ))
        
        conn.execute(
            "INSERT INTO activity_log (action, details, timestamp) VALUES (?, ?, ?)",
            ("application_saved", f"Application '{title}' tracked under stage '{stage}'", now)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM applications WHERE id = ?", (app_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def delete_application(app_id, db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        existing = conn.execute("SELECT title FROM applications WHERE id = ?", (app_id,)).fetchone()
        title = existing["title"] if existing else app_id
        cursor = conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        if cursor.rowcount > 0:
            conn.execute(
                "INSERT INTO activity_log (action, details) VALUES (?, ?)",
                ("application_deleted", f"Removed application '{title}'")
            )
            conn.commit()
            return True
        return False
    finally:
        conn.close()

# -------------------------------------------------------------
# Saved Opportunities Queries
# -------------------------------------------------------------
def list_saved(db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT * FROM saved_opportunities ORDER BY created_at DESC").fetchall()
        result = []
        for r in rows:
            d = dict(r)
            try:
                d["data"] = json.loads(d["data_json"])
            except Exception:
                d["data"] = {}
            result.append(d)
        return result
    finally:
        conn.close()

def save_opportunity_item(item, db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        opp_id = item.get("id") or item.get("url") or str(int(datetime.utcnow().timestamp() * 1000))
        title = item.get("title", "").strip() or "Untitled Opportunity"
        org = item.get("organization") or item.get("org", "")
        url = item.get("url", "")
        data_json = json.dumps(item)
        now = utc_now_iso()
        
        conn.execute("""
            INSERT INTO saved_opportunities (id, title, organization, url, data_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                organization=excluded.organization,
                url=excluded.url,
                data_json=excluded.data_json
        """, (opp_id, title, org, url, data_json, now))
        
        conn.execute(
            "INSERT INTO activity_log (action, details, timestamp) VALUES (?, ?, ?)",
            ("opportunity_saved", f"Saved opportunity '{title}' ({org})", now)
        )
        conn.commit()
        return {"id": opp_id, "title": title, "url": url}
    finally:
        conn.close()

def delete_saved_opportunity(opp_id, db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("DELETE FROM saved_opportunities WHERE id = ?", (opp_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

# -------------------------------------------------------------
# Activity Log & Analytics Queries
# -------------------------------------------------------------
def get_activity_log(limit=15, db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT * FROM activity_log ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_analytics(db_path=DEFAULT_DB_PATH):
    """Compute live metrics derived from actual database records."""
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        total_apps = conn.execute("SELECT COUNT(*) AS c FROM applications").fetchone()["c"]
        stage_counts = {}
        for stage in VALID_STAGES:
            stage_counts[stage] = 0
            
        rows = conn.execute("SELECT stage, COUNT(*) as cnt FROM applications GROUP BY stage").fetchall()
        for r in rows:
            stage_counts[r["stage"]] = r["cnt"]
            
        total_saved = conn.execute("SELECT COUNT(*) AS c FROM saved_opportunities").fetchone()["c"]
        
        profile = get_profile(db_path)
        profile_skills_count = len(profile.get("skills", [])) if profile else 0
        
        return {
            "total_applications": total_apps,
            "total_saved": total_saved,
            "stage_breakdown": stage_counts,
            "applied_count": stage_counts.get("applied", 0),
            "interviewing_count": stage_counts.get("interviewing", 0),
            "selected_count": stage_counts.get("selected", 0),
            "profile_skills_count": profile_skills_count
        }
    finally:
        conn.close()
