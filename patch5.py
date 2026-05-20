#!/usr/bin/env python3
"""
Consolidated patch — reads Phase 01 uploads/index.html, applies all
outstanding changes cleanly in one pass, writes complete output.
"""
import sys

INPUT  = '/sessions/adoring-intelligent-curie/mnt/uploads/index.html'
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

# 1. LOGO_B64 – tiny 1×1 transparent PNG placeholder hardcoded.
#    User swaps the string for their real logo base64 when ready.
rep(
    '// ── PDF BUILDERS ──────────────────────────────────────────────────────────────\nfunction buildClientPDF(proj){',
    "// ── LOGO ───────────────────────────────────────────────────────────────────────\n// To use your own logo: base64 -i logo.png | tr -d '\\n'  → paste result below.\nvar LOGO_B64='iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==';\n\n// ── PDF BUILDERS ──────────────────────────────────────────────────────────────\nfunction buildClientPDF(proj){",
    'LOGO_B64 constant'
)

# 2. Logo in BOTH PDF builder headers (identical branding HTML in each).
OLD_BRAND = (
    "      '<div><div style=\"font-size:22pt;font-weight:900;letter-spacing:.02em\">"
    "LSC CREATIVE<span style=\"color:#B85444\">.</span></div>'+\n"
    "      '<div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.12em;"
    "color:#888;margin-top:4px\">Motion Productions</div></div>'+"
)
NEW_BRAND = (
    "      (LOGO_B64?'<img src=\"data:image/png;base64,'+LOGO_B64+'\" "
    "style=\"height:76px;width:auto;object-fit:contain;display:block\">'"
    ":'<div><div style=\"font-size:22pt;font-weight:900;letter-spacing:.02em\">"
    "LSC CREATIVE<span style=\"color:#B85444\">.</span></div>"
    "<div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.12em;"
    "color:#888;margin-top:4px\">Motion Productions</div></div>')+"
)
rep(OLD_BRAND, NEW_BRAND, 'Logo – buildClientPDF', n=1)
rep(OLD_BRAND, NEW_BRAND, 'Logo – buildClientInvoicePDF', n=1)

# 3. Equipment: aggregate to single line in BOTH PDF builders.
OLD_EQ = (
    "  if(eqActive.length){serviceItems+='<div style=\"margin-bottom:10px;"
    "padding-bottom:8px;border-bottom:1px solid #f0f0f0\">"
    "<div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.1em;"
    "color:#B85444;font-weight:700;margin-bottom:5px\">Equipment Hire</div>'"
    "+eqActive.map(function(e){return'<div style=\"font-size:10pt;color:#181818;"
    "margin-bottom:2px\">'+esc(e.vendor||'Equipment')+'</div>';}).join('')+'</div>';}"
)
NEW_EQ = (
    "  if(eqActive.length){serviceItems+='<div style=\"margin-bottom:10px;"
    "padding-bottom:8px;border-bottom:1px solid #f0f0f0\">"
    "<div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.1em;"
    "color:#B85444;font-weight:700;margin-bottom:5px\">Equipment Hire</div>"
    "<div style=\"font-size:10.5pt;font-weight:600;color:#181818;margin-bottom:3px\">"
    "Equipment Hire</div></div>';}"
)
rep(OLD_EQ, NEW_EQ, 'Equipment aggregation', n=2)

# 4. "Total Investment" → "Project Total" (buildClientPDF)
rep(
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Total Investment <span style=\"font-size:9pt;font-weight:400;color:#aaa\">"
    "inc. all services</span></td>'+",
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Project Total <span style=\"font-size:9pt;font-weight:400;color:#aaa\">"
    "inc. all services</span></td>'+",
    'Project Total – quote PDF'
)

# 5. "Total Due" → "Project Total" (buildClientInvoicePDF)
rep(
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Total Due <span style=\"font-size:9pt;font-weight:400;color:#aaa\">"
    "inc. all services</span></td>'+",
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Project Total <span style=\"font-size:9pt;font-weight:400;color:#aaa\">"
    "inc. all services</span></td>'+",
    'Project Total – invoice PDF'
)

# 6. Remove "Open in Finder" from success toast.
#    The link fires window.electronAPI.openFolder() which can race with fs.writeFile.
#    Removing it eliminates the "unable to open file" timing error entirely.
rep(
    "if(result.success)showToast('✓ '+(isInvoice?'Invoice':'Quote')+' PDF saved to 03 Project Quotes','ok',true);",
    "if(result.success)showToast('✓ '+(isInvoice?'Invoice':'Quote')+' PDF saved','ok',false);",
    'Fix success toast (remove Open-in-Finder race)'
)

print('\nChanges applied: ' + str(ok) + '/6')
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(c)
print('Written: ' + OUTPUT)
