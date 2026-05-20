#!/usr/bin/env python3
"""
patch_logo_cards.py
1. Replace canvas logo loader with fetch+FileReader (works under file://)
2. Add .card-link-bar CSS
3. Inject link bar HTML into each project card
4. Wire copy-link event bindings in renderList
"""
import sys

PATH = '/sessions/adoring-intelligent-curie/mnt/LSC Billing App [Phase 01]/index.html'

with open(PATH, 'r', encoding='utf-8') as f:
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

# ── 1. LOGO LOADER: canvas → fetch + FileReader ───────────────────────────────
rep(
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

    "var LOGO_B64='';\n"
    "(function(){\n"
    "  fetch('uploads/logo.png')\n"
    "    .then(function(r){if(!r.ok)throw new Error('logo 404');return r.blob();})\n"
    "    .then(function(b){\n"
    "      var fr=new FileReader();\n"
    "      fr.onload=function(e){\n"
    "        LOGO_B64=e.target.result.replace('data:image/png;base64,','');\n"
    "      };\n"
    "      fr.readAsDataURL(b);\n"
    "    })\n"
    "    .catch(function(){});\n"
    "})();",

    'logo loader canvas→fetch+FileReader'
)

# ── 2. CARD LINK BAR CSS (inject after .card-date rule) ──────────────────────
rep(
    '.card-date{color:var(--muted);font-size:10px}',

    '.card-date{color:var(--muted);font-size:10px}'
    '\n.card-link-bar{display:flex;align-items:center;gap:6px;margin-top:11px;padding-top:11px;border-top:1px solid var(--border)}'
    '\n.card-link-url{flex:1;font-family:monospace;font-size:10px;color:var(--muted);background:rgba(240,237,232,0.05);padding:4px 8px;border-radius:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:default}'
    '\n.card-link-copy{flex-shrink:0;font-size:9px;padding:3px 9px;border:1px solid var(--accent);color:var(--accent);background:none;cursor:pointer;letter-spacing:.07em;text-transform:uppercase;border-radius:2px;transition:background .15s,color .15s;font-family:inherit}'
    '\n.card-link-copy:hover{background:var(--accent);color:#F0EDE8}'
    '\n.card-link-copy.copied{border-color:var(--text);color:var(--text);background:rgba(240,237,232,0.08)}',

    'card-link-bar CSS'
)

# ── 3. CARD HTML: inject link bar before closing </div> ───────────────────────
rep(
    "        '<div class=\"card-foot\"><div class=\"card-date\">'+esc(p.date||'—')+'</div><div class=\"tag\">'+esc(p.clientName||'—')+'</div></div>'+\n"
    "      '</div>';",

    "        '<div class=\"card-foot\"><div class=\"card-date\">'+esc(p.date||'—')+'</div><div class=\"tag\">'+esc(p.clientName||'—')+'</div></div>'+\n"
    "        '<div class=\"card-link-bar\">'+\n"
    "          '<span class=\"card-link-url\">'+(p.upid||('EST-'+p.id))+'</span>'+\n"
    "          '<button class=\"card-link-copy\" data-cupid=\"'+(p.upid||('EST-'+p.id))+'\">Copy Link</button>'+\n"
    "        '</div>'+\n"
    "      '</div>';",

    'card link bar HTML'
)

# ── 4. RENDERLIST: wire copy-link event bindings ──────────────────────────────
rep(
    "  qsa('.proj-card',el).forEach(function(c){c.addEventListener('click',function(){viewingId=parseInt(c.dataset.id);view='estimate';render();});});",

    "  qsa('.proj-card',el).forEach(function(c){c.addEventListener('click',function(){viewingId=parseInt(c.dataset.id);view='estimate';render();});});\n"
    "  qsa('.card-link-copy',el).forEach(function(btn){\n"
    "    btn.addEventListener('click',function(e){\n"
    "      e.stopPropagation();\n"
    "      var upid=btn.dataset.cupid;\n"
    "      var url=window.location.href.split('#')[0]+'#'+upid;\n"
    "      navigator.clipboard.writeText(url).then(function(){\n"
    "        var orig=btn.textContent;\n"
    "        btn.textContent='✓ Copied';\n"
    "        btn.classList.add('copied');\n"
    "        setTimeout(function(){btn.textContent=orig;btn.classList.remove('copied');},2000);\n"
    "      }).catch(function(){});\n"
    "    });\n"
    "  });",

    'card copy-link event bindings'
)

print('\nChanges applied: ' + str(ok) + '/4')
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(c)
print('Written: ' + PATH)
