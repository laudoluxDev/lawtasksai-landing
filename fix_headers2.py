#!/usr/bin/env python3
"""
Pass 2: Strip any remaining inline header CSS by matching known selectors directly.
These are all defined in shared.css and should not appear inline.
"""

import os, re, glob

ROOT = '/Users/clio/dev/lawtasksai-landing'

# Individual CSS rules to strip (matched as full rule blocks)
SELECTOR_PATTERNS = [
    # header element rules
    r'[ \t]*header\s*\{[^}]+\}\n?',
    r'[ \t]*header\s*\.container\s*\{[^}]+\}\n?',
    r'[ \t]*header\.main-header\s*\{[^}]+\}\n?',
    # logo
    r'[ \t]*\.logo\s*\{[^}]+\}\n?',
    r'[ \t]*\.logo\s+span\s*\{[^}]+\}\n?',
    # nav
    r'[ \t]*\.nav-links\s*\{[^}]+\}\n?',
    r'[ \t]*\.nav-links\s*>\s*a\s*\{[^}]+\}\n?',
    r'[ \t]*\.nav-links\s*>\s*a:hover(?:,\s*\.nav-links\s*>\s*a\.active)?\s*\{[^}]+\}\n?',
    r'[ \t]*\.nav-links\s*>\s*a\.active\s*\{[^}]+\}\n?',
    r'[ \t]*\.nav-links\s*>\s*a:hover\s*\{[^}]+\}\n?',
    r'[ \t]*\.nav-links\s*>\s*a,\s*\n?\s*\.nav-links\s*\.dropdown-toggle\s*\{[^}]+\}\n?',
    # header CTA
    r'[ \t]*\.header-cta\s*\{[^}]+\}\n?',
    r'[ \t]*\.header-cta:hover\s*\{[^}]+\}\n?',
    # dropdown
    r'[ \t]*\.dropdown\s*\{\s*position:\s*relative;\s*\}\n?',
    r'[ \t]*\.dropdown-toggle\s*\{[^}]+\}\n?',
    r'[ \t]*\.dropdown-toggle:hover\s*\{[^}]+\}\n?',
    r'[ \t]*\.dropdown-toggle::after\s*\{[^}]+\}\n?',
    r'[ \t]*\.dropdown-menu\s*\{[^}]+\}\n?',
    r'[ \t]*\.dropdown:hover\s*\.dropdown-menu\s*\{[^}]+\}\n?',
    r'[ \t]*\.dropdown\.mobile-open\s*\.dropdown-menu\s*\{[^}]+\}\n?',
    r'[ \t]*\.dropdown-menu\s*a\s*\{[^}]+\}\n?',
    r'[ \t]*\.dropdown-menu\s*a:hover\s*\{[^}]+\}\n?',
    # hamburger
    r'[ \t]*\.hamburger\s*\{[^}]+\}\n?',
    r'[ \t]*\.hamburger\s+span\s*\{[^}]+\}\n?',
    r'[ \t]*\.hamburger\.active\s+span:nth-child\(1\)\s*\{[^}]+\}\n?',
    r'[ \t]*\.hamburger\.active\s+span:nth-child\(2\)\s*\{[^}]+\}\n?',
    r'[ \t]*\.hamburger\.active\s+span:nth-child\(3\)\s*\{[^}]+\}\n?',
    # mobile overlay
    r'[ \t]*\.mobile-overlay\s*\{[^}]+\}\n?',
    r'[ \t]*\.mobile-overlay\.active\s*\{[^}]+\}\n?',
]

# Responsive versions (inside @media blocks) - same selectors
RESPONSIVE_SELECTOR_PATTERNS = [
    r'[ \t]*\.hamburger\s*\{\s*display:\s*block;\s*\}\n?',
    r'[ \t]*\.nav-links\s*\{[^}]*position:\s*fixed[^}]*\}\n?',
    r'[ \t]*\.nav-links\.active\s*\{\s*display:\s*flex;\s*\}\n?',
    r'[ \t]*\.nav-links\s*>\s*a(?:,\s*\n?\s*\.nav-links\s*\.dropdown-toggle)?\s*\{[^}]*padding:\s*14px[^}]*\}\n?',
    r'[ \t]*\.dropdown\s*\{\s*width:\s*100%;\s*\}\n?',
    r'[ \t]*\.dropdown-toggle\s*\{[^}]*border-bottom[^}]*\}\n?',
    r'[ \t]*\.dropdown-menu\s*\{[^}]*position:\s*static[^}]*\}\n?',
    r'[ \t]*\.dropdown:hover\s*\.dropdown-menu\s*\{\s*display:\s*none;\s*\}\n?',
    r'[ \t]*\.dropdown\.mobile-open\s*\.dropdown-menu\s*\{\s*display:\s*block;\s*\}\n?',
    r'[ \t]*\.header-cta\s*\{[^}]*(?:width|margin-top)[^}]*\}\n?',
]

def clean_style(style_content):
    cleaned = style_content
    for pat in SELECTOR_PATTERNS + RESPONSIVE_SELECTOR_PATTERNS:
        cleaned = re.sub(pat, '', cleaned, flags=re.DOTALL)
    # Remove orphaned section comments (/* Header */, /* Nav */, etc.)
    cleaned = re.sub(r'[ \t]*/\*\s*(?:Header|Nav(?:igation)?|Hamburger|Dropdown|Mobile responsive for header)\s*\*/\s*\n?', '', cleaned, flags=re.IGNORECASE)
    # Remove comment blocks (/* === ... === */)
    cleaned = re.sub(r'[ \t]*/\*[=\s]*(?:MAIN SITE HEADER|NAV)[^*]*\*/\s*\n?', '', cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned

def ensure_shared_css(content):
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

for filepath in sorted(files):
    if os.path.basename(filepath) in skip:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original
    content = re.sub(r'<style>(.*?)</style>',
                     lambda m: '<style>' + clean_style(m.group(1)) + '</style>',
                     content, flags=re.DOTALL)
    content = ensure_shared_css(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changed.append(os.path.relpath(filepath, ROOT))
        print(f'  FIXED:   {os.path.relpath(filepath, ROOT)}')
    else:
        print(f'  clean:   {os.path.relpath(filepath, ROOT)}')

print(f'\nUpdated {len(changed)} files.')
