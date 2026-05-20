#!/usr/bin/env python3
"""
Brand-guide v4 upgrade patch.
Reads the current patched index.html and applies:
  - Correct brand colour tokens (terracotta #C0603C, sage #4CAF82, charcoal palette)
  - Sage for all hover / focus / active-nav states (never terracotta)
  - Terracotta kept for CTA buttons, eyebrow labels, brand accents
  - Improved PDF section-header eyebrow style (high letter-spacing, terracotta rule)
  - All hardcoded #B85444 in PDF HTML strings → #C0603C
  - All hardcoded old darks (#181818 bg, #2C2F35 surface) → brand tokens
"""
import sys

INPUT  = '/sessions/adoring-intelligent-curie/mnt/LSC Billing App [Phase 01]/index.html'
OUTPUT = '/sessions/adoring-intelligent-curie/mnt/LSC Billing App [Phase 01]/index.html'

with open(INPUT, 'r', encoding='utf-8') as f:
    c = f.read()

ok = 0
def rep(old, new, tag, n=1):
    global c, ok
    found = c.count(old)
    if found == 0:
        print('MISS [' + tag + ']', file=sys.stderr); return
    c = c.replace(old, new, n)
    ok += 1
    print('OK(' + str(min(found, n)) + 'x) [' + tag + ']')

# ── 1. CSS VARIABLES ──────────────────────────────────────────────────────────
rep(
    ':root{\n'
    '  --bg:#181818;--text:#F0EDE8;--surface:#2C2F35;--border:#3D4A5C;\n'
    '  --accent:#B85444;--ah:#9a3d31;--muted:rgba(240,237,232,0.42);--muted2:rgba(240,237,232,0.18);\n'
    '  --row-hover:rgba(240,237,232,0.03);\n'
    '}',
    ':root{\n'
    '  --bg:#0E0E0E;--text:#F0EDE8;--surface:#1C1F24;--border:rgba(240,237,232,0.1);\n'
    '  --accent:#C0603C;--ah:#8C4832;--hover:#4CAF82;--muted:rgba(240,237,232,0.42);--muted2:rgba(240,237,232,0.18);\n'
    '  --row-hover:rgba(240,237,232,0.04);\n'
    '}',
    'CSS variables'
)

# ── 2. NAV LINK hover → sage ──────────────────────────────────────────────────
rep(
    '.nav-link:hover{color:var(--text)}',
    '.nav-link:hover{color:var(--hover)}',
    'nav-link hover → sage'
)

# ── 3. NAV LINK active underline → sage (nav active = sage per brand guide) ──
rep(
    '.nav-link.active{color:var(--text);border-bottom-color:var(--accent)}',
    '.nav-link.active{color:var(--text);border-bottom-color:var(--hover)}',
    'nav-link active underline → sage'
)

# ── 4. BACK BUTTON hover → sage ───────────────────────────────────────────────
rep(
    '.back-btn:hover{color:var(--accent)}',
    '.back-btn:hover{color:var(--hover)}',
    'back-btn hover → sage'
)

# ── 5. GHOST BUTTON hover → sage ─────────────────────────────────────────────
rep(
    '.btn:hover{border-color:var(--accent);color:var(--accent)}',
    '.btn:hover{border-color:var(--hover);color:var(--hover)}',
    'btn hover → sage'
)

# ── 6. PROJECT CARD bottom stripe (hover indicator) → sage ───────────────────
rep(
    '.proj-card::after{content:\'\';position:absolute;bottom:0;left:0;right:0;height:2px;background:var(--accent);transform:scaleX(0);transition:.2s;transform-origin:left}',
    '.proj-card::after{content:\'\';position:absolute;bottom:0;left:0;right:0;height:2px;background:var(--hover);transform:scaleX(0);transition:transform .2s ease-out;transform-origin:left}',
    'proj-card::after stripe → sage'
)

# ── 7. PROJECT CARD hover border → sage ──────────────────────────────────────
rep(
    '.proj-card:hover{border-color:var(--accent)}',
    '.proj-card:hover{border-color:var(--hover)}',
    'proj-card:hover border → sage'
)

# ── 8. FOCUS STATES → sage ───────────────────────────────────────────────────
rep(
    '.field input:focus,.field textarea:focus{border-color:var(--accent)}',
    '.field input:focus,.field textarea:focus{border-color:var(--hover)}',
    'field input/textarea focus → sage'
)
rep(
    '.svc-select:focus{border-color:var(--accent)}',
    '.svc-select:focus{border-color:var(--hover)}',
    'svc-select focus → sage'
)
rep(
    '.num-inp:focus{border-color:var(--accent)}',
    '.num-inp:focus{border-color:var(--hover)}',
    'num-inp focus → sage'
)
rep(
    '.pricing-table input:focus{border-color:var(--accent)}',
    '.pricing-table input:focus{border-color:var(--hover)}',
    'pricing-table input focus → sage'
)
rep(
    '.tax-setting input:focus{border-color:var(--accent)}',
    '.tax-setting input:focus{border-color:var(--hover)}',
    'tax-setting input focus → sage'
)
rep(
    '.doc-type-select:focus{border-color:var(--accent)}',
    '.doc-type-select:focus{border-color:var(--hover)}',
    'doc-type-select focus → sage'
)

# text-inp:focus appears twice (duplicate rule); replace both
rep(
    '.text-inp:focus{border-color:var(--accent)}',
    '.text-inp:focus{border-color:var(--hover)}',
    'text-inp focus → sage', n=2
)

# ── 9. UPID FIELD highlight → sage (active input indicator) ──────────────────
rep(
    '.upid-field{border-color:var(--accent) !important}',
    '.upid-field{border-color:var(--hover) !important}',
    'upid-field → sage'
)

# ── 10. PANEL HEADS: #111 → brand black #0E0E0E ──────────────────────────────
# bb-head, est-block-head, pricing-sec-head all use background:#111
rep(
    'background:#111;padding:9px 16px;border-bottom:1px solid var(--border)',
    'background:#0E0E0E;padding:9px 16px;border-bottom:1px solid var(--border)',
    'bb-head bg #111 → brand black'
)
rep(
    'background:#111;padding:8px 16px;display:flex;justify-content:space-between;border-bottom:1px solid var(--border)',
    'background:#0E0E0E;padding:8px 16px;display:flex;justify-content:space-between;border-bottom:1px solid var(--border)',
    'est-block-head bg #111 → brand black'
)
rep(
    'background:#111;padding:10px 16px;border-bottom:1px solid var(--border)',
    'background:#0E0E0E;padding:10px 16px;border-bottom:1px solid var(--border)',
    'pricing-sec-head bg #111 → brand black'
)

# ── 11. INPUT BACKGROUNDS: #1a1c20 → #161819 (darker inset on surface) ────────
rep(
    'background:#1a1c20;border:1px solid var(--border);color:var(--text);font-size:12px;font-family:\'Funnel Sans\',sans-serif;padding:5px 8px;outline:none;transition:.15s;width:100%',
    'background:#161819;border:1px solid var(--border);color:var(--text);font-size:12px;font-family:\'Funnel Sans\',sans-serif;padding:5px 8px;outline:none;transition:.15s;width:100%',
    'text-inp bg'
)
rep(
    'background:#1a1c20;border:1px solid var(--border);color:var(--text);font-size:12px;font-family:\'Funnel Sans\',sans-serif;padding:5px 8px;outline:none;transition:.15s;text-align:right',
    'background:#161819;border:1px solid var(--border);color:var(--text);font-size:12px;font-family:\'Funnel Sans\',sans-serif;padding:5px 8px;outline:none;transition:.15s;text-align:right',
    'num-inp bg'
)
# Second text-inp rule (duplicate definition)
rep(
    'background:#1a1c20;border:1px solid var(--border);color:var(--text);font-size:12px;padding:5px 8px;outline:none;transition:.15s;width:100%',
    'background:#161819;border:1px solid var(--border);color:var(--text);font-size:12px;padding:5px 8px;outline:none;transition:.15s;width:100%',
    'text-inp bg (2nd definition)'
)
# pricing-table input
rep(
    'background:#1a1c20;border:1px solid var(--border);color:var(--text);font-size:12px;font-family:\'Funnel Sans\',sans-serif;padding:5px 8px;outline:none;width:90px;text-align:right',
    'background:#161819;border:1px solid var(--border);color:var(--text);font-size:12px;font-family:\'Funnel Sans\',sans-serif;padding:5px 8px;outline:none;width:90px;text-align:right',
    'pricing-table input bg'
)
# tax-setting input
rep(
    'background:#1a1c20;border:1px solid var(--border);color:var(--text);font-size:13px;padding:6px 10px;outline:none;width:90px;text-align:right',
    'background:#161819;border:1px solid var(--border);color:var(--text);font-size:13px;padding:6px 10px;outline:none;width:90px;text-align:right',
    'tax-setting input bg'
)

# ── 12. SVC-SELECT OPTION bg ──────────────────────────────────────────────────
rep(
    '.svc-select option{background:#1e2228;color:var(--text)}',
    '.svc-select option{background:#1C1F24;color:var(--text)}',
    'svc-select option bg'
)

# ── 13. TABLE ROW BORDERS: rgba(61,74,92,...) → rgba(240,237,232,...) ─────────
rep(
    'border-bottom:1px solid rgba(61,74,92,0.4)',
    'border-bottom:1px solid rgba(240,237,232,0.08)',
    'table row borders', n=10
)

# ── 14. BB-PICKER background ─────────────────────────────────────────────────
rep(
    'background:rgba(61,74,92,0.12)',
    'background:rgba(240,237,232,0.04)',
    'bb-picker bg'
)

# ── 15. NET ROW accent tint ───────────────────────────────────────────────────
rep(
    'background:rgba(184,84,68,0.08)',
    'background:rgba(192,96,60,0.08)',
    'net-row accent bg'
)

# ── 16. PDF STYLE BLOCKS: improve .sh eyebrow + body tone ────────────────────
# Quote PDF style block (no body padding in original)
rep(
    '*{box-sizing:border-box;margin:0;padding:0}body{font-family:Arial,Helvetica,sans-serif;font-size:11pt;color:#181818;background:#fff}.sh{font-size:8pt;text-transform:uppercase;letter-spacing:.12em;color:#888;font-weight:700;margin-bottom:10px;padding-bottom:6px;border-bottom:2px solid #181818}',
    '*{box-sizing:border-box;margin:0;padding:0}body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:11pt;color:#0E0E0E;background:#fff;padding:40px 48px;max-width:740px;margin:0 auto}.sh{font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;font-weight:700;margin-bottom:12px;padding-bottom:7px;border-bottom:1px solid rgba(192,96,60,0.25)}',
    'Quote PDF style block'
)
# Invoice PDF style block (has body padding already)
rep(
    '*{box-sizing:border-box;margin:0;padding:0}body{font-family:Arial,Helvetica,sans-serif;font-size:11pt;color:#181818;background:#fff;padding:40px 32px;max-width:700px;margin:0 auto}.sh{font-size:8pt;text-transform:uppercase;letter-spacing:.12em;color:#888;font-weight:700;margin-bottom:10px;padding-bottom:6px;border-bottom:2px solid #181818}',
    '*{box-sizing:border-box;margin:0;padding:0}body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:11pt;color:#0E0E0E;background:#fff;padding:40px 48px;max-width:740px;margin:0 auto}.sh{font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;font-weight:700;margin-bottom:12px;padding-bottom:7px;border-bottom:1px solid rgba(192,96,60,0.25)}',
    'Invoice PDF style block'
)

# ── 17. PDF HEADER divider line: 3px solid #181818 → brand black ─────────────
rep(
    'border-bottom:3px solid #181818">',
    'border-bottom:2px solid #0E0E0E">',
    'PDF header divider', n=2
)

# ── 18. PDF: ALL #B85444 → #C0603C ───────────────────────────────────────────
# Replace every occurrence inside the PDF HTML string builders
rep('#B85444', '#C0603C', 'PDF #B85444 → #C0603C (all)', n=50)

# ── 19. PDF: body text color #181818 → #0E0E0E in section items ──────────────
# Service item text colours in PDF (these are inside the PDF HTML string)
rep(
    "color:#181818;margin-bottom:3px'>",
    "color:#0E0E0E;margin-bottom:3px'>",
    'PDF service item text', n=10
)
rep(
    "color:#181818;margin-bottom:2px'>",
    "color:#0E0E0E;margin-bottom:2px'>",
    'PDF crew/travel text', n=10
)

# ── 20. PDF: deliverables table alternating row warm tint ─────────────────────
# Even rows: #fff → #fff (keep white)
# Odd rows: #fafafa → #F7F5F2 (warm near-white matching brand F0EDE8 direction)
rep(
    "var bg=i%2===0?'#fff':'#fafafa'",
    "var bg=i%2===0?'#fff':'#F7F5F2'",
    'PDF deliverables alt row warm tint', n=2
)

# ── 21. PDF: table header row bg #f7f7f7 → warmer tint ───────────────────────
rep(
    "background:#f7f7f7'>",
    "background:#F2F0EC'>",
    'PDF table header row bg', n=2
)

# ── 22. PDF: deliverables header cells bg (matches table head row) ────────────
rep(
    "border-bottom:1px solid #e8e8e8'>",
    "border-bottom:1px solid #E8E2D9'>",
    'PDF th border', n=10
)

# ── 23. PDF: payment terms block background + border ─────────────────────────
rep(
    "background:#f7f7f7;border-left:3px solid #C0603C",
    "background:#FBF9F7;border-left:3px solid #C0603C",
    'PDF payment terms bg'
)

# ── 24. PDF: contact footer border top ───────────────────────────────────────
rep(
    "border-top:1px solid #e8e8e8'>",
    "border-top:1px solid #E8E2D9'>",
    'PDF footer border'
)

# ── 25. PDF: contact footer text colour #333 → #0E0E0E ───────────────────────
rep(
    "font-size:10.5pt;color:#333;line-height:2.1",
    "font-size:10.5pt;color:#0E0E0E;line-height:2.1",
    'PDF contact footer text'
)

# ── 26. PDF: payment details section divider border (#181818 → #0E0E0E) ───────
rep(
    "border-top:2px solid #181818'>",
    "border-top:2px solid #0E0E0E'>",
    'PDF payment details divider top'
)
rep(
    "border-bottom:2px solid #181818",
    "border-bottom:2px solid #0E0E0E",
    'PDF payment details divider bottom'
)

# ── 27. PDF: invoice total box (#181818 row bg) ───────────────────────────────
rep(
    "background:#181818'>",
    "background:#0E0E0E'>",
    'PDF total row bg → brand black'
)

# ── 28. PDF: inline body text (#181818 → #0E0E0E in payment table) ────────────
rep(
    "font-weight:600;color:#181818'>",
    "font-weight:600;color:#0E0E0E'>",
    'PDF payment table cell text', n=10
)
rep(
    "font-weight:800;color:#181818;margin-top:6px",
    "font-weight:800;color:#0E0E0E;margin-top:6px",
    'PDF project name text', n=2
)

# ── 29. PDF: invoice header title text (#181818) ──────────────────────────────
rep(
    "font-size:16pt;font-weight:900;color:#181818;letter-spacing:.02em",
    "font-size:16pt;font-weight:900;color:#0E0E0E;letter-spacing:.02em",
    'PDF invoice header title'
)

# ── 30. PDF logo fallback text: LSC CREATIVE branding ────────────────────────
# Already updated #B85444 → #C0603C in step 18 (covers the dot colour)

total_changes = 30  # approximate target
print('\nChanges applied: ' + str(ok))
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(c)
print('Written: ' + OUTPUT)
