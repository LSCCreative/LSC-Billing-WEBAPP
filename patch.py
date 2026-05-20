#!/usr/bin/env python3
import sys

INPUT = '/sessions/adoring-intelligent-curie/mnt/uploads/index.html'
OUTPUT = '/sessions/adoring-intelligent-curie/mnt/LSC Billing App [Phase 01]/index.html'

with open(INPUT, 'r', encoding='utf-8') as f:
    c = f.read()

changes = 0

def rep(old, new, tag):
    global c, changes
    if old not in c:
        print('WARNING: could not find [' + tag + ']', file=sys.stderr)
        return
    c = c.replace(old, new, 1)
    changes += 1
    print('OK: [' + tag + ']')

# ── 1. CSS ──────────────────────────────────────────────────────────────────
rep(
    '.saved-msg{color:#6fcf6f;font-size:11px;display:none}\n</style>',
    """.saved-msg{color:#6fcf6f;font-size:11px;display:none}
/* Invoice Settings Modal */
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:9000;display:none;align-items:center;justify-content:center}
.modal-overlay.open{display:flex}
.modal-box{background:var(--surface);border:1px solid var(--border);width:500px;max-width:95vw;padding:28px 32px}
.modal-title{font-family:'Delight','Georgia',serif;font-weight:700;font-size:20px;color:var(--text);margin-bottom:20px}
.modal-actions{display:flex;gap:10px;justify-content:flex-end;padding-top:18px;border-top:1px solid var(--border);margin-top:18px}
/* Doc type bar */
.doc-type-bar{display:flex;align-items:center;gap:12px;padding:12px 0 18px;margin-bottom:16px}
.doc-type-label{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);white-space:nowrap}
.doc-type-select{background:var(--surface);border:1px solid var(--border);color:var(--text);font-size:12px;padding:6px 10px;outline:none;cursor:pointer;transition:.15s}
.doc-type-select:focus{border-color:var(--accent)}
.inv-num-wrap{display:none;align-items:center;gap:8px}
.inv-num-wrap.show{display:flex}
.inv-num-inp{background:var(--surface);border:1px solid var(--accent);color:var(--text);font-size:12px;padding:6px 10px;outline:none;width:130px;font-family:'Funnel Sans',sans-serif}
.inv-num-inp:focus{border-color:var(--text)}
</style>""",
    'CSS additions'
)

# ── 2. Nav button ────────────────────────────────────────────────────────────
rep(
    '    <button class="nav-link" id="nav-pricing">Pricing</button>\n  </div>',
    '    <button class="nav-link" id="nav-pricing">Pricing</button>\n    <button class="nav-link" id="nav-invoice-settings">Invoice Settings</button>\n  </div>',
    'Nav button'
)

# ── 3. Modal HTML before <script> ────────────────────────────────────────────
rep(
    '<script>\n(function(){\n\'use strict\';',
    """<div class="modal-overlay" id="modal-invoice-settings">
  <div class="modal-box">
    <div class="modal-title">Invoice Settings</div>
    <div class="form-grid">
      <div class="field"><label>Bank Name</label><input id="inv-bank-name" type="text" placeholder="e.g. Commonwealth Bank"></div>
      <div class="field"><label>Account Name</label><input id="inv-account-name" type="text" placeholder="e.g. LSC Creative Pty Ltd"></div>
      <div class="field"><label>BSB</label><input id="inv-bsb" type="text" placeholder="e.g. 062-000"></div>
      <div class="field"><label>Account Number</label><input id="inv-account-num" type="text" placeholder="e.g. 12345678"></div>
      <div class="field full"><label>Payment Terms</label><textarea id="inv-payment-terms" placeholder="e.g. Strictly 14 Days — EFT only. Please reference invoice number."></textarea></div>
    </div>
    <div class="modal-actions">
      <button class="btn btn-ghost btn-sm" id="btn-close-inv-settings">Cancel</button>
      <button class="btn btn-accent" id="btn-save-inv-settings">Save Details</button>
    </div>
  </div>
</div>
<script>
(function(){
'use strict';""",
    'Modal HTML'
)

# ── 4. Invoice settings persistence helpers ──────────────────────────────────
rep(
    "var projects=[],nextId=1,view='list',editProj=null,viewingId=null;",
    """var projects=[],nextId=1,view='list',editProj=null,viewingId=null;

// Invoice settings persistence
function loadInvoiceSettings(){
  try{return JSON.parse(localStorage.getItem('lsc-invoice-settings')||'{}');}catch(e){return{};}
}
function saveInvoiceSettings(s){
  try{localStorage.setItem('lsc-invoice-settings',JSON.stringify(s));}catch(e){}
}""",
    'Invoice settings helpers'
)

# ── 5. Nav-invoice-settings event listener ───────────────────────────────────
rep(
    "$id('nav-pricing').addEventListener('click',function(){view='pricing';render();});",
    "$id('nav-pricing').addEventListener('click',function(){view='pricing';render();});\n$id('nav-invoice-settings').addEventListener('click',function(){openInvoiceSettingsModal();});",
    'Nav invoice listener'
)

# ── 6. Doc type badge on list cards ─────────────────────────────────────────
rep(
    "'<div class=\"card-gross-label\">Net Invoice</div>'+",
    """'<div style=\"margin-bottom:8px\">'+(p.docType==='invoice'?'<span style=\"font-size:9px;padding:2px 7px;border:1px solid var(--accent);color:var(--accent);letter-spacing:.05em\">INVOICE</span>':'<span style=\"font-size:9px;padding:2px 7px;border:1px solid var(--border);color:var(--muted);letter-spacing:.05em\">ESTIMATE</span>')+'</div>'+
        '<div class=\"card-gross-label\">Net Invoice</div>'+""",
    'List card badge'
)

# ── 7. Doc type bar in renderForm ────────────────────────────────────────────
rep(
    "    '<div class=\"field full\"><label>Internal Notes</label><textarea id=\"f-notes\">'+esc(p?p.notes||'':'')+'</textarea></div>'+\n  '</div>';",
    """    '<div class=\"field full\"><label>Internal Notes</label><textarea id=\"f-notes\">'+esc(p?p.notes||'':'')+'</textarea></div>'+
  '</div>'+
  '<div class=\"doc-type-bar\">'+
    '<span class=\"doc-type-label\">Document Type</span>'+
    '<select class=\"doc-type-select\" id=\"f-doctype\">'+
      '<option value=\"estimate\"'+(p&&p.docType==='invoice'?'':' selected')+'>Estimate</option>'+
      '<option value=\"invoice\"'+(p&&p.docType==='invoice'?' selected':'')+'>Invoice</option>'+
    '</select>'+
    '<div class=\"inv-num-wrap'+(p&&p.docType==='invoice'?' show':'')+'\" id=\"inv-num-wrap\">'+
      '<label style=\"font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--accent)\">Invoice #</label>'+
      '<input class=\"inv-num-inp\" id=\"f-invnum\" type=\"text\" placeholder=\"e.g. INV-001\" value=\"'+esc(p&&p.invoiceNumber||'')+'\">'+
    '</div>'+
  '</div>';""",
    'Doc type bar in form'
)

# ── 8. bindFormGlobal – docType toggle binding ───────────────────────────────
rep(
    "  var del=$id('js-del');if(del)del.addEventListener('click',deleteProject);",
    """  var del=$id('js-del');if(del)del.addEventListener('click',deleteProject);
  var dtSel=$id('f-doctype');var invWrap=$id('inv-num-wrap');
  if(dtSel){dtSel.addEventListener('change',function(){if(invWrap)invWrap.classList.toggle('show',this.value==='invoice');});}""",
    'bindFormGlobal docType toggle'
)

# ── 9. saveProject – add docType + invoiceNumber ─────────────────────────────
rep(
    "    notes:($id('f-notes')&&$id('f-notes').value||'').trim(),",
    """    notes:($id('f-notes')&&$id('f-notes').value||'').trim(),
    docType:($id('f-doctype')&&$id('f-doctype').value)||'estimate',
    invoiceNumber:($id('f-invnum')&&$id('f-invnum').value||'').trim(),""",
    'saveProject docType'
)

# ── 10. renderEstimate – export button text ──────────────────────────────────
rep(
    "'<button class=\"btn btn-accent btn-sm\" id=\"js-export\"><span class=\"spinner\" id=\"exp-spin\"></span>↑ Export Quote PDF</button>'+",
    "'<button class=\"btn btn-accent btn-sm\" id=\"js-export\"><span class=\"spinner\" id=\"exp-spin\"></span>↑ '+(proj.docType==='invoice'?'Export Client Invoice':'Export Quote PDF')+'</button>'+",
    'Export button text'
)

# ── 11. renderEstimate – invoice badge in header ─────────────────────────────
rep(
    "      '<div class=\"est-upid\">'+esc(proj.upid||'—')+'</div>'+",
    "      '<div class=\"est-upid\">'+esc(proj.upid||'—')+(proj.docType==='invoice'?' &nbsp;<span style=\"font-size:9px;padding:2px 7px;border:1px solid var(--accent);color:var(--accent);letter-spacing:.05em\">INVOICE '+esc(proj.invoiceNumber||'—')+'</span>':'')+'</div>'+",
    'Estimate header badge'
)

# ── 12. buildClientInvoicePDF function ───────────────────────────────────────
INVOICE_PDF_FN = """
// ── INVOICE PDF BUILDER ────────────────────────────────────────────────────────────────────────────
function buildClientInvoicePDF(proj){
  var ar=proj.activeRows||{};
  var serviceItems='';
  labourSections.forEach(function(sec){
    var rows=(ar[sec.id]||[]).filter(function(s){return(s.qty||0)>0;});if(!rows.length)return;
    serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0f0f0">'+
      '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#B85444;font-weight:700;margin-bottom:5px">'+esc(sec.label)+'</div>';
    rows.forEach(function(s){serviceItems+='<div style="font-size:10.5pt;font-weight:600;color:#181818;margin-bottom:3px">'+esc(s.name)+'</div>';});
    serviceItems+='</div>';
  });
  var eqActive=(ar.equip||[]).filter(function(e){return e.vendor||(e.days&&e.cost);});
  if(eqActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0f0f0"><div style="font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#B85444;font-weight:700;margin-bottom:5px">Equipment Hire</div>'+eqActive.map(function(e){return'<div style="font-size:10pt;color:#181818;margin-bottom:2px">'+esc(e.vendor||'Equipment')+'</div>';}).join('')+'</div>';}
  var tvActive=(ar.travel||[]).filter(function(t){return(t.qty||0)>0;});
  if(tvActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0f0f0"><div style="font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#B85444;font-weight:700;margin-bottom:5px">Travel &amp; Accommodation</div>'+tvActive.map(function(s){return'<div style="font-size:10pt;color:#181818;margin-bottom:2px">'+esc(s.name)+'</div>';}).join('')+'</div>';}
  var crActive=(ar.crew||[]).filter(function(c){return c.role||(c.days&&c.cost);});
  if(crActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0f0f0"><div style="font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#B85444;font-weight:700;margin-bottom:5px">External Crew &amp; Contracts</div>'+crActive.map(function(c){return'<div style="font-size:10pt;color:#181818;margin-bottom:2px">'+esc(c.role||'Crew Member')+'</div>';}).join('')+'</div>';}
  var invSettings=loadInvoiceSettings();
  var payBlock='';
  if(invSettings.bankName||invSettings.accountName||invSettings.bsb||invSettings.accountNumber||invSettings.paymentTerms){
    payBlock='<div style="margin-top:28px;padding-top:20px;border-top:2px solid #181818">'+
      '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.12em;color:#888;font-weight:700;margin-bottom:14px;padding-bottom:6px;border-bottom:2px solid #181818">Payment Details</div>'+
      '<table style="width:100%;border-collapse:collapse;font-size:10.5pt"><tbody>'+
      (invSettings.bankName?'<tr><td style="padding:5px 0;color:#888;width:160px">Bank</td><td style="padding:5px 0;font-weight:600;color:#181818">'+esc(invSettings.bankName)+'</td></tr>':'')+
      (invSettings.accountName?'<tr><td style="padding:5px 0;color:#888">Account Name</td><td style="padding:5px 0;font-weight:600;color:#181818">'+esc(invSettings.accountName)+'</td></tr>':'')+
      (invSettings.bsb?'<tr><td style="padding:5px 0;color:#888">BSB</td><td style="padding:5px 0;font-weight:600;color:#181818">'+esc(invSettings.bsb)+'</td></tr>':'')+
      (invSettings.accountNumber?'<tr><td style="padding:5px 0;color:#888">Account Number</td><td style="padding:5px 0;font-weight:600;color:#181818">'+esc(invSettings.accountNumber)+'</td></tr>':'')+
      '</tbody></table>'+
      (invSettings.paymentTerms?'<div style="margin-top:12px;padding:12px 16px;background:#f7f7f7;border-left:3px solid #B85444"><div style="font-size:8pt;text-transform:uppercase;letter-spacing:.08em;color:#888;margin-bottom:4px;font-weight:700">Payment Terms</div><div style="font-size:10pt;color:#181818;line-height:1.6">'+esc(invSettings.paymentTerms)+'</div></div>':'')+
    '</div>';
  }
  var drows=(proj.activeRows&&proj.activeRows.deliverables||[]).filter(function(d){return d.name;});
  var delivTable='';
  if(drows.length){
    delivTable='<div style="margin-bottom:28px"><div class="sh">Deliverables</div>'+
      '<table style="width:100%;border-collapse:collapse;font-size:10pt"><thead><tr style="background:#f7f7f7">'+
        '<th style="text-align:left;padding:8px 12px;font-size:8pt;text-transform:uppercase;color:#888;border-bottom:1px solid #e8e8e8">Deliverable</th>'+
        '<th style="text-align:right;padding:8px 12px;font-size:8pt;text-transform:uppercase;color:#888;border-bottom:1px solid #e8e8e8">Format</th>'+
        '<th style="text-align:right;padding:8px 12px;font-size:8pt;text-transform:uppercase;color:#888;border-bottom:1px solid #e8e8e8">Duration</th>'+
        '<th style="text-align:right;padding:8px 12px;font-size:8pt;text-transform:uppercase;color:#888;border-bottom:1px solid #e8e8e8">Qty</th>'+
      '</tr></thead><tbody>'+
      drows.map(function(d,i){var bg=i%2===0?'#fff':'#fafafa';return'<tr style="background:'+bg+'"><td style="padding:8px 12px;font-weight:600;color:#181818">'+esc(d.name)+'</td><td style="text-align:right;padding:8px 12px;color:#555">'+esc(d.format||'—')+'</td><td style="text-align:right;padding:8px 12px;color:#555">'+esc(d.duration||'—')+'</td><td style="text-align:right;padding:8px 12px;font-weight:700;color:#B85444">'+esc(String(d.qty||1))+'</td></tr>';}).join('')+
      '</tbody></table></div>';
  }
  return'<!DOCTYPE html><html><head><meta charset="UTF-8"><style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:Arial,Helvetica,sans-serif;font-size:11pt;color:#181818;background:#fff;padding:40px 32px;max-width:700px;margin:0 auto}.sh{font-size:8pt;text-transform:uppercase;letter-spacing:.12em;color:#888;font-weight:700;margin-bottom:10px;padding-bottom:6px;border-bottom:2px solid #181818}</style></head><body>'+
    '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:28px;padding-bottom:16px;border-bottom:3px solid #181818">'+
      '<div><div style="font-size:22pt;font-weight:900;letter-spacing:.02em">LSC CREATIVE<span style="color:#B85444">.</span></div>'+
      '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.12em;color:#888;margin-top:4px">Motion Productions</div></div>'+
      '<div style="text-align:right">'+
      '<div style="font-size:16pt;font-weight:900;color:#181818;letter-spacing:.02em">INVOICE <span style="color:#B85444">'+esc(proj.invoiceNumber||'—')+'</span></div>'+
      '<div style="font-size:9pt;color:#888;margin-top:2px">'+esc(proj.date||'')+'</div>'+
      '<div style="font-size:15pt;font-weight:800;color:#181818;margin-top:6px">'+esc(proj.name)+'</div>'+
      (proj.businessName?'<div style="font-size:10pt;color:#555;margin-top:3px;font-weight:500">'+esc(proj.businessName)+'</div>':'')+
      (proj.clientName?'<div style="font-size:9.5pt;color:#888;margin-top:2px">'+esc(proj.clientName)+(proj.clientEmail?' &middot; '+esc(proj.clientEmail):'')+'</div>':'')+
      '</div></div>'+
    delivTable+
    '<div style="margin-bottom:28px"><div class="sh">What Goes Into This Project</div>'+serviceItems+'</div>'+
    '<div style="margin-bottom:0"><div class="sh">Invoice Total</div>'+
      '<div style="border:1px solid #e8e8e8;display:inline-block;min-width:290px"><table style="width:100%;border-collapse:collapse"><tr style="background:#181818">'+
        '<td style="padding:13px 16px;font-size:13pt;font-weight:800;color:#fff">Total Due <span style="font-size:9pt;font-weight:400;color:#aaa">inc. all services</span></td>'+
        '<td style="padding:13px 16px;text-align:right;font-size:15pt;font-weight:900;color:#B85444">'+fmt(proj.net)+'</td>'+
      '</tr></table></div>'+
      '<div style="margin-top:10px;font-size:8.5pt;color:#aaa">All prices in AUD. GST not included.</div></div>'+
    payBlock+
    '</body></html>';
}

"""

rep(
    'async function doExport(proj,idx){',
    INVOICE_PDF_FN + 'async function doExport(proj,idx){',
    'buildClientInvoicePDF'
)

# ── 13. doExport – check docType ─────────────────────────────────────────────
OLD_EXPORT = (
    "  var base=(proj.upid||'EST-'+pad(idx+1))+' - '+(proj.businessName||'Client')+' - '+proj.name;\n"
    "  try{\n"
    "    if(window.electronAPI){\n"
    "      var result=await window.electronAPI.exportPDF({html:buildClientPDF(proj),filename:base+'.pdf'});\n"
    "      if(result.success)showToast('✓ Quote PDF saved to 03 Project Quotes','ok',true);\n"
    "      else showToast('⚠ Export issue: '+(result.error||'Unknown error'),'err');\n"
    "    }else showToast('Run inside the desktop app to export','err');"
)
NEW_EXPORT = (
    "  var isInvoice=proj.docType==='invoice';\n"
    "  var prefix=isInvoice?(proj.invoiceNumber||'INV'):(proj.upid||'EST-'+pad(idx+1));\n"
    "  var base=prefix+' - '+(proj.businessName||'Client')+' - '+proj.name;\n"
    "  try{\n"
    "    if(window.electronAPI){\n"
    "      var pdfHtml=isInvoice?buildClientInvoicePDF(proj):buildClientPDF(proj);\n"
    "      var result=await window.electronAPI.exportPDF({html:pdfHtml,filename:base+'.pdf'});\n"
    "      if(result.success)showToast('✓ '+(isInvoice?'Invoice':'Quote')+' PDF saved to 03 Project Quotes','ok',true);\n"
    "      else showToast('⚠ Export issue: '+(result.error||'Unknown error'),'err');\n"
    "    }else showToast('Run inside the desktop app to export','err');"
)
rep(OLD_EXPORT, NEW_EXPORT, 'doExport logic')

# ── 14. Invoice Settings modal functions + final render() ────────────────────
rep(
    'render();\n})();',
    """// ── INVOICE SETTINGS MODAL ────────────────────────────────────────────────────────────────────────────
function openInvoiceSettingsModal(){
  var s=loadInvoiceSettings();
  var f=$id('inv-bank-name');if(f)f.value=s.bankName||'';
  var a=$id('inv-account-name');if(a)a.value=s.accountName||'';
  var b=$id('inv-bsb');if(b)b.value=s.bsb||'';
  var n=$id('inv-account-num');if(n)n.value=s.accountNumber||'';
  var t=$id('inv-payment-terms');if(t)t.value=s.paymentTerms||'';
  var overlay=$id('modal-invoice-settings');
  if(overlay)overlay.classList.add('open');
}
function closeInvoiceSettingsModal(){
  var overlay=$id('modal-invoice-settings');
  if(overlay)overlay.classList.remove('open');
}
$id('btn-close-inv-settings').addEventListener('click',closeInvoiceSettingsModal);
$id('btn-save-inv-settings').addEventListener('click',function(){
  var s={
    bankName:($id('inv-bank-name')&&$id('inv-bank-name').value||'').trim(),
    accountName:($id('inv-account-name')&&$id('inv-account-name').value||'').trim(),
    bsb:($id('inv-bsb')&&$id('inv-bsb').value||'').trim(),
    accountNumber:($id('inv-account-num')&&$id('inv-account-num').value||'').trim(),
    paymentTerms:($id('inv-payment-terms')&&$id('inv-payment-terms').value||'').trim()
  };
  saveInvoiceSettings(s);
  closeInvoiceSettingsModal();
  showToast('✓ Invoice settings saved','ok');
});
$id('modal-invoice-settings').addEventListener('click',function(e){
  if(e.target===this)closeInvoiceSettingsModal();
});

render();
})();""",
    'Invoice Settings modal JS + render'
)

print('\\nTotal changes applied: ' + str(changes))

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(c)

print('Written to: ' + OUTPUT)
