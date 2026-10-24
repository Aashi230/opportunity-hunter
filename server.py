#!/usr/bin/env python3
"""
Opportunity Hunter — Lightweight Backend Proxy for TinyFish API
Serves the web application and proxies Search and Fetch requests to TinyFish
without exposing API keys to the browser.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

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

class OpportunityHunterHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local testing
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path

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
                "has_api_key": has_key,
                "mode": "live" if has_key else "demo_fallback",
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

        # Serve static files (HTML, JSON, CSS, images)
        return super().do_GET()

    def do_POST(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path

        # Read POST body
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

        if path == "/api/search":
            if not has_key:
                return self.send_json(401, {
                    "error": "MISSING_API_KEY",
                    "message": "TINYFISH_API_KEY is not configured in .env. Open .env, add your key, and restart server."
                })
            return self.handle_tinyfish_search(body, api_key)

        elif path == "/api/fetch":
            if not has_key:
                return self.send_json(401, {
                    "error": "MISSING_API_KEY",
                    "message": "TINYFISH_API_KEY is not configured in .env. Open .env, add your key, and restart server."
                })
            return self.handle_tinyfish_fetch(body, api_key)

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
                "User-Agent": "OpportunityHunter/1.0"
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
                "User-Agent": "OpportunityHunter/1.0"
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
    print(" Opportunity Hunter Backend Proxy ")
    print("=" * 60)
    api_key = os.environ.get("TINYFISH_API_KEY", "").strip()
    if api_key and api_key != "your_tinyfish_api_key_here":
        masked = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else "***"
        print(f"[STATUS] TinyFish API Key: Configured ({masked})")
        print("[STATUS] Mode: LIVE (TinyFish Web Search & Fetch active)")
    else:
        print("[STATUS] TinyFish API Key: NOT SET in .env")
        print("[STATUS] Mode: DEMO / FIXTURE FALLBACK (Safe for hackathon preview)")
        print("         To enable live search, add your key to .env and restart.")

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
