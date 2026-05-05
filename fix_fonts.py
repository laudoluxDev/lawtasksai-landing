#!/usr/bin/env python3
"""Bump font sizes in redesign.css to meet minimum readability thresholds."""

with open('redesign.css', 'r') as f:
    content = f.read()

replacements = [
    # Trust bar 0.77 -> 0.85rem
    ('font-size: 0.77rem;\n  font-weight: 500;\n  padding: 9px 0;\n  text-align: center;',
     'font-size: 0.85rem;\n  font-weight: 500;\n  padding: 9px 0;\n  text-align: center;'),
    # Dropdown caret 0.68 -> 0.8rem
    ('font-size: 0.68rem;\n  opacity: 0.55;',
     'font-size: 0.8rem;\n  opacity: 0.55;'),
    # section-eyebrow 0.77 -> 0.85rem
    ('.section-eyebrow {\n  font-size: 0.77rem;',
     '.section-eyebrow {\n  font-size: 0.85rem;'),
    # hero-eyebrow 0.78 -> 0.85rem
    ('  font-size: 0.78rem;\n  font-weight: 700;\n  padding: 5px 14px;\n  border-radius: 100px;',
     '  font-size: 0.85rem;\n  font-weight: 700;\n  padding: 5px 14px;\n  border-radius: 100px;'),
    # hero-meta-item 0.82 -> 0.875rem
    ('.hero-meta-item {\n  font-size: 0.82rem;',
     '.hero-meta-item {\n  font-size: 0.875rem;'),
    # hero-card-title 0.77 -> 0.85rem
    ('.hero-card-title { color: #64748b; font-size: 0.77rem; font-weight: 500; }',
     '.hero-card-title { color: #64748b; font-size: 0.85rem; font-weight: 500; }'),
    # task-name 0.82 -> 0.875rem
    ('.task-name { font-size: 0.82rem; font-weight: 600;',
     '.task-name { font-size: 0.875rem; font-weight: 600;'),
    # task-status 0.73 -> 0.8rem
    ('.task-status { font-size: 0.73rem; color: var(--muted); }',
     '.task-status { font-size: 0.8rem; color: var(--muted); }'),
    # task-time 0.72 -> 0.8rem
    ('.task-time { font-size: 0.72rem; color: var(--muted-2); flex-shrink: 0; }',
     '.task-time { font-size: 0.8rem; color: var(--muted-2); flex-shrink: 0; }'),
    # hero-output-label 0.73 -> 0.8rem
    ('  font-size: 0.73rem;\n  font-weight: 700;\n  color: var(--green);\n  text-transform: uppercase;\n  letter-spacing: 0.05em;\n  margin-bottom: 6px;',
     '  font-size: 0.8rem;\n  font-weight: 700;\n  color: var(--green);\n  text-transform: uppercase;\n  letter-spacing: 0.05em;\n  margin-bottom: 6px;'),
    # hero-output p 0.81 -> 0.875rem
    ('.hero-output p { font-size: 0.81rem; color: #166534; line-height: 1.5; }',
     '.hero-output p { font-size: 0.875rem; color: #166534; line-height: 1.5; }'),
    # hero-timer 0.73 -> 0.8rem
    ('  font-size: 0.73rem;\n  color: var(--muted);\n}',
     '  font-size: 0.8rem;\n  color: var(--muted);\n}'),
    # .quote 0.94 -> 1rem
    ('.quote { font-size: 0.94rem; color: var(--ink-2); line-height: 1.65; margin-bottom: 14px; }',
     '.quote { font-size: 1rem; color: var(--ink-2); line-height: 1.65; margin-bottom: 14px; }'),
    # .attr 0.81 -> 0.875rem
    ('.attr  { font-size: 0.81rem; color: var(--muted); font-weight: 600; }',
     '.attr  { font-size: 0.875rem; color: var(--muted); font-weight: 600; }'),
    # testimonial-note 0.76 -> 0.85rem
    ('  color: var(--muted-2);\n  font-size: 0.76rem;\n  font-style: italic;',
     '  color: var(--muted-2);\n  font-size: 0.85rem;\n  font-style: italic;'),
    # step-card p 0.9 -> 1rem
    ('.step-card p  { font-size: 0.9rem; color: var(--muted); line-height: 1.65; }',
     '.step-card p  { font-size: 1rem; color: var(--muted); line-height: 1.65; }'),
    # trust-badge h4 0.92 -> 1rem
    ('.trust-badge h4 { font-size: 0.92rem; font-weight: 700; color: white; margin-bottom: 4px; }',
     '.trust-badge h4 { font-size: 1rem; font-weight: 700; color: white; margin-bottom: 4px; }'),
    # trust-badge p 0.83 -> 0.875rem
    ('.trust-badge p  { font-size: 0.83rem; color: #94a3b8; line-height: 1.55; }',
     '.trust-badge p  { font-size: 0.875rem; color: #94a3b8; line-height: 1.55; }'),
    # stat-label 0.82 -> 0.875rem
    ('.stat-label { font-size: 0.82rem; color: #94a3b8; font-weight: 500; line-height: 1.45; }',
     '.stat-label { font-size: 0.875rem; color: #94a3b8; font-weight: 500; line-height: 1.45; }'),
    # feature-card h3 0.98 -> 1rem
    ('.feature-card h3 { font-size: 0.98rem; font-weight: 700; color: var(--ink); margin-bottom: 8px; }',
     '.feature-card h3 { font-size: 1rem; font-weight: 700; color: var(--ink); margin-bottom: 8px; }'),
    # feature-card p 0.87 -> 1rem
    ('.feature-card p  { font-size: 0.87rem; color: var(--muted); line-height: 1.62; }',
     '.feature-card p  { font-size: 1rem; color: var(--muted); line-height: 1.62; }'),
    # pricing-note 0.94 -> 1rem
    ('  color: var(--muted);\n  font-size: 0.94rem;\n  margin-top: -32px;',
     '  color: var(--muted);\n  font-size: 1rem;\n  margin-top: -32px;'),
    # pricing-badge 0.72 -> 0.8rem
    ('  border-radius: 100px;\n  font-size: 0.72rem;\n  font-weight: 700;\n  white-space: nowrap;',
     '  border-radius: 100px;\n  font-size: 0.8rem;\n  font-weight: 700;\n  white-space: nowrap;'),
    # pricing-card-name 0.8 -> 0.85rem
    ('.pricing-card-name {\n  font-size: 0.8rem;',
     '.pricing-card-name {\n  font-size: 0.85rem;'),
    # pricing-per 0.8 -> 0.875rem
    ('.pricing-per   { font-size: 0.8rem; color: var(--muted); margin-bottom: 18px; }',
     '.pricing-per   { font-size: 0.875rem; color: var(--muted); margin-bottom: 18px; }'),
    # pricing-perks li 0.83 -> 0.875rem
    ('.pricing-perks li {\n  font-size: 0.83rem;',
     '.pricing-perks li {\n  font-size: 0.875rem;'),
    # pricing-footnote 0.77 -> 0.85rem
    ('  color: var(--muted-2);\n  font-size: 0.77rem;\n  margin-top: 28px;',
     '  color: var(--muted-2);\n  font-size: 0.85rem;\n  margin-top: 28px;'),
    # chevron 0.72 -> 0.8rem
    ('.chevron { transition: transform 0.25s; font-size: 0.72rem; display: inline-block; }',
     '.chevron { transition: transform 0.25s; font-size: 0.8rem; display: inline-block; }'),
    # collapsible-body h3 0.97 -> 1rem
    ('.collapsible-body h3 { font-size: 0.97rem; font-weight: 700; color: var(--ink); margin-bottom: 8px; }',
     '.collapsible-body h3 { font-size: 1rem; font-weight: 700; color: var(--ink); margin-bottom: 8px; }'),
    # collapsible-body p/li 0.87 -> 1rem
    ('.collapsible-body p, .collapsible-body li {\n  font-size: 0.87rem; color: var(--muted); line-height: 1.7;',
     '.collapsible-body p, .collapsible-body li {\n  font-size: 1rem; color: var(--muted); line-height: 1.7;'),
    # footer-disclaimer span 0.78 -> 0.875rem
    ('.footer-disclaimer span { font-size: 0.78rem; color: #94a3b8; }',
     '.footer-disclaimer span { font-size: 0.875rem; color: #94a3b8; }'),
    # disclaimer-label 0.73 -> 0.8rem
    ('.disclaimer-label {\n  font-size: 0.73rem;',
     '.disclaimer-label {\n  font-size: 0.8rem;'),
    # footer-brand p 0.84 -> 0.875rem
    ('.footer-brand p { font-size: 0.84rem; color: #64748b; max-width: 300px; line-height: 1.6; }',
     '.footer-brand p { font-size: 0.875rem; color: #64748b; max-width: 300px; line-height: 1.6; }'),
    # footer-links a 0.84 -> 0.875rem
    ('.footer-links a { color: #64748b; text-decoration: none; font-size: 0.84rem; transition: color 0.15s; }',
     '.footer-links a { color: #64748b; text-decoration: none; font-size: 0.875rem; transition: color 0.15s; }'),
    # footer-bottom 0.81 -> 0.875rem
    ('  padding-top: 20px;\n  font-size: 0.81rem;\n  color: #475569;',
     '  padding-top: 20px;\n  font-size: 0.875rem;\n  color: #475569;'),
    # modal-sub 0.84 -> 0.875rem
    ('.modal-sub { font-size: 0.84rem; color: var(--muted); margin-bottom: 22px; line-height: 1.55; }',
     '.modal-sub { font-size: 0.875rem; color: var(--muted); margin-bottom: 22px; line-height: 1.55; }'),
    # form-group label 0.82 -> 0.875rem
    ('.form-group label { display: block; font-size: 0.82rem; font-weight: 600; color: #374151; margin-bottom: 4px; }',
     '.form-group label { display: block; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 4px; }'),
    # attestation-box span 0.82 -> 0.875rem
    ('.attestation-box span { font-size: 0.82rem; color: #166534; line-height: 1.5; }',
     '.attestation-box span { font-size: 0.875rem; color: #166534; line-height: 1.5; }'),
    # modal-error 0.82 -> 0.875rem
    ('.modal-error { color: var(--red); font-size: 0.82rem; min-height: 1.2em; margin-bottom: 8px; }',
     '.modal-error { color: var(--red); font-size: 0.875rem; min-height: 1.2em; margin-bottom: 8px; }'),
    # modal-stripe-note 0.75 -> 0.8rem
    ('.modal-stripe-note { text-align: center; font-size: 0.75rem; color: var(--muted-2); margin-top: 10px; }',
     '.modal-stripe-note { text-align: center; font-size: 0.8rem; color: var(--muted-2); margin-top: 10px; }'),
]

changes = 0
not_found = []
for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        changes += 1
    else:
        not_found.append(repr(old[:70]))

print(f"Applied {changes}/{len(replacements)} replacements")
if not_found:
    print("NOT FOUND:")
    for s in not_found:
        print(" ", s)

with open('redesign.css', 'w') as f:
    f.write(content)

print("Saved redesign.css")
