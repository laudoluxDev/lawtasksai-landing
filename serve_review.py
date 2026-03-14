#!/usr/bin/env python3
"""
LawTasksAI Landing — Security Docs Review Server
Run: python3 serve_review.py
Opens at: http://localhost:8099
"""

import http.server
import socketserver
import os
import html as html_lib

PORT = 8099
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

NEW_FILES = [
    ("client-matter-isolation-procedures.html", "Client Matter Isolation Procedures"),
    ("macmini-security-checklist.html", "Mac Mini Security Checklist"),
    ("macmini-startup-guide.html", "Mac Mini Startup Guide"),
    ("openclaw-mac-vs-windows.html", "OpenClaw: Mac vs Windows"),
    ("openclaw-security-reference.html", "OpenClaw Security Reference"),
    ("openclaw-windows-install.html", "OpenClaw + Ollama on Windows"),
    ("secure-communications-reference.html", "Secure Communications Reference"),
    ("vps-security-hardening-manual.html", "VPS Security Hardening Manual"),
    ("aba-ethics-guidance-ai.html", "ABA Ethics Guidance on AI Tools"),
    ("aba-formal-opinion-512.html", "ABA Formal Opinion 512"),
    ("openclaw-security-guide-FULL.html", "OpenClaw Security Guide (FULL — replaces placeholder)"),
]

EXISTING_SECURITY = [
    ("law-firm-claude-security-guide.html", "Law Firm Claude Security Guide"),
    ("uploading-files-to-anthropic-zdr-guide.html", "Uploading Files to Anthropic ZDR Guide"),
    ("zdr-aba-compliance-guide.html", "ZDR ABA Compliance Guide"),
    ("openclaw-security-guide.html", "OpenClaw Security Guide (current placeholder — Coming Soon)"),
]

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>LawTasksAI — Security Docs Review</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         background: #f5f0e8; color: #1a1a2e; max-width: 860px;
         margin: 0 auto; padding: 3rem 2rem; }}
  h1 {{ font-size: 1.8rem; border-bottom: 3px solid #b8860b; padding-bottom: 0.5rem; }}
  h2 {{ font-size: 1.2rem; color: #1a5c3a; margin-top: 2rem; }}
  .badge {{ display: inline-block; font-size: 0.7rem; font-weight: bold;
            padding: 2px 8px; border-radius: 99px; margin-left: 8px;
            vertical-align: middle; }}
  .new  {{ background: #d4edda; color: #155724; }}
  .ok   {{ background: #cce5ff; color: #004085; }}
  .warn {{ background: #fff3cd; color: #856404; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ margin: 0.5rem 0; }}
  a {{ color: #1a1a2e; text-decoration: none; font-size: 1rem; }}
  a:hover {{ text-decoration: underline; color: #b8860b; }}
  .note {{ background: #fff3cd; border-left: 4px solid #b8860b;
           padding: 1rem 1.2rem; margin: 1.5rem 0; font-size: 0.9rem; }}
</style>
</head>
<body>
<h1>🏛️ LawTasksAI — Security Docs Review</h1>
<div class="note">
  <strong>Review checklist:</strong> The <span class="badge new">NEW</span> files were generated
  from source .docx/.pdf files. The <span class="badge warn">NEEDS REVIEW</span> file is the
  full Security folder version of the OpenClaw Security Guide — the landing repo currently has
  only a "Coming Soon" placeholder. Decide whether to replace it.
</div>

<h2>Newly Generated HTML Files</h2>
<ul>
{new_links}
</ul>

<h2>Existing Landing Repo Security Files (content verified ✅)</h2>
<ul>
{existing_links}
</ul>

<h2>All HTML Files in Repo</h2>
<ul>
{all_links}
</ul>
</body>
</html>"""


def build_index():
    new_links = "\n".join(
        f'  <li><a href="/{f}" target="_blank">{label}</a>'
        f'  <span class="badge {"warn" if "FULL" in f else "new"}">{"NEEDS REVIEW" if "FULL" in f else "NEW"}</span></li>'
        for f, label in NEW_FILES
        if os.path.exists(os.path.join(DIRECTORY, f))
    )
    existing_links = "\n".join(
        f'  <li><a href="/{f}" target="_blank">{label}</a>'
        f'  <span class="badge ok">OK</span></li>'
        for f, label in EXISTING_SECURITY
        if os.path.exists(os.path.join(DIRECTORY, f))
    )
    all_html = sorted(
        f for f in os.listdir(DIRECTORY)
        if f.endswith('.html') and f != 'index.html'
    )
    all_links = "\n".join(
        f'  <li><a href="/{f}" target="_blank">{html_lib.escape(f)}</a></li>'
        for f in all_html
    )
    return INDEX_HTML.format(
        new_links=new_links,
        existing_links=existing_links,
        all_links=all_links,
    )


class ReviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            content = build_index().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        pass  # suppress access log noise


if __name__ == '__main__':
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(('', PORT), ReviewHandler) as httpd:
        print(f'\n🏛️  LawTasksAI Security Docs Review Server')
        print(f'   URL: http://localhost:{PORT}')
        print(f'   Dir: {DIRECTORY}')
        print(f'\n   Press Ctrl+C to stop.\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nStopped.')
