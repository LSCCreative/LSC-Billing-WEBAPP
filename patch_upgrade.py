#!/usr/bin/env python3
"""
patch_upgrade.py — LSC Billing Web App Upgrade
1.  Font paths: replace base64 lines 8-9 with relative file paths
2.  Canvas logo loader replacing LOGO_B64 placeholder
3.  App header: add <img src="uploads/logo.png">
4.  Eliminate sage green: --hover:#4CAF82 → #C0603C; PDF a{color} × 2
5.  "Your Investment" → "Project Estimate"
6.  @page margin: 0 → .5in (both PDF builders)
7.  Share panel: CSS + HTML + JS (copy-link, copy-email, hash nav)
8.  Hash navigation on page load
"""
import sys

PATH = '/sessions/adoring-intelligent-curie/mnt/LSC Billing App [Phase 01]/index.html'

with open(PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

ok = 0

# ── 1. FONT PATHS (line-based, lines 8 and 9, index 7 and 8) ──────────────────
if lines[7].startswith("@font-face{font-family:'Delight';src:url('data:font"):
    lines[7] = "@font-face{font-family:'Delight';src:url('uploads/Delight-VF.ttf')format('truetype');font-weight:100 900;font-style:normal}\n"
    ok += 1
    print("OK [font line 8 → Delight-VF.ttf]")
else:
    print("MISS [font line 8]", file=sys.stderr)

if lines[8].startswith("@font-face{font-family:'Delight';src:url('data:font"):
    lines[8] = "@font-face{font-family:'FunnelSans';src:url('uploads/FunnelSans-Light.ttf')format('truetype');font-weight:300;font-style:normal}\n"
    ok += 1
    print("OK [font line 9 → FunnelSans-Light.ttf]")
else:
    print("MISS [font line 9]", file=sys.stderr)

c = ''.join(lines)

def rep(old, new, tag, n=1):
    global c, ok
    found = c.count(old)
    if found == 0:
        print('MISS [' + tag + ']', file=sys.stderr); return
    c = c.replace(old, new, n)
    ok += 1
    print('OK(' + str(min(found, n)) + 'x) [' + tag + ']')

# ── 2. SAGE GREEN: --hover token ───────────────────────────────────────────────
rep('--hover:#4CAF82;', '--hover:#C0603C;', 'hover token sage→terra')

# ── 3. SAGE GREEN: PDF a{color} × 2 ──────────────────────────────────────────
rep(
    'a{color:#4CAF82;text-decoration:none}',
    'a{color:#C0603C;text-decoration:none}',
    'PDF a color ×2',
    n=2
)

# ── 4. "Your Investment" → "Project Estimate" ─────────────────────────────────
rep(
    "'>Your Investment</div>'",
    "'>Project Estimate</div>'",
    'Your Investment → Project Estimate'
)

# ── 5. @page MARGIN 0 → .5in (both PDF builders) ─────────────────────────────
rep(
    '@page{size:letter;margin:0}',
    '@page{size:letter;margin:.5in}',
    '@page margin ×2',
    n=2
)

# ── 6. CANVAS LOGO LOADER ──────────────────────────────────────────────────────
rep(
    "var LOGO_B64='iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==';",
    "var LOGO_B64='';\n"
    "(function(){\n"
    "  var _li=new Image();\n"
    "  _li.onload=function(){\n"
    "    var _lc=document.createElement('canvas');\n"
    "    _lc.width=_li.width;_lc.height=_li.height;\n"
    "    var _lx=_lc.getContext('2d');_lx.drawImage(_li,0,0);\n"
    "    LOGO_B64=_lc.toDataURL('image/png').replace('data:image/png;base64,','');\n"
    "  };\n"
    "  _li.onerror=function(){};\n"
    "  _li.src='uploads/logo.png';\n"
    "})();",
    'LOGO_B64 canvas loader'
)

# ── 7. APP HEADER: add logo img ───────────────────────────────────────────────
rep(
    '  <button id="logo-btn">\n    <span class="logo-text">LSC CREATIVE<em>.</em></span>',
    '  <button id="logo-btn">\n'
    '    <img src="uploads/logo.png" id="app-logo-img" alt="LSC Creative" onerror="this.style.display=\'none\'">\n'
    '    <span class="logo-text">LSC CREATIVE<em>.</em></span>',
    'header logo img'
)

# ── 8. SHARE PANEL CSS (inject before closing </style>) ───────────────────────
rep(
    '.inv-num-inp:focus{border-color:var(--text)}',
    '.inv-num-inp:focus{border-color:var(--text)}'
    '\n#share-panel{position:fixed;bottom:0;left:0;right:0;background:var(--surface);border-top:1px solid var(--border);padding:10px 28px;display:none;align-items:center;gap:10px;z-index:200}'
    '\n#share-panel.active{display:flex}'
    '\n#share-url-input{flex:1;background:var(--bg);border:1px solid var(--border);color:var(--muted);font-size:11px;padding:6px 10px;border-radius:4px;font-family:monospace;outline:none}'
    '\n#share-url-input:focus{border-color:var(--accent)}'
    '\n.share-label{font-size:10px;text-transform:uppercase;letter-spacing:.18em;color:var(--muted);white-space:nowrap}'
    '\n@media print{#share-panel{display:none!important}}',
    'share panel CSS'
)

# ── 9. SHARE PANEL HTML (inject after </header>) ──────────────────────────────
rep(
    '</header>\n<div id="main"></div>',
    '</header>\n'
    '<div id="share-panel">\n'
    '  <span class="share-label">Share Estimate</span>\n'
    '  <input type="text" id="share-url-input" readonly>\n'
    '  <button class="btn btn-sm" id="share-copy-link">Copy Link</button>\n'
    '  <button class="btn btn-accent btn-sm" id="share-copy-email">Copy Email Template</button>\n'
    '</div>\n'
    '<div id="main"></div>',
    'share panel HTML'
)

# ── 10. SHARE PANEL JS in renderEstimate ──────────────────────────────────────
rep(
    "  $id('js-back').addEventListener('click',function(){view='list';render();});\n"
    "  $id('js-edit').addEventListener('click',function(){editProj=proj;view='form';render();});\n"
    "  $id('js-export').addEventListener('click',function(){doExport(proj,idx);});",

    "  $id('js-back').addEventListener('click',function(){\n"
    "    window.location.hash='';\n"
    "    var _sp=$id('share-panel');if(_sp)_sp.classList.remove('active');\n"
    "    view='list';render();\n"
    "  });\n"
    "  $id('js-edit').addEventListener('click',function(){editProj=proj;view='form';render();});\n"
    "  $id('js-export').addEventListener('click',function(){doExport(proj,idx);});\n"
    "  (function(){\n"
    "    var _upid=proj.upid||('EST-'+String(proj.id).padStart(3,'0'));\n"
    "    window.location.hash=_upid;\n"
    "    var _sp=$id('share-panel'),_su=$id('share-url-input');\n"
    "    if(_sp&&_su){\n"
    "      _su.value=window.location.href;\n"
    "      _sp.classList.add('active');\n"
    "      $id('share-copy-link').onclick=function(){\n"
    "        navigator.clipboard.writeText(_su.value)\n"
    "          .then(function(){showToast('✓ Link copied to clipboard','ok',false);});\n"
    "      };\n"
    "      $id('share-copy-email').onclick=function(){\n"
    "        var _body='Hi '+proj.client+',\\n\\n"
    "I\\'ve put together a project estimate for your review:\\n\\n"
    "'+_su.value+'\\n\\n"
    "The estimate outlines everything discussed — feel free to reach out if you\\'d like to talk through any details.\\n\\n"
    "Looking forward to hearing from you.\\n\\n"
    "Best,\\nLachlan\\nLSC Creative\\nlachlan@creativelsc.com';\n"
    "        navigator.clipboard.writeText(_body)\n"
    "          .then(function(){showToast('✓ Email template copied','ok',false);});\n"
    "      };\n"
    "    }\n"
    "  })();",

    'share panel JS in renderEstimate'
)

# ── 11. HASH NAVIGATION on page load (before final render()) ──────────────────
rep(
    'render();',
    "(function(){\n"
    "  var _h=window.location.hash.replace('#','');\n"
    "  if(_h){\n"
    "    var _p=projects.find(function(x){\n"
    "      return(x.upid||('EST-'+String(x.id).padStart(3,'0')))===_h;\n"
    "    });\n"
    "    if(_p){viewingId=_p.id;view='estimate';}\n"
    "  }\n"
    "})();\n"
    "render();",
    'hash nav on load'
)

print('\nChanges applied: ' + str(ok) + '/11')
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(c)
print('Written: ' + PATH)
