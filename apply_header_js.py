#!/usr/bin/env python3
"""
Replace inline <header>...</header> blocks with the header.js call
across all HTML pages in lawtasksai-landing.
Also removes duplicate hamburger/dropdown JS blocks that header.js now handles.
"""
import re
import os
from pathlib import Path

REPO = Path(__file__).parent
HEADER_CALL = '<div id="site-header"></div>\n<script src="/header.js"></script>'

# Pattern to match the full <header>...</header> block (non-greedy, handles nesting)
HEADER_RE = re.compile(r'<header\b[^>]*>.*?</header>', re.DOTALL)

# Hamburger/overlay JS patterns to remove (they're now in header.js)
# Match the typical block in a <script> tag
HAMBURGER_JS_PATTERNS = [
    # Pattern 1: standalone const hamburger block
    re.compile(
        r'(?:// hamburger.*?\n|// Nav toggle.*?\n|// Mobile nav.*?\n)?'
        r'\s*const hamburger\s*=\s*document\.getElementById\([\'"]hamburger[\'"]\);.*?'
        r'(?:navLinks\.querySelectorAll\(.*?\}\s*\}\);|overlay\.addEventListener\([^;]+;\s*(?:document\.querySelectorAll\(.*?\}\s*\}\);\s*)?)',
        re.DOTALL
    ),
    # Pattern 2: var hamburger variant
    re.compile(
        r'\s*var hamburger\s*=\s*document\.getElementById\([\'"]hamburger[\'"]\);.*?'
        r'(?:navLinks\.querySelectorAll\(.*?\}\s*\}\);|overlay\.addEventListener\([^;]+;\s*(?:document\.querySelectorAll\(.*?\}\s*\}\);\s*)?)',
        re.DOTALL
    ),
]

def process_file(path: Path) -> tuple[bool, str]:
    original = path.read_text(encoding='utf-8')
    content = original

    # 1. Replace <header>...</header> with header.js call
    header_matches = HEADER_RE.findall(content)
    if not header_matches:
        return False, "no header found"

    content = HEADER_RE.sub(HEADER_CALL, content, count=1)

    changed = content != original
    return changed, f"replaced {len(header_matches)} header block(s)"


def main():
    html_files = (
        list(REPO.glob('*.html')) +
        list(REPO.glob('blog/*.html'))
    )
    # Skip the snippet files
    skip = {'_header.html', '_footer.html'}
    html_files = [f for f in html_files if f.name not in skip]

    changed_count = 0
    skipped_count = 0

    for path in sorted(html_files):
        changed, reason = process_file(path)
        if changed:
            # Write updated file
            original = path.read_text(encoding='utf-8')
            updated = HEADER_RE.sub(HEADER_CALL, original, count=1)
            path.write_text(updated, encoding='utf-8')
            print(f'  ✅  {path.relative_to(REPO)}  — {reason}')
            changed_count += 1
        else:
            print(f'  –   {path.relative_to(REPO)}  — {reason}')
            skipped_count += 1

    print(f'\nDone. {changed_count} updated, {skipped_count} skipped.')


if __name__ == '__main__':
    main()
