#!/usr/bin/env python3
"""
Opportunity Hunter 2.0 — Feature & API Integration Test Suite
Validates SQLite persistence, Application Tracker (Kanban), Profile Management,
Saved Opportunities, Resume Analyzer, and Contextual Career Assistant.
"""

import os
import sys
import json
import io
import unittest

from server import OpportunityHunterHandler
import db
import intelligence

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

class TestOpportunityHunterV2Features(unittest.TestCase):
    def run_request(self, method, path, headers=None, body=None):
        req_lines = [f"{method} {path} HTTP/1.1", "Host: localhost"]
        if headers:
            for k, v in headers.items():
                req_lines.append(f"{k}: {v}")
        body_bytes = b""
        if body is not None:
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

        # Invoke request handler
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

    def test_01_profile_crud(self):
        """Verify profile GET and POST endpoints persist student profile."""
        code, _, _, body = self.run_request("GET", "/api/profile")
        self.assertEqual(code, 200)
        self.assertTrue(body.get("ok"))
        self.assertIn("profile", body)

        # Update Profile
        update_data = {
            "name": "Aashi Srivastava",
            "degree": "B.Tech Computer Science",
            "year": "2nd year",
            "graduation_year": "2027",
            "skills": ["Python", "SQL", "React", "Docker"],
            "location": "India",
            "opportunity_type": "internship",
            "work_mode": "remote",
            "interests": "Software Engineering"
        }
        code, _, _, updated = self.run_request("POST", "/api/profile", body=update_data)
        self.assertEqual(code, 200)
        self.assertTrue(updated.get("ok"))
        prof = updated["profile"]
        self.assertEqual(prof["name"], "Aashi Srivastava")
        self.assertEqual(prof["degree"], "B.Tech Computer Science")
        self.assertIn("Python", prof["skills"])
        print("  [PASS] Test 1: Student profile persistence verified.")

    def test_02_application_tracker_crud(self):
        """Verify Kanban applications CRUD with full lifecycle stages."""
        app_id = "test-app-ms-123"
        new_app = {
            "id": app_id,
            "title": "Explore Microsoft Internship",
            "organization": "Microsoft",
            "url": "https://careers.microsoft.com/v2/global/en/exploremicrosoft",
            "stage": "interested",
            "notes": "Looking forward to engineering foundations track",
            "deadline": "2026-11-30"
        }
        # Create
        code, _, _, resp = self.run_request("POST", "/api/applications", body=new_app)
        self.assertEqual(code, 200)
        self.assertTrue(resp.get("ok"))
        self.assertEqual(resp["application"]["stage"], "interested")

        # List
        code, _, _, list_resp = self.run_request("GET", "/api/applications")
        self.assertEqual(code, 200)
        items = [a for a in list_resp.get("applications", []) if a["id"] == app_id]
        self.assertEqual(len(items), 1)

        # Update stage to 'interviewing'
        new_app["stage"] = "interviewing"
        new_app["interview_date"] = "2026-12-05"
        code, _, _, update_resp = self.run_request("POST", "/api/applications", body=new_app)
        self.assertEqual(code, 200)
        self.assertEqual(update_resp["application"]["stage"], "interviewing")

        # Delete
        code, _, _, del_resp = self.run_request("DELETE", f"/api/applications?id={app_id}")
        self.assertEqual(code, 200)
        self.assertTrue(del_resp.get("ok"))
        print("  [PASS] Test 2: Application Tracker (Kanban) CRUD verified.")

    def test_03_saved_opportunities_crud(self):
        """Verify saved opportunities storage and deletion."""
        opp_id = "test-saved-ibm-456"
        item = {
            "id": opp_id,
            "title": "IBM Global Student Internships",
            "organization": "IBM",
            "url": "https://www.ibm.com/in-en/careers/internships"
        }
        # Save
        code, _, _, resp = self.run_request("POST", "/api/saved", body=item)
        self.assertEqual(code, 200)
        self.assertTrue(resp.get("ok"))

        # List
        code, _, _, list_resp = self.run_request("GET", "/api/saved")
        self.assertEqual(code, 200)
        found = [s for s in list_resp.get("saved", []) if s["id"] == opp_id]
        self.assertEqual(len(found), 1)

        # Delete
        code, _, _, del_resp = self.run_request("DELETE", f"/api/saved?id={opp_id}")
        self.assertEqual(code, 200)
        self.assertTrue(del_resp.get("ok"))
        print("  [PASS] Test 3: Saved opportunities CRUD verified.")

    def test_04_analytics_endpoint(self):
        """Verify analytics endpoint computes real database metrics."""
        code, _, _, resp = self.run_request("GET", "/api/analytics")
        self.assertEqual(code, 200)
        self.assertTrue(resp.get("ok"))
        analytics = resp.get("analytics", {})
        self.assertIn("total_applications", analytics)
        self.assertIn("total_saved", analytics)
        self.assertIn("stage_breakdown", analytics)
        print("  [PASS] Test 4: Dynamic dashboard analytics verified.")

    def test_05_resume_parser_endpoint(self):
        """Verify resume text analysis and skill extraction."""
        resume_sample = """
        Aashi Srivastava
        Email: aashi@example.com | GitHub: github.com/Aashi230 | LinkedIn: linkedin.com/in/aashi
        B.Tech Computer Science Engineering - Class of 2027
        Skills: Python, React, JavaScript, SQL, Docker, Git, Machine Learning, Data Analysis
        Projects:
        - Opportunity Hunter Platform: Engineered full-stack career discovery platform serving 1,000+ student queries with 40% faster latency.
        - AI Resume Analyzer: Implemented rule-based skill extraction tool with 95% accuracy.
        """
        payload = {
            "text": resume_sample,
            "opportunities": [
                {"title": "Explore Microsoft", "text": "Requires Python, C++, and basic coding in college."},
                {"title": "IBM SkillsBuild", "text": "Requires Python, Git, and Linux cloud fundamentals."}
            ]
        }
        code, _, _, resp = self.run_request("POST", "/api/resume/parse", body=payload)
        self.assertEqual(code, 200)
        self.assertTrue(resp.get("ok"))
        analysis = resp["analysis"]
        self.assertIn("Python", analysis["extracted_skills"])
        self.assertIn("Docker", analysis["extracted_skills"])
        self.assertIn("React", analysis["extracted_skills"])
        self.assertTrue(analysis["has_github"])
        self.assertGreaterEqual(analysis["strength_score"], 60)
        self.assertGreaterEqual(len(analysis["recommended_opportunities"]), 1)
        print("  [PASS] Test 5: Resume Analyzer extraction & scoring verified.")

    def test_06_career_assistant_endpoint(self):
        """Verify career assistant responds with grounded contextual guidance."""
        payload = {
            "query": "Am I eligible for Microsoft Explore as a 2nd year student?",
            "profile": {
                "name": "Aashi",
                "degree": "B.Tech CSE",
                "year": "2nd year",
                "skills": ["Python", "C++", "SQL"]
            }
        }
        code, _, _, resp = self.run_request("POST", "/api/assistant", body=payload)
        self.assertEqual(code, 200)
        self.assertTrue(resp.get("ok"))
        reply = resp["reply"]
        self.assertIn("eligible", reply.lower())
        self.assertIn("explore microsoft", reply.lower())
        print("  [PASS] Test 6: Career Assistant contextual reasoning verified.")

    def test_07_activity_log_endpoint(self):
        """Verify activity log recording and retrieval."""
        code, _, _, resp = self.run_request("GET", "/api/activity")
        self.assertEqual(code, 200)
        self.assertTrue(resp.get("ok"))
        self.assertIsInstance(resp.get("activity"), list)
        print("  [PASS] Test 7: Activity log logging verified.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
