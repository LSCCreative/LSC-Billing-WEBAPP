#!/usr/bin/env python3
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
    print('OK(' + str(min(found,n)) + 'x) [' + tag + ']')

# ── 1. Hidden <img> in body so Electron loads logo.png naturally on startup ───
rep(
    '<div class="export-toast" id="export-toast">\n  <div class="toast-dot" id="toast-dot"></div>\n  <div id="toast-msg"></div>\n</div>',
    '<div class="export-toast" id="export-toast">\n  <div class="toast-dot" id="toast-dot"></div>\n  <div id="toast-msg"></div>\n</div>\n<img id="app-logo" src="logo.png" style="display:none" alt="">',
    'Hidden logo img'
)

# ── 2. LOGO_B64 global + synchronous getLogoB64() before PDF builders ─────────
rep(
    '// ── PDF BUILDERS ──────────────────────────────────────────────────────────────\nfunction buildClientPDF(proj){',
    """// ── LOGO ───────────────────────────────────────────────────────────────────────
// Drop logo.png next to index.html — loaded automatically by Electron on startup.
var LOGO_B64='';
function getLogoB64(){
  var img=$id('app-logo');
  if(!img||!img.complete||img.naturalWidth===0)return'';
  try{
    var cv=document.createElement('canvas');
    cv.width=img.naturalWidth;cv.height=img.naturalHeight;
    cv.getContext('2d').drawImage(img,0,0);
    var d=cv.toDataURL('image/png');
    return d.indexOf(',')>-1?d.split(',')[1]:'';
  }catch(e){return'';}
}

// ── PDF BUILDERS ──────────────────────────────────────────────────────────────
function buildClientPDF(proj){""",
    'LOGO_B64 + getLogoB64()'
)

# ── 3 & 4. Swap text branding for logo img in BOTH PDF headers ───────────────
# The two builders share identical branding HTML — replace both occurrences.
OLD_BRAND = (
    "      '<div><div style=\"font-size:22pt;font-weight:900;letter-spacing:.02em\">"
    "LSC CREATIVE<span style=\"color:#B85444\">.</span></div>'+\n"
    "      '<div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.12em;"
    "color:#888;margin-top:4px\">Motion Productions</div></div>'+"
)
NEW_BRAND = (
    "      (LOGO_B64"
    "?'<img src=\"data:image/png;base64,'+LOGO_B64+'\" "
    "style=\"height:76px;width:auto;object-fit:contain;display:block\">'"
    ":'<div><div style=\"font-size:22pt;font-weight:900;letter-spacing:.02em\">"
    "LSC CREATIVE<span style=\"color:#B85444\">.</span></div>"
    "<div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.12em;"
    "color:#888;margin-top:4px\">Motion Productions</div></div>')+"
)
rep(OLD_BRAND, NEW_BRAND, 'Logo in PDF headers', n=2)

# ── 5. Equipment: single aggregated line in BOTH PDF builders ─────────────────
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

# ── 6. "Total Investment" → "Project Total" (buildClientPDF) ─────────────────
rep(
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Total Investment "
    "<span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Project Total "
    "<span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    'Total Investment → Project Total'
)

# ── 7. "Total Due" → "Project Total" (buildClientInvoicePDF) ─────────────────
rep(
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Total Due "
    "<span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Project Total "
    "<span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    'Total Due → Project Total'
)

# ── 8. Refresh LOGO_B64 synchronously at export time ─────────────────────────
rep(
    "  showToast('Generating PDF…','');\n  var isInvoice=proj.docType==='invoice';",
    "  showToast('Generating PDF…','');\n  LOGO_B64=getLogoB64();\n  var isInvoice=proj.docType==='invoice';",
    'LOGO_B64=getLogoB64() in doExport'
)

print('\nTotal: ' + str(ok) + '/8')
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(c)
print('Written: ' + OUTPUT)
