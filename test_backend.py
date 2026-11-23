#!/usr/bin/env python3
"""
Automated Unit & Integration Tests for Opportunity Hunter Backend
Tests endpoints, CORS headers, security handling, and offline fallback
without requiring external network permissions or port binding.
"""

import os
import sys
import json
import io
import unittest

from server import OpportunityHunterHandler

class MockSocket:
    def __init__(self, request_bytes):
        self.request_bytes = request_bytes
        self.response_bytes = bytearray()

    def makefile(self, mode, *args, **kwargs):
        if "r" in mode:
            return io.BytesIO(self.request_bytes)
        return self

    def sendall(self, data):
        self.response_bytes.extend(data)

    def write(self, data):
        self.response_bytes.extend(data)

    def flush(self):
        pass


class TestOpportunityHunterBackend(unittest.TestCase):
    def run_request(self, method, path, headers=None, body=None, env=None):
        if env is not None:
            old_env = dict(os.environ)
            os.environ.clear()
            os.environ.update(env)
        else:
            old_env = None

        try:
            req_lines = [f"{method} {path} HTTP/1.1", "Host: localhost"]
            if headers:
                for k, v in headers.items():
                    req_lines.append(f"{k}: {v}")
            body_bytes = b""
            if body:
                if isinstance(body, dict):
                    body_bytes = json.dumps(body).encode("utf-8")
                elif isinstance(body, str):
                    body_bytes = body.encode("utf-8")
                else:
                    body_bytes = body
                req_lines.append(f"Content-Length: {len(body_bytes)}")
                req_lines.append("Content-Type: application/json")

            req_raw = "\r\n".join(req_lines).encode("utf-8") + b"\r\n\r\n" + body_bytes
            sock = MockSocket(req_raw)

            # Invoke handler
            handler = OpportunityHunterHandler(sock, ("127.0.0.1", 12345), None)
            response_raw = sock.response_bytes.decode("utf-8", errors="replace")

            # Parse HTTP response
            parts = response_raw.split("\r\n\r\n", 1)
            header_lines = parts[0].split("\r\n")
            status_line = header_lines[0]
            status_code = int(status_line.split(" ")[1])

            resp_headers = {}
            for line in header_lines[1:]:
                if ": " in line:
                    hk, hv = line.split(": ", 1)
                    resp_headers[hk.lower()] = hv

            resp_body = parts[1] if len(parts) > 1 else ""
            json_body = None
            if "application/json" in resp_headers.get("content-type", ""):
                try:
                    json_body = json.loads(resp_body)
                except Exception:
                    pass

            return status_code, resp_headers, resp_body, json_body
        finally:
            if old_env is not None:
                os.environ.clear()
                os.environ.update(old_env)

    def test_01_health_and_status(self):
        """Verify /api/status returns valid JSON and correct mode."""
        status_code, headers, _, json_body = self.run_request(
            "GET", "/api/status", env={"TINYFISH_API_KEY": ""}
        )
        self.assertEqual(status_code, 200)
        self.assertIn("application/json", headers.get("content-type", ""))
        self.assertIsNotNone(json_body)
        self.assertTrue(json_body.get("ok"))
        self.assertFalse(json_body.get("has_api_key"))
        self.assertEqual(json_body.get("mode"), "demo_fallback")
        self.assertEqual(headers.get("access-control-allow-origin"), "*")
        print("  [PASS] /api/status in demo mode verified.")

    def test_02_status_with_api_key(self):
        """Verify /api/status detects configured API key without leaking it."""
        status_code, _, _, json_body = self.run_request(
            "GET", "/api/status", env={"TINYFISH_API_KEY": "tf_live_test_secret_12345"}
        )
        self.assertEqual(status_code, 200)
        self.assertTrue(json_body.get("has_api_key"))
        self.assertEqual(json_body.get("mode"), "live")
        # Ensure secret is NOT in output
        self.assertNotIn("tf_live_test_secret_12345", json.dumps(json_body))
        print("  [PASS] /api/status in live mode verified (secrets protected).")

    def test_03_fixtures_endpoint(self):
        """Verify /api/fixtures serves verified program fixtures."""
        status_code, headers, _, json_body = self.run_request("GET", "/api/fixtures")
        self.assertEqual(status_code, 200)
        self.assertIsNotNone(json_body)
        self.assertIn("pages", json_body)
        self.assertGreaterEqual(len(json_body["pages"]), 3)
        print("  [PASS] /api/fixtures successfully returned", len(json_body["pages"]), "pages.")

    def test_04_search_without_key_blocks_cleanly(self):
        """Verify /api/search rejects requests without API key with 401 and clean message."""
        status_code, _, _, json_body = self.run_request(
            "POST",
            "/api/search",
            body={"query": "Software Engineering Internship"},
            env={"TINYFISH_API_KEY": ""}
        )
        self.assertEqual(status_code, 401)
        self.assertIsNotNone(json_body)
        self.assertEqual(json_body.get("error"), "MISSING_API_KEY")
        print("  [PASS] /api/search safely blocked missing credentials.")

    def test_05_fetch_without_key_blocks_cleanly(self):
        """Verify /api/fetch rejects requests without API key with 401 and clean message."""
        status_code, _, _, json_body = self.run_request(
            "POST",
            "/api/fetch",
            body={"urls": ["https://careers.microsoft.com"]},
            env={"TINYFISH_API_KEY": ""}
        )
        self.assertEqual(status_code, 401)
        self.assertIsNotNone(json_body)
        self.assertEqual(json_body.get("error"), "MISSING_API_KEY")
        print("  [PASS] /api/fetch safely blocked missing credentials.")

    def test_06_cors_preflight(self):
        """Verify CORS preflight (OPTIONS) returns 204 with required headers."""
        status_code, headers, _, _ = self.run_request("OPTIONS", "/api/search")
        self.assertEqual(status_code, 204)
        self.assertEqual(headers.get("access-control-allow-origin"), "*")
        self.assertIn("POST", headers.get("access-control-allow-methods", ""))
        print("  [PASS] CORS OPTIONS preflight verified.")

    def test_07_static_file_routing(self):
        """Verify root path routes to opportunity-hunter.html."""
        status_code, headers, body, _ = self.run_request("GET", "/")
        self.assertEqual(status_code, 200)
        self.assertIn("Opportunity Hunter", body)
        print("  [PASS] Static routing for opportunity-hunter.html verified.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
