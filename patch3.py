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
        print('MISS: [' + tag + ']', file=sys.stderr); return
    c = c.replace(old, new, n)
    ok += 1
    print('OK(' + str(min(found,n)) + 'x): [' + tag + ']')

# ── 1. Inject LOGO_B64 var + initLogo() async function before PDF builders ───
rep(
    '// ── PDF BUILDERS ──────────────────────────────────────────────────────────────\nfunction buildClientPDF(proj){',
    """// ── LOGO LOADER ────────────────────────────────────────────────────────────────
// Place logo.png in the same folder as index.html — it is loaded automatically at export time.
var LOGO_B64='';
var _logoFetched=false;
async function initLogo(){
  if(_logoFetched)return;
  _logoFetched=true;
  try{
    var r=await fetch('logo.png');
    if(!r.ok&&r.status!==0)return;
    var buf=await r.arrayBuffer();
    var b=new Uint8Array(buf),s='',sz=8192;
    for(var i=0;i<b.length;i+=sz)s+=String.fromCharCode.apply(null,b.subarray(i,Math.min(i+sz,b.length)));
    LOGO_B64=btoa(s);
  }catch(e){LOGO_B64='';}
}

// ── PDF BUILDERS ──────────────────────────────────────────────────────────────
function buildClientPDF(proj){""",
    'LOGO_B64 + initLogo()'
)

# ── 2. Logo in buildClientPDF header ─────────────────────────────────────────
# Original: two string literals for text branding (first occurrence = buildClientPDF)
OLD_BRAND = (
    "      '<div><div style=\"font-size:22pt;font-weight:900;letter-spacing:.02em\">LSC CREATIVE<span style=\"color:#B85444\">.</span></div>'+\n"
    "      '<div style=\"font-size:8pt;text-transform:uppercase;letter-spacing:.12em;color:#888;margin-top:4px\">Motion Productions</div></div>'+"
)
NEW_BRAND_QUOTE = (
    "      (LOGO_B64?'<img src=\"data:image/png;base64,'+LOGO_B64+'\" "
    "style=\"height:76px;width:auto;object-fit:contain;display:block\">'"
    ":'<div><div style=\"font-size:22pt;font-weight:900;letter-spacing:.02em\">LSC CREATIVE"
    "<span style=\"color:#B85444\">.</span></div><div style=\"font-size:8pt;text-transform:uppercase;"
    "letter-spacing:.12em;color:#888;margin-top:4px\">Motion Productions</div></div>')+"
)
rep(OLD_BRAND, NEW_BRAND_QUOTE, 'Logo header – buildClientPDF', n=1)

# ── 3. Logo in buildClientInvoicePDF header (identical branding HTML, 2nd hit) ─
# After step 2 the first occurrence is gone; the 2nd (invoice) is now the only one left.
rep(OLD_BRAND, NEW_BRAND_QUOTE, 'Logo header – buildClientInvoicePDF', n=1)

# ── 4. Equipment: aggregate to single line in buildClientPDF (1st hit) ────────
OLD_EQ = (
    "  if(eqActive.length){serviceItems+='<div style=\"margin-bottom:10px;padding-bottom:8px;"
    "border-bottom:1px solid #f0f0f0\"><div style=\"font-size:8pt;text-transform:uppercase;"
    "letter-spacing:.1em;color:#B85444;font-weight:700;margin-bottom:5px\">Equipment Hire</div>'"
    "+eqActive.map(function(e){return'<div style=\"font-size:10pt;color:#181818;margin-bottom:2px\">'"
    "+esc(e.vendor||'Equipment')+'</div>';}).join('')+'</div>';}"
)
NEW_EQ = (
    "  if(eqActive.length){serviceItems+='<div style=\"margin-bottom:10px;padding-bottom:8px;"
    "border-bottom:1px solid #f0f0f0\"><div style=\"font-size:8pt;text-transform:uppercase;"
    "letter-spacing:.1em;color:#B85444;font-weight:700;margin-bottom:5px\">Equipment Hire</div>"
    "<div style=\"font-size:10.5pt;font-weight:600;color:#181818;margin-bottom:3px\">"
    "Equipment Hire</div></div>';}"
)
rep(OLD_EQ, NEW_EQ, 'Equipment aggregation', n=2)

# ── 5. "Total Investment" → "Project Total" in buildClientPDF ─────────────────
rep(
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Total Investment <span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Project Total <span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    'Total Investment → Project Total'
)

# ── 6. "Total Due" → "Project Total" in buildClientInvoicePDF ────────────────
rep(
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Total Due <span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    "'<td style=\"padding:13px 16px;font-size:13pt;font-weight:800;color:#fff\">"
    "Project Total <span style=\"font-size:9pt;font-weight:400;color:#aaa\">inc. all services</span></td>'+",
    'Total Due → Project Total'
)

# ── 7. Await initLogo() inside doExport before PDF is built ──────────────────
rep(
    "  showToast('Generating PDF…','');\n  var isInvoice=proj.docType==='invoice';",
    "  showToast('Generating PDF…','');\n  await initLogo();\n  var isInvoice=proj.docType==='invoice';",
    'await initLogo() in doExport'
)

print('\nChanges applied: ' + str(ok))
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(c)
print('Written: ' + OUTPUT)
