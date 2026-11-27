#!/usr/bin/env python3
"""
Opportunity Hunter 2.0 — High-Performance Student Career Backend Proxy & API
Provides secure TinyFish API proxying, SQLite persistence for Student Profiles,
Kanban Application Tracking, Saved Opportunities, Resume Parsing, and Career Intelligence.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

import db
import intelligence

# 1. Load .env file safely without external dependencies
def load_env(env_path=".env"):
    if not os.path.exists(env_path):
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = val
    except Exception as e:
        print(f"[WARN] Could not parse .env file: {e}", file=sys.stderr)

load_env()

PORT = int(os.environ.get("PORT", 5000))
TINYFISH_SEARCH_URL = "https://api.search.tinyfish.ai"
TINYFISH_FETCH_URL = "https://api.fetch.tinyfish.ai"

# Initialize SQLite Database on startup
try:
    db.init_db()
except Exception as e:
    print(f"[WARN] Database initialization notice: {e}", file=sys.stderr)

class OpportunityHunterHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local testing and cross-origin tools
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path
        query_params = urllib.parse.parse_qs(url_parts.query)

        # Root redirect to main application
        if path in ("/", "/index.html"):
            self.path = "/opportunity-hunter.html"
            return super().do_GET()

        # Health & Status API
        if path == "/api/status":
            api_key = os.environ.get("TINYFISH_API_KEY", "").strip()
            has_key = bool(api_key and api_key != "your_tinyfish_api_key_here")
            resp = {
                "ok": True,
                "version": "2.0.0",
                "has_api_key": has_key,
                "mode": "live" if has_key else "demo_fallback",
                "database": "sqlite_connected",
                "message": "Ready for live search" if has_key else "TINYFISH_API_KEY is not set in .env. Running in demo fixture mode."
            }
            return self.send_json(200, resp)

        # Fixtures API endpoint for frontend fallback
        if path == "/api/fixtures":
            fixtures_path = os.path.join(os.path.dirname(__file__), "opportunity-hunter.fixtures.json")
            if os.path.exists(fixtures_path):
                try:
                    with open(fixtures_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    return self.send_json(200, data)
                except Exception as e:
                    return self.send_json(500, {"error": "FAILED_READ_FIXTURES", "message": str(e)})
            else:
                return self.send_json(404, {"error": "FIXTURES_NOT_FOUND", "message": "opportunity-hunter.fixtures.json not found"})

        # Profile API: GET
        if path == "/api/profile":
            try:
                prof = db.get_profile()
                return self.send_json(200, {"ok": True, "profile": prof})
            except Exception as e:
                return self.send_json(500, {"error": "DB_ERROR", "message": str(e)})

        # Application Tracker API: GET
        if path == "/api/applications":
            try:
                stage = query_params.get("stage", [None])[0]
                apps = db.list_applications(stage)
                return self.send_json(200, {"ok": True, "applications": apps, "total": len(apps)})
            except Exception as e:
                return self.send_json(500, {"error": "DB_ERROR", "message": str(e)})

        # Saved Opportunities API: GET
        if path == "/api/saved":
            try:
                saved = db.list_saved()
                return self.send_json(200, {"ok": True, "saved": saved, "total": len(saved)})
            except Exception as e:
                return self.send_json(500, {"error": "DB_ERROR", "message": str(e)})

        # Analytics API: GET
        if path == "/api/analytics":
            try:
                stats = db.get_analytics()
                return self.send_json(200, {"ok": True, "analytics": stats})
            except Exception as e:
                return self.send_json(500, {"error": "DB_ERROR", "message": str(e)})

        # Activity Log API: GET
        if path == "/api/activity":
            try:
                limit = int(query_params.get("limit", [15])[0])
                logs = db.get_activity_log(limit)
                return self.send_json(200, {"ok": True, "activity": logs})
            except Exception as e:
                return self.send_json(500, {"error": "DB_ERROR", "message": str(e)})

        # Serve static files (HTML, JSON, CSS, images)
        return super().do_GET()

    def do_POST(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path

        # Read and validate POST body
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 2 * 1024 * 1024:  # 2MB cap
            return self.send_json(413, {"error": "PAYLOAD_TOO_LARGE", "message": "Request body exceeds 2MB limit."})
        
        body_bytes = self.rfile.read(content_length)
        try:
            body = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
        except Exception:
            return self.send_json(400, {"error": "INVALID_JSON", "message": "Malformed JSON body."})

        api_key = os.environ.get("TINYFISH_API_KEY", "").strip()
        has_key = bool(api_key and api_key != "your_tinyfish_api_key_here")

        # TinyFish Search Proxy
        if path == "/api/search":
            if not has_key:
                return self.send_json(401, {
                    "error": "MISSING_API_KEY",
                    "message": "TINYFISH_API_KEY is not configured in .env. Open .env, add your key, and restart server."
                })
            return self.handle_tinyfish_search(body, api_key)

        # TinyFish Fetch Proxy
        elif path == "/api/fetch":
            if not has_key:
                return self.send_json(401, {
                    "error": "MISSING_API_KEY",
                    "message": "TINYFISH_API_KEY is not configured in .env. Open .env, add your key, and restart server."
                })
            return self.handle_tinyfish_fetch(body, api_key)

        # Profile API: POST
        elif path == "/api/profile":
            try:
                updated_profile = db.save_profile(body)
                return self.send_json(200, {"ok": True, "profile": updated_profile})
            except Exception as e:
                return self.send_json(500, {"error": "DB_ERROR", "message": str(e)})

        # Application Tracker API: POST (create or update)
        elif path == "/api/applications":
            try:
                saved_app = db.save_application(body)
                return self.send_json(200, {"ok": True, "application": saved_app})
            except Exception as e:
                return self.send_json(500, {"error": "DB_ERROR", "message": str(e)})

        # Saved Opportunities API: POST
        elif path == "/api/saved":
            try:
                saved_item = db.save_opportunity_item(body)
                return self.send_json(200, {"ok": True, "saved": saved_item})
            except Exception as e:
                return self.send_json(500, {"error": "DB_ERROR", "message": str(e)})

        # Resume Analyzer API: POST
        elif path == "/api/resume/parse":
            try:
                resume_text = body.get("text", "")
                opportunities = body.get("opportunities", [])
                analysis = intelligence.parse_resume_text(resume_text, opportunities)
                return self.send_json(200, {"ok": True, "analysis": analysis})
            except Exception as e:
                return self.send_json(500, {"error": "RESUME_PARSE_ERROR", "message": str(e)})

        # Career Assistant API: POST
        elif path == "/api/assistant":
            try:
                user_query = body.get("query", "")
                profile = body.get("profile") or db.get_profile()
                opportunities = body.get("opportunities", [])
                applications = body.get("applications", [])
                reply = intelligence.generate_assistant_reply(user_query, profile, opportunities, applications)
                return self.send_json(200, {"ok": True, "reply": reply})
            except Exception as e:
                return self.send_json(500, {"error": "ASSISTANT_ERROR", "message": str(e)})

        # Application Delete via POST fallback
        elif path == "/api/applications/delete":
            app_id = body.get("id")
            if not app_id:
                return self.send_json(400, {"error": "MISSING_ID", "message": "id is required."})
            success = db.delete_application(app_id)
            return self.send_json(200, {"ok": True, "deleted": success})

        # Saved Delete via POST fallback
        elif path == "/api/saved/delete":
            opp_id = body.get("id")
            if not opp_id:
                return self.send_json(400, {"error": "MISSING_ID", "message": "id is required."})
            success = db.delete_saved_opportunity(opp_id)
            return self.send_json(200, {"ok": True, "deleted": success})

        else:
            return self.send_json(404, {"error": "NOT_FOUND", "message": f"Endpoint {path} not found."})

    def do_DELETE(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path
        query_params = urllib.parse.parse_qs(url_parts.query)

        # Read potential body
        content_length = int(self.headers.get("Content-Length", 0))
        body = {}
        if content_length > 0:
            try:
                body = json.loads(self.rfile.read(content_length).decode("utf-8"))
            except Exception:
                pass

        if path == "/api/applications":
            app_id = query_params.get("id", [None])[0] or body.get("id")
            if not app_id:
                return self.send_json(400, {"error": "MISSING_ID", "message": "id query param or body field is required."})
            success = db.delete_application(app_id)
            return self.send_json(200, {"ok": True, "deleted": success})

        elif path == "/api/saved":
            opp_id = query_params.get("id", [None])[0] or body.get("id")
            if not opp_id:
                return self.send_json(400, {"error": "MISSING_ID", "message": "id query param or body field is required."})
            success = db.delete_saved_opportunity(opp_id)
            return self.send_json(200, {"ok": True, "deleted": success})

        else:
            return self.send_json(404, {"error": "NOT_FOUND", "message": f"Endpoint {path} not found."})

    def handle_tinyfish_search(self, body, api_key):
        query = body.get("query", "").strip()
        if not query:
            return self.send_json(400, {"error": "MISSING_QUERY", "message": "query parameter is required."})

        params = {"query": query}
        if "purpose" in body:
            params["purpose"] = body["purpose"]
        if "exclude_domains" in body:
            params["exclude_domains"] = body["exclude_domains"]
        if "location" in body:
            params["location"] = body["location"]

        full_url = f"{TINYFISH_SEARCH_URL}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(
            full_url,
            headers={
                "X-API-Key": api_key,
                "User-Agent": "OpportunityHunter/2.0"
            },
            method="GET"
        )

        try:
            with urllib.request.urlopen(req, timeout=18) as response:
                status_code = response.getcode()
                raw_data = response.read().decode("utf-8")
                try:
                    data = json.loads(raw_data)
                except Exception:
                    data = {"raw": raw_data}
                return self.send_json(status_code, data)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            try:
                err_json = json.loads(err_body)
            except Exception:
                err_json = {"error": "UPSTREAM_ERROR", "message": err_body}
            return self.send_json(e.code, err_json)
        except urllib.error.URLError as e:
            return self.send_json(504, {
                "error": "NETWORK_TIMEOUT",
                "message": f"Could not reach TinyFish Search API: {e.reason}"
            })
        except Exception as e:
            return self.send_json(500, {
                "error": "INTERNAL_ERROR",
                "message": f"Internal proxy error: {str(e)}"
            })

    def handle_tinyfish_fetch(self, body, api_key):
        urls = body.get("urls", [])
        if not urls or not isinstance(urls, list):
            return self.send_json(400, {"error": "INVALID_URLS", "message": "urls array is required."})

        payload = {
            "urls": urls[:10],  # TinyFish max 10 URLs per request
            "format": body.get("format", "markdown"),
            "links": bool(body.get("links", True)),
            "image_links": bool(body.get("image_links", False)),
            "iframe_links": bool(body.get("iframe_links", False)),
            "per_url_timeout_ms": int(body.get("per_url_timeout_ms", 40000)),
            "purpose": body.get("purpose", "Extract deadline, eligibility and location for student opportunities")
        }

        req = urllib.request.Request(
            TINYFISH_FETCH_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
                "User-Agent": "OpportunityHunter/2.0"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=50) as response:
                status_code = response.getcode()
                raw_data = response.read().decode("utf-8")
                try:
                    data = json.loads(raw_data)
                except Exception:
                    data = {"raw": raw_data}
                return self.send_json(status_code, data)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            try:
                err_json = json.loads(err_body)
            except Exception:
                err_json = {"error": "UPSTREAM_ERROR", "message": err_body}
            return self.send_json(e.code, err_json)
        except urllib.error.URLError as e:
            return self.send_json(504, {
                "error": "NETWORK_TIMEOUT",
                "message": f"Could not reach TinyFish Fetch API: {e.reason}"
            })
        except Exception as e:
            return self.send_json(500, {
                "error": "INTERNAL_ERROR",
                "message": f"Internal proxy error: {str(e)}"
            })

    def send_json(self, status_code, data):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Clean logging format without leaking query params or sensitive tokens
        sys.stderr.write(f"[BACKEND] {self.address_string()} - {format % args}\n")

def main():
    print("=" * 60)
    print(" Opportunity Hunter 2.0 Backend Proxy & Platform Server ")
    print("=" * 60)
    api_key = os.environ.get("TINYFISH_API_KEY", "").strip()
    if api_key and api_key != "your_tinyfish_api_key_here":
        masked = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else "***"
        print(f"[STATUS] TinyFish API Key: Configured ({masked})")
        print("[STATUS] Mode: LIVE (TinyFish Web Search & Fetch active)")
    else:
        print("[STATUS] TinyFish API Key: NOT SET in .env")
        print("[STATUS] Mode: DEMO / FIXTURE FALLBACK (Verified program fixtures active)")
        print("         To enable live search, add your key to .env and restart.")

    print(f"[DATABASE] SQLite local storage initialized at: opportunity_hunter.db")
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, OpportunityHunterHandler)
    print(f"\n[SERVER] Running at: http://localhost:{PORT}")
    print(f"[SERVER] Open your browser at: http://localhost:{PORT}/opportunity-hunter.html")
    print("[SERVER] Press Ctrl+C to stop.\n" + "=" * 60)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        httpd.server_close()

if __name__ == "__main__":
    main()
