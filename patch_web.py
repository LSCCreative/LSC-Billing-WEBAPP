#!/usr/bin/env python3
"""
Convert LSC Billing from Electron desktop app → standalone web app.
Changes:
  1. Remove all -webkit-app-region CSS (drag/no-drag — Electron only)
  2. Replace doExport Electron IPC call with browser window.open + window.print()
  3. Fix showToast — remove Electron openFolder reference
  4. Update <title> tag to reflect web context
  5. Remove the Electron-only fallback error message
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

# ── 1. TITLE ──────────────────────────────────────────────────────────────────
rep(
    '<title>LSC Creative — Project Billing</title>',
    '<title>LSC Creative · Project Billing</title>',
    'title tag'
)

# ── 2. REMOVE -webkit-app-region:drag from header ────────────────────────────
rep(
    ';-webkit-app-region:drag}',
    '}',
    'header webkit-app-region:drag'
)

# ── 3. REMOVE -webkit-app-region:no-drag from logo btn ───────────────────────
rep(
    ';-webkit-app-region:no-drag}',
    '}',
    'logo-btn webkit-app-region:no-drag', n=2
)

# ── 4. FIX showToast — remove openFolder / Electron reference ────────────────
rep(
    "  m.innerHTML=msg+(link?'<span class=\"toast-link\" id=\"tl-el\">Open in Finder →</span>':'');\n"
    "  if(link){var el=$id('tl-el');if(el)el.addEventListener('click',function(){window.electronAPI&&window.electronAPI.openFolder();});}",
    "  m.innerHTML=msg;",
    'showToast remove openFolder'
)

# ── 5. REPLACE doExport — swap Electron IPC for browser print ────────────────
rep(
    "  try{\n"
    "    if(window.electronAPI){\n"
    "      var pdfHtml=isInvoice?buildClientInvoicePDF(proj):buildClientPDF(proj);\n"
    "      var result=await window.electronAPI.exportPDF({html:pdfHtml,filename:base+'.pdf'});\n"
    "      if(result.success)showToast('✓ '+(isInvoice?'Invoice':'Quote')+' PDF saved','ok',false);\n"
    "      else showToast('⚠ Export issue: '+(result.error||'Unknown error'),'err');\n"
    "    }else showToast('Run inside the desktop app to export','err');\n"
    "  }catch(e){alert('EXPORT ERROR: '+String(e));showToast('⚠ Export failed — see alert','err');}",

    "  try{\n"
    "    var pdfHtml=isInvoice?buildClientInvoicePDF(proj):buildClientPDF(proj);\n"
    "    var win=window.open('','_blank');\n"
    "    if(!win){showToast('⚠ Pop-up blocked — allow pop-ups for this site','err');return;}\n"
    "    win.document.write(pdfHtml);\n"
    "    win.document.close();\n"
    "    win.focus();\n"
    "    setTimeout(function(){\n"
    "      win.print();\n"
    "      showToast('✓ '+(isInvoice?'Invoice':'Quote')+' PDF ready — save from print dialog','ok',false);\n"
    "    },400);\n"
    "  }catch(e){showToast('⚠ Export failed: '+String(e),'err');}",

    'doExport → browser print'
)

print('\nChanges applied: ' + str(ok) + '/5')
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(c)
print('Written: ' + OUTPUT)
