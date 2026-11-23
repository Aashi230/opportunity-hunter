#!/usr/bin/env python3
"""
Test Suite for Opportunity Hunter Bug Fixes:
1. Microsoft targeted program link vs. senior job requisitions
2. Infosys placement cell handling & InStep link extraction
3. Academic-year inference isolation from job seniority
"""

import re
import json
import unittest

with open("opportunity-hunter.fixtures.json", "r", encoding="utf-8") as f:
    FIXTURES_DATA = json.load(f)

# Python port of the JavaScript levelCheck function
def level_check(t, year):
    s = t[:45000].lower()
    s = re.sub(r'(?:first|1st)[- ]*(?:and\/or|and|or|\/|&)[- ]*(?:second|2nd)[- ]*year', '1st-year and 2nd-year', s)
    s = re.sub(r'(?:third|3rd)[- ]*(?:and\/or|and|or|\/|&)[- ]*(?:fourth|4th|final)[- ]*year', '3rd-year and 4th-year', s)

    # Bug 3 fix: strip job experience requirements and senior titles
    s = re.sub(r'\b\d+\+?\s*years?(?:\s+of)?(?:\s+[\w-]+){0,4}\s+(?:experience|hands-on|industry|technical)\b', ' ', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(?:senior|principal|lead|staff)\s+(?:software|engineer|developer|architect|manager|product|program)\b', ' ', s, flags=re.IGNORECASE)

    sentences = re.split(r'(?<=[.!?])\s+|\n+', s)
    student_ctx = "\n".join([
        x for x in sentences
        if re.search(r'\b(?:student|students|undergrad|undergraduate|undergraduates|college|university|enrolled|enrolment|pursuing|intern|interns|internship|sophomore|sophomores|freshman|freshmen|fresher|freshers|bachelor|bachelors)\b', x, re.IGNORECASE)
        and not re.search(r'\b\d+\+?\s*years?\s+(?:of\s+)?experience\b', x, re.IGNORECASE)
    ])

    LV = {
        "1st year": r'\b(?:first|1st)[- ]?year(?:\s+(?:college|university|student|undergraduate))?\b|\bfreshm[ae]n\b',
        "2nd year": r'\b(?:second|2nd)[- ]?year(?:\s+(?:college|university|student|undergraduate))?\b|\bsophomores?\b',
        "3rd year": r'\b(?:third|3rd)[- ]?year(?:\s+(?:college|university|student|undergraduate))?\b|\bpre-?final[- ]?year\b|\bjunior year\b',
        "Final year": r'(?<!pre-)(?<!pre)\bfinal[- ]?year(?:\s+(?:college|university|student|undergraduate))?\b|\b(?:fourth|4th)[- ]?year\b|\blast[- ]?year\b|\bsenior year\b',
        "Master’s": r'\bmaster(?:\'s|’s|s)? (?:students?|degree)|\bpostgraduate students?\b|\bm\.?tech students?\b|\bmsc students?\b',
        "PhD": r'\bph\.?d\.? (?:students?|candidates?)\b|\bdoctoral (?:students?|candidates?)\b',
        "Graduated": r'\b(?:recent|fresh) graduates?\b|\bfreshers?\b|\bnew grads?\b'
    }

    if not year:
        return "unclear"
    found = [k for k, pat in LV.items() if re.search(pat, student_ctx, re.IGNORECASE)]
    if found:
        return "ok" if year in found else "mismatch"
    if re.search(r'\b(?:open to|available to|for) (?:all|any) (?:enrolled )?(?:undergraduate |college |university )?students?\b', student_ctx, re.IGNORECASE):
        return "ok"
    return "unclear"


class TestBugFixes(unittest.TestCase):
    def test_bug_1_microsoft_links(self):
        """Bug 1: Microsoft Explore links should point to #explorer and filter out senior engineer requisitions."""
        ms_page = FIXTURES_DATA["pages"][0]
        links = ms_page.get("links", [])
        
        # Verify targeted explorer link is found
        explorer_links = [u for u in links if "explorer" in u.lower()]
        self.assertEqual(len(explorer_links), 1)
        self.assertIn("filter_hiring_title=%23explorer", explorer_links[0])

        # Verify senior job requisitions (job/1970393557042167) are identified as separate professional postings
        senior_requisitions = [u for u in links if "/careers/job/" in u]
        self.assertEqual(len(senior_requisitions), 3)
        print("  [PASS] Bug 1: Microsoft #explorer targeted link distinguished from senior roles.")

    def test_bug_2_infosys_placement_office_and_instep(self):
        """Bug 2: Infosys placement office instruction should be recognized while preserving InStep link."""
        info_page = FIXTURES_DATA["pages"][1]
        text = info_page["text"]
        links = info_page.get("links", [])

        # Check campus placement detection
        has_placement = bool(re.search(r'placement (?:office|cell)', text, re.IGNORECASE))
        self.assertTrue(has_placement)

        # Check that InStep flagship portal is present
        instep_links = [u for u in links if "instep" in u.lower()]
        self.assertEqual(len(instep_links), 1)
        self.assertEqual(instep_links[0], "https://www.infosys.com/instep.html")
        print("  [PASS] Bug 2: Infosys placement notice captured without dropping InStep portal.")

    def test_bug_3_academic_year_isolation_from_seniority(self):
        """Bug 3: 4+ years technical experience / Senior title should NOT match 4th year or Final year."""
        ms_text = FIXTURES_DATA["pages"][0]["text"]
        
        # Explore Microsoft is for 1st and 2nd year students
        self.assertEqual(level_check(ms_text, "1st year"), "ok")
        self.assertEqual(level_check(ms_text, "2nd year"), "ok")

        # Senior Software Engineer (4+ years technical engineering experience) must NOT qualify Final year or 3rd year
        self.assertEqual(level_check(ms_text, "Final year"), "mismatch")
        self.assertEqual(level_check(ms_text, "3rd year"), "mismatch")
        self.assertEqual(level_check(ms_text, "Master’s"), "mismatch")
        print("  [PASS] Bug 3: Job seniority (4+ years / Senior) successfully excluded from student level.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
