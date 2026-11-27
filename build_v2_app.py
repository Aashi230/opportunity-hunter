#!/usr/bin/env python3
"""
Opportunity Hunter 2.0 — Platform Builder
Assembles Modern CSS Design System, HTML5 Layout, and Application Engine
into production-ready opportunity-hunter.html and index.html files.
"""

import os
from build_css import get_css
from build_html import get_html_body
from build_js import get_js

def build():
    css_content = get_css()
    html_body = get_html_body()
    js_content = get_js()

    full_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Opportunity Hunter 2.0 — Your Personal Career &amp; Opportunity Companion</title>
  <meta name="description" content="Discover verified student internships, scholarships, fellowships, and developer programs with explainable eligibility audits, Kanban tracking, and AI career guidance.">
  
  <!-- Modern Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
{css_content}
  </style>
</head>
<body>
{html_body}

  <script>
{js_content}
  </script>
</body>
</html>
"""

    # Write both opportunity-hunter.html and index.html
    base_dir = os.path.dirname(__file__)
    for filename in ["opportunity-hunter.html", "index.html"]:
        filepath = os.path.join(base_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"[BUILD SUCCESS] Generated: {filename} ({len(full_html)} bytes)")

if __name__ == "__main__":
    build()
