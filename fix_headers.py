#!/usr/bin/env python3
"""
For every HTML page:
1. Strip the inline /* Header */ CSS block from <style> tags
2. Ensure <link rel="stylesheet" href="/shared.css"> is present
3. Also strip duplicate inline hamburger JS if it exists as a <script> block
   (header.js already handles this)
"""

import os, re, glob

ROOT = '/Users/clio/dev/lawtasksai-landing'

def strip_header_css(style_content):
    """Remove inline header/nav CSS blocks up to (but not including) the next /* comment */."""
    # Covers: /* Header */, /* Header — ... */, /* ===== MAIN SITE HEADER ... =====  */
    pattern = re.compile(
        r'[ \t]*/\*[\s=]*(?:Header|MAIN SITE HEADER|Nav(?:igation)?)[^*]*\*/.*?(?=\n[ \t]*/\*|\Z)',
        re.DOTALL | re.IGNORECASE
    )
    cleaned = pattern.sub('', style_content)
    # Also strip orphaned nav/hamburger/dropdown blocks not under a comment
    # (for pages like sample.html that split them under separate /* Dropdown */ /* Hamburger */ comments)
    orphan_patterns = [
        r'[ \t]*/\*\s*Dropdown\s*\*/.*?(?=\n[ \t]*/\*|\Z)',
        r'[ \t]*/\*\s*Hamburger\s*\*/.*?(?=\n[ \t]*/\*|\Z)',
        r'[ \t]*/\*\s*Mobile responsive for header\s*\*/.*?(?=\n[ \t]*/\*|\Z)',
    ]
    for op in orphan_patterns:
        cleaned = re.sub(op, '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    # Clean up resulting blank lines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned

def strip_hamburger_js(content):
    """Remove inline hamburger/dropdown script blocks that duplicate header.js logic."""
    # Match script blocks containing hamburger click handler
    pattern = re.compile(
        r'\n?[ \t]*<script>\s*\n\s*(?:const|var|let)\s+hamburger[^<]+</script>',
        re.DOTALL
    )
    return pattern.sub('', content)

def ensure_shared_css(content):
    """Add shared.css link after favicon if not present."""
    if '/shared.css' in content:
        return content
    return re.sub(
        r'(<link rel="icon"[^>]+>)',
        r'\1\n    <link rel="stylesheet" href="/shared.css">',
        content
    )

files = (
    glob.glob(f'{ROOT}/*.html') +
    glob.glob(f'{ROOT}/blog/*.html')
)

skip = {'_header.html', '_footer.html'}
changed = []
skipped_no_header_comment = []

for filepath in sorted(files):
    name = os.path.basename(filepath)
    if name in skip:
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    # Only touch files that have some form of inline header CSS
    header_markers = ['/* Header', '/* MAIN SITE HEADER', '/* Dropdown */', '/* Hamburger */']
    if not any(m in content for m in header_markers):
        skipped_no_header_comment.append(os.path.relpath(filepath, ROOT))
        continue

    # Strip inline header CSS from all <style> blocks
    def clean_style(m):
        return '<style>' + strip_header_css(m.group(1)) + '</style>'
    content = re.sub(r'<style>(.*?)</style>', clean_style, content, flags=re.DOTALL)

    # Ensure shared.css linked
    content = ensure_shared_css(content)

    # Strip duplicate hamburger JS
    content = strip_hamburger_js(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changed.append(os.path.relpath(filepath, ROOT))
        print(f'  FIXED:   {os.path.relpath(filepath, ROOT)}')
    else:
        print(f'  NO-DIFF: {os.path.relpath(filepath, ROOT)}')

print(f'\nUpdated {len(changed)} files.')
if skipped_no_header_comment:
    print(f'Skipped (no inline header block): {skipped_no_header_comment}')
