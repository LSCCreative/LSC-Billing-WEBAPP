#!/usr/bin/env python3
import sys

INPUT  = '/sessions/adoring-intelligent-curie/mnt/uploads/index.html'
OUTPUT = '/sessions/adoring-intelligent-curie/mnt/LSC Billing App [Phase 01]/index.html'

with open(INPUT, 'r', encoding='utf-8') as f:
    c = f.read()

changes = 0
def rep(old, new, tag, count=1):
    global c, changes
    found = c.count(old)
    if found == 0:
        print('WARNING: not found [' + tag + ']', file=sys.stderr)
        return
    if found < count:
        print('WARNING: expected ' + str(count) + ' occurrences but found ' + str(found) + ' [' + tag + ']', file=sys.stderr)
    c = c.replace(old, new, count)
    changes += 1
    print('OK (' + str(min(found,count)) + 'x): [' + tag + ']')

# ── 1. Add LOGO_B64 constant before PDF builders ─────────────────────────────
rep(
    '// ── PDF BUILDERS ──────────────────────────────────────────────────────────────\nfunction buildClientPDF(proj){',
    """// ── PDF BUILDERS ──────────────────────────────────────────────────────────────
// LOGO: run  base64 -i logo.png | tr -d '\\n' | pbcopy  then paste result below.
var LOGO_B64 = '';
function buildClientPDF(proj){""",
    'Add LOGO_B64 constant'
)

# ── 2. Logo in buildClientPDF header (replaces text branding, 1st occurrence) ─
OLD_BRAND = (
    "      '<div><div style=\"font-size:22pt;font-weight:900;letter-spacing:.02em\">LSC CREATIVE<span style=\"color:#B85444\">.</span></div>'+\n"
    "      '<div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.12em;color:#888;margin-top:4px\">Motion Productions</div></div>'+"
)
NEW_BRAND = (
    "      (LOGO_B64?'<img src=\"data:image/png;base64,'+LOGO_B64+'\" style=\"height:76px;width:auto;object-fit:contain;display:block\">':'<div><div style=\"font-size:22pt;font-weight:900;letter-spacing:.02em\">LSC CREATIVE<span style=\"color:#B85444\">.</span></div><div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.12em;color:#888;margin-top:4px\">Motion Productions</div></div>')+"
)
# replace both occurrences (buildClientPDF + buildClientInvoicePDF share identical branding HTML)
rep(OLD_BRAND, NEW_BRAND, 'Logo in PDF headers', count=2)

# ── 3. Equipment: aggregate to single line in buildClientPDF ─────────────────
OLD_EQ = (
    "  if(eqActive.length){serviceItems+='<div style=\"margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0f0f0\">"
    "<div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#B85444;font-weight:700;margin-bottom:5px\">Equipment Hire</div>'"
    "+eqActive.map(function(e){return'<div style=\"font-size:10pt;color:#181818;margin-bottom:2px\">'+esc(e.vendor||'Equipment')+'</div>';}).join('')+'</div>';}"
)
NEW_EQ = (
    "  if(eqActive.length){serviceItems+='<div style=\"margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0f0f0\">"
    "<div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#B85444;font-weight:700;margin-bottom:5px\">Equipment Hire</div>"
    "<div style=\"font-size:10.5pt;font-weight:600;color:#181818;margin-bottom:3px\">Equipment Hire</div></div>';}"
)
rep(OLD_EQ, NEW_EQ, 'Equipment aggregation', count=2)

# ── 4. "Total Investment" → "Project Total" in buildClientPDF ────────────────
rep(
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">Total Investment <span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">Project Total <span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    'Label: Total Investment → Project Total'
)

# ── 5. "Total Due" → "Project Total" in buildClientInvoicePDF ───────────────
rep(
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">Total Due <span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">Project Total <span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    'Label: Total Due → Project Total'
)

print('\nTotal change groups: ' + str(changes))

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(c)

print('Written to: ' + OUTPUT)
