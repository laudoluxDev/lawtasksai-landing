#!/usr/bin/env python3
"""
LawTasksAI landing site refactor script.
- Injects <link rel="stylesheet" href="/shared.css"> into every HTML <head>
- Replaces each page's nav header with the canonical shared header
- Replaces each page's footer with the canonical shared footer
- Injects shared nav JS if not already present
"""

import re
import os
import glob

REPO = os.path.dirname(os.path.abspath(__file__))

# ─── Canonical HTML snippets ───────────────────────────────────────────────

SHARED_CSS_TAG = '<link rel="stylesheet" href="/shared.css">'

SHARED_HEADER = """\
<header>
  <div class="container">
    <div class="header-inner">
      <a href="/index.html" class="logo">LawTasks<span>AI</span></a>
      <nav class="nav-links" id="navLinks">
        <a href="/task-library.html">Task Library</a>
        <a href="/sample.html">Samples</a>
        <a href="/vs-chatgpt.html">vs ChatGPT</a>
        <div class="dropdown">
          <span class="dropdown-toggle">ABA 1.6</span>
          <div class="dropdown-menu">
            <a href="/security.html">Rule 1.6 &amp; Security</a>
            <a href="/law-firm-claude-security-guide.html">Law Firm Claude Security Guide</a>
            <a href="/zdr-aba-compliance-guide.html">ZDR ABA Compliance Guide</a>
            <a href="/aba-formal-opinion-512.html">ABA Formal Opinion 512</a>
            <a href="/aba-ethics-guidance-ai.html">ABA Ethics Guidance on AI</a>
          </div>
        </div>
        <div class="dropdown">
          <span class="dropdown-toggle">Support</span>
          <div class="dropdown-menu">
            <a href="/index.html#faq">FAQ</a>
            <a href="/getting-started.html">Getting Started</a>
            <a href="/download.html">Download</a>
            <a href="/terms.html">Terms of Service</a>
            <a href="/privacy.html">Privacy Policy</a>
          </div>
        </div>
        <a href="/signup" class="header-cta">Try Free &rarr;</a>
      </nav>
      <button class="hamburger" id="hamburger" aria-label="Open menu">
        <span></span><span></span><span></span>
      </button>
      <div class="mobile-overlay" id="overlay"></div>
    </div>
  </div>
</header>"""

SHARED_FOOTER = """\
<footer class="site-footer-shared">
  <div class="container">
    <div class="footer-disclaimer">
      <span class="disclaimer-label">&#9888; Not Legal Advice</span>
      <span>LawTasksAI is software that assists attorneys and paralegals with legal research and drafting. It is not a law firm and does not provide legal advice. Always apply your own professional review and judgment to any output.</span>
    </div>
    <div class="footer-inner">
      <div class="footer-brand">
        <a href="/index.html" class="logo">LawTasks<span>AI</span></a>
        <p>AI-powered legal workflows for attorneys and legal professionals.</p>
      </div>
      <div class="footer-links">
        <a href="/task-library.html">Task Library</a>
        <a href="/getting-started.html">Getting Started</a>
        <a href="/security.html">ABA Rule 1.6</a>
        <a href="/terms.html">Terms</a>
        <a href="/privacy.html">Privacy</a>
        <a href="mailto:hello@lawtasksai.com">hello@lawtasksai.com</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 LawTasksAI &nbsp;&middot;&nbsp; <a href="/terms.html">Terms</a> &nbsp;&middot;&nbsp; <a href="/privacy.html">Privacy</a> &nbsp;&middot;&nbsp; <a href="mailto:hello@lawtasksai.com">hello@lawtasksai.com</a></p>
    </div>
  </div>
</footer>"""

# Mobile nav JS — injected before </body> if not already present
SHARED_NAV_JS = """\
<script>
(function() {
  // ---- Shared mobile nav ----
  var hamburger = document.getElementById('hamburger');
  var navLinks  = document.getElementById('navLinks');
  var overlay   = document.getElementById('overlay');
  if (!hamburger || !navLinks || !overlay) return;

  function toggleNav() {
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('active');
    overlay.classList.toggle('active');
  }
  hamburger.addEventListener('click', toggleNav);
  overlay.addEventListener('click', toggleNav);
  navLinks.querySelectorAll('a').forEach(function(a) {
    a.addEventListener('click', function() {
      if (navLinks.classList.contains('active')) toggleNav();
    });
  });

  // Mobile dropdown tap
  document.querySelectorAll('.dropdown-toggle').forEach(function(t) {
    t.addEventListener('click', function(e) {
      if (window.innerWidth <= 768) {
        e.stopPropagation();
        this.parentElement.classList.toggle('mobile-open');
      }
    });
  });
  if (window.innerWidth > 768) {
    document.querySelectorAll('.dropdown').forEach(function(d) {
      d.addEventListener('mouseenter', function() {
        var m = d.querySelector('.dropdown-menu');
        if (m) m.style.display = 'block';
      });
      d.addEventListener('mouseleave', function() {
        var m = d.querySelector('.dropdown-menu');
        if (m) m.style.display = '';
      });
    });
  }
})();
</script>"""

# ─── Helpers ───────────────────────────────────────────────────────────────

def inject_shared_css(html):
    """Add /shared.css link to <head> if not already present."""
    if '/shared.css' in html:
        return html
    # Insert before first <link rel="stylesheet"> or before </head>
    if '<link rel="stylesheet"' in html:
        html = html.replace('<link rel="stylesheet"',
                            SHARED_CSS_TAG + '\n    <link rel="stylesheet"', 1)
    elif '</head>' in html:
        html = html.replace('</head>', '    ' + SHARED_CSS_TAG + '\n</head>', 1)
    return html


def find_header_end(html, start):
    """
    Given the position of an opening <header...> tag in html,
    find the position just after the matching </header>.
    Returns None if not found.
    """
    # Skip past the opening tag itself
    open_tag_end = html.index('>', start) + 1
    pos = open_tag_end
    depth = 0  # 0 means we're inside the target header

    while pos < len(html):
        # Find next <header (opening) and </header> from current pos
        next_open = re.search(r'<header\b', html[pos:], re.IGNORECASE)
        next_close = re.search(r'</header\s*>', html[pos:], re.IGNORECASE)

        if next_close is None:
            return None  # malformed HTML

        open_pos = (pos + next_open.start()) if next_open else None
        close_pos = pos + next_close.start()
        close_end = pos + next_close.end()

        if open_pos is not None and open_pos < close_pos:
            # Nested header opens before this close
            depth += 1
            pos = open_pos + len(next_open.group(0))
        else:
            # Close comes first (or no more opens)
            if depth == 0:
                return close_end
            else:
                depth -= 1
                pos = close_end

    return None


def replace_nav_header(html, filename):
    """
    Replace the site-nav <header> (plain <header> or <header class="main-header">)
    with the shared header.
    Leaves document-specific headers (class="site-header", class="masthead") alone.
    For pages that have NO nav header at all, insert the shared header after <body>.
    """
    all_headers = list(re.finditer(r'<header(?:\s[^>]*)?>',html, re.IGNORECASE))

    nav_header_match = None
    for m in all_headers:
        tag = m.group(0).lower()
        # Skip document headers
        if 'site-header' in tag or 'masthead' in tag:
            continue
        nav_header_match = m
        break

    if nav_header_match is None:
        # No nav header found — inject shared header after <body> tag
        if re.search(r'<body\b', html, re.IGNORECASE):
            html = re.sub(r'(<body[^>]*>)', r'\1\n' + SHARED_HEADER, html, count=1, flags=re.IGNORECASE)
            print(f"  [insert] No nav header found — injected after <body>")
        else:
            print(f"  [skip]   No nav header and no <body> tag in {filename}")
        return html

    start = nav_header_match.start()
    end = find_header_end(html, start)
    if end is None:
        print(f"  [warn]   Could not find </header> in {filename}")
        return html

    html = html[:start] + SHARED_HEADER + html[end:]
    print(f"  [ok]     Replaced nav header ({nav_header_match.group(0)[:40]}…)")
    return html


def replace_footer(html, filename):
    """
    Replace the page <footer> with the shared footer.
    Skip class="site-footer" (document footers). Replace first bare <footer>.
    """
    # If already done, skip
    if 'site-footer-shared' in html:
        print(f"  [skip]   Already has site-footer-shared in {filename}")
        return html

    all_footers = list(re.finditer(r'<footer(?:\s[^>]*)?>',html, re.IGNORECASE))

    if not all_footers:
        print(f"  [skip]   No <footer> found in {filename}")
        return html

    # Choose which footer to replace — prefer bare <footer> or <footer class="">
    target_footer = None
    for fm in all_footers:
        tag = fm.group(0).lower()
        # Skip document-style footers (site-footer class but NOT site-footer-shared)
        if 'site-footer' in tag and 'site-footer-shared' not in tag:
            continue
        target_footer = fm
        break

    if target_footer is None:
        # Fall back to last footer
        target_footer = all_footers[-1]

    start = target_footer.start()
    close_m = re.search(r'</footer\s*>', html[start:], re.IGNORECASE)
    if close_m is None:
        print(f"  [warn]   Could not find </footer> in {filename}")
        return html
    end = start + close_m.end()
    html = html[:start] + SHARED_FOOTER + html[end:]
    print(f"  [ok]     Replaced footer")
    return html


def inject_nav_js(html, filename):
    """
    Inject shared mobile nav JS before </body>.
    index.html keeps its own JS (has full checkout etc.).
    """
    if filename == 'index.html':
        return html  # index.html keeps its own rich JS
    if 'toggleNav' in html:
        return html  # already has nav toggle
    if 'id="hamburger"' not in html and "id='hamburger'" not in html:
        return html  # no hamburger in this page
    html = html.replace('</body>', SHARED_NAV_JS + '\n</body>', 1)
    print(f"  [js]     Injected shared nav JS")
    return html


def remove_duplicate_shared_css(html):
    """If /shared.css appears more than once, deduplicate."""
    count = html.count('/shared.css')
    if count > 1:
        html = re.sub(r'[ \t]*<link[^>]+/shared\.css[^>]*>\n?', '', html)
        html = inject_shared_css(html)
    return html


def process_file(filepath):
    filename = os.path.basename(filepath)
    print(f"\n--- {filename} ---")

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    html = inject_shared_css(html)
    html = replace_nav_header(html, filename)
    html = replace_footer(html, filename)
    html = inject_nav_js(html, filename)
    html = remove_duplicate_shared_css(html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  [saved]  {filename}")
    else:
        print(f"  [nochange] {filename}")


# ─── Main ──────────────────────────────────────────────────────────────────

html_files = sorted(glob.glob(os.path.join(REPO, '*.html')))
# Exclude the snippet files
html_files = [f for f in html_files if os.path.basename(f) not in ('_header.html', '_footer.html')]

print(f"Processing {len(html_files)} HTML files…\n")
for filepath in html_files:
    process_file(filepath)

print("\nDone.")
