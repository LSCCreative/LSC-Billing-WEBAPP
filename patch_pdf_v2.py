#!/usr/bin/env python3
"""
PDF v2 — Full template redesign for both PDF builders.
Layout: white upper section → dark lower block (#0E0E0E).
- Letter-size @page rule
- Logo header (max-height:50px)
- Terracotta eyebrows, sage links, warm-white text on dark
- Investment total + contact footer in the lower dark block
- Invoice: payment details also in dark block
"""

INPUT  = '/sessions/adoring-intelligent-curie/mnt/LSC Billing App [Phase 01]/index.html'
OUTPUT = '/sessions/adoring-intelligent-curie/mnt/LSC Billing App [Phase 01]/index.html'

with open(INPUT, 'r', encoding='utf-8') as f:
    c = f.read()

# ── LOCATE BOUNDARIES ────────────────────────────────────────────────────────
# Quote PDF: everything from 'return...' to the closing } before invoice comment
QUOTE_RET_START = "  return'<!DOCTYPE html><html><head><meta charset=\"UTF-8\"><style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:\"Helvetica Neue\",Helvetica,Arial,sans-serif;font-size:11pt;color:#0E0E0E;background:#fff;padding:40px 48px;max-width:740px;margin:0 auto}.sh{font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;font-weight:700;margin-bottom:12px;padding-bottom:7px;border-bottom:1px solid rgba(192,96,60,0.25)}</style></head><body>'"
INVOICE_BOUNDARY  = "\n\n// ── INVOICE PDF BUILDER"
DOEXPORT_BOUNDARY = "\n\nasync function doExport"
INVOICE_FUNC_START = "function buildClientInvoicePDF(proj){"

assert QUOTE_RET_START in c, "MISS: quote return start"
assert INVOICE_BOUNDARY in c, "MISS: invoice builder comment"
assert DOEXPORT_BOUNDARY in c, "MISS: doExport boundary"
assert INVOICE_FUNC_START in c, "MISS: invoice func start"

# ── NEW QUOTE PDF RETURN ──────────────────────────────────────────────────────
NEW_QUOTE_RETURN = """  return'<!DOCTYPE html><html><head><meta charset="UTF-8"><style>*{box-sizing:border-box;margin:0;padding:0}@page{size:letter;margin:0}@media print{.lower{-webkit-print-color-adjust:exact;print-color-adjust:exact;color-adjust:exact}}body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:10.5pt;color:#0E0E0E;background:#fff;width:8.5in;margin:0 auto}.upper{padding:42px 52px 36px;background:#fff}.lower{padding:36px 52px 42px;background:#0E0E0E}.sh{font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;font-weight:700;margin-bottom:12px;padding-bottom:7px;border-bottom:1px solid rgba(192,96,60,0.25)}table{border-collapse:collapse;width:100%}a{color:#4CAF82;text-decoration:none}</style></head><body>'+
    '<div class="upper">'+
      '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:34px;padding-bottom:22px;border-bottom:1px solid rgba(14,14,14,0.1)">'+
        (LOGO_B64?'<img src="data:image/png;base64,'+LOGO_B64+'" style="max-height:50px;width:auto;object-fit:contain;display:block">':'<div><div style="font-size:18pt;font-weight:900;letter-spacing:-.01em;color:#0E0E0E">LSC CREATIVE<span style="color:#C0603C">.</span></div><div style="font-size:8pt;text-transform:uppercase;letter-spacing:.22em;color:#7A7470;margin-top:4px">Motion Productions</div></div>')+
        '<div style="text-align:right">'+
          '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;margin-bottom:6px">Project Quote</div>'+
          '<div style="font-size:11pt;font-weight:700;color:#0E0E0E;letter-spacing:.02em">'+esc(proj.upid||'—')+'</div>'+
          '<div style="font-size:9pt;color:#7A7470;margin-top:3px">'+esc(proj.date||'')+'</div>'+
        '</div>'+
      '</div>'+
      '<div style="margin-bottom:32px">'+
        '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;font-weight:700;margin-bottom:10px">Prepared for</div>'+
        '<div style="font-size:20pt;font-weight:800;color:#0E0E0E;line-height:1.05;letter-spacing:-.01em">'+esc(proj.name)+'</div>'+
        (proj.businessName?'<div style="font-size:11pt;color:#3A4756;margin-top:5px;font-weight:500">'+esc(proj.businessName)+'</div>':'')+
        (proj.clientName?'<div style="font-size:9.5pt;color:#7A7470;margin-top:4px">'+esc(proj.clientName)+(proj.clientEmail?' &middot; <a href="mailto:'+esc(proj.clientEmail)+'">'+esc(proj.clientEmail)+'</a>':'')+'</div>':'')+
      '</div>'+
      (function(){
        var drows=(proj.activeRows&&proj.activeRows.deliverables||[]).filter(function(d){return d.name;});
        if(!drows.length)return'';
        return'<div style="margin-bottom:28px"><div class="sh">Deliverables</div>'+
          '<table style="font-size:10pt"><thead><tr style="background:#F2F0EC">'+
            '<th style="text-align:left;padding:8px 12px;font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid #E8E2D9">Deliverable</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid #E8E2D9">Format</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid #E8E2D9">Duration</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid #E8E2D9">Qty</th>'+
          '</tr></thead><tbody>'+
          drows.map(function(d,i){var bg=i%2===0?'#fff':'#F7F5F2';return'<tr style="background:'+bg+'"><td style="padding:8px 12px;font-weight:600;color:#0E0E0E">'+esc(d.name)+'</td><td style="text-align:right;padding:8px 12px;color:#3A4756">'+esc(d.format||'—')+'</td><td style="text-align:right;padding:8px 12px;color:#3A4756">'+esc(d.duration||'—')+'</td><td style="text-align:right;padding:8px 12px;font-weight:700;color:#C0603C">'+esc(String(d.qty||1))+'</td></tr>';}).join('')+
          '</tbody></table></div>';
      })()+
      '<div style="padding-bottom:8px"><div class="sh">Production Scope</div>'+serviceItems+'</div>'+
    '</div>'+
    '<div class="lower">'+
      '<div style="margin-bottom:26px">'+
        '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;font-weight:700;margin-bottom:14px">Your Investment</div>'+
        '<div style="display:flex;justify-content:space-between;align-items:baseline;padding:14px 0;border-top:1px solid rgba(240,237,232,0.15);border-bottom:1px solid rgba(240,237,232,0.15)">'+
          '<div style="color:#F0EDE8;font-size:13pt;font-weight:700">Project Total <span style="color:#858585;font-size:9pt;font-weight:400">inc. all services</span></div>'+
          '<div style="color:#C0603C;font-size:22pt;font-weight:900;letter-spacing:-.01em">'+fmt(proj.net)+'</div>'+
        '</div>'+
        '<div style="color:#858585;font-size:8pt;margin-top:10px;letter-spacing:.02em">All prices in AUD. GST not included. Quote valid for 30 days from issue date.</div>'+
      '</div>'+
      '<hr style="border:none;border-top:1px solid rgba(240,237,232,0.07);margin:0 0 26px">'+
      '<div style="display:flex;justify-content:space-between;align-items:flex-end">'+
        '<div>'+
          '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.22em;color:#858585;margin-bottom:10px">Questions?</div>'+
          '<div style="font-size:11pt;font-weight:700;color:#F0EDE8">Lachlan Sullivan-Carey</div>'+
          '<a href="mailto:lachlan@creativelsc.com" style="display:block;margin-top:5px;font-size:10pt">lachlan@creativelsc.com</a>'+
          '<div style="color:#858585;font-size:9.5pt;margin-top:3px">04 12 710 836</div>'+
        '</div>'+
        '<div style="text-align:right">'+
          (LOGO_B64?'<img src="data:image/png;base64,'+LOGO_B64+'" style="max-height:34px;width:auto;opacity:.4;display:block;margin-left:auto">':'')+
          '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.2em;color:#858585;margin-top:8px">LSC Creative.</div>'+
        '</div>'+
      '</div>'+
    '</div>'+
  '</body></html>';
}"""

# ── NEW INVOICE PDF FUNCTION ──────────────────────────────────────────────────
NEW_INVOICE_FUNC = """function buildClientInvoicePDF(proj){
  var ar=proj.activeRows||{};
  var serviceItems='';
  labourSections.forEach(function(sec){
    var rows=(ar[sec.id]||[]).filter(function(s){return(s.qty||0)>0;});if(!rows.length)return;
    serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0f0f0">'+
      '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">'+esc(sec.label)+'</div>';
    rows.forEach(function(s){serviceItems+='<div style="font-size:10.5pt;font-weight:600;color:#0E0E0E;margin-bottom:3px">'+esc(s.name)+'</div>';});
    serviceItems+='</div>';
  });
  var eqActive=(ar.equip||[]).filter(function(e){return e.vendor||(e.days&&e.cost);});
  if(eqActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0f0f0"><div style="font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">Equipment Hire</div><div style="font-size:10.5pt;font-weight:600;color:#0E0E0E;margin-bottom:3px">Equipment Hire</div></div>';}
  var tvActive=(ar.travel||[]).filter(function(t){return(t.qty||0)>0;});
  if(tvActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0f0f0"><div style="font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">Travel &amp; Accommodation</div>'+tvActive.map(function(s){return'<div style="font-size:10pt;color:#0E0E0E;margin-bottom:2px">'+esc(s.name)+'</div>';}).join('')+'</div>';}
  var crActive=(ar.crew||[]).filter(function(c){return c.role||(c.days&&c.cost);});
  if(crActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #f0f0f0"><div style="font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">External Crew &amp; Contracts</div>'+crActive.map(function(c){return'<div style="font-size:10pt;color:#0E0E0E;margin-bottom:2px">'+esc(c.role||'Crew Member')+'</div>';}).join('')+'</div>';}
  var invSettings=loadInvoiceSettings();
  var payBlock='';
  if(invSettings.bankName||invSettings.accountName||invSettings.bsb||invSettings.accountNumber||invSettings.paymentTerms){
    payBlock=
      '<div style="margin-bottom:26px">'+
        '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;font-weight:700;margin-bottom:14px">Payment Details</div>'+
        '<table style="font-size:10.5pt"><tbody>'+
        (invSettings.bankName?'<tr><td style="padding:6px 0;color:#858585;width:160px">Bank</td><td style="padding:6px 0;font-weight:600;color:#F0EDE8">'+esc(invSettings.bankName)+'</td></tr>':'')+
        (invSettings.accountName?'<tr><td style="padding:6px 0;color:#858585">Account Name</td><td style="padding:6px 0;font-weight:600;color:#F0EDE8">'+esc(invSettings.accountName)+'</td></tr>':'')+
        (invSettings.bsb?'<tr><td style="padding:6px 0;color:#858585">BSB</td><td style="padding:6px 0;font-weight:600;color:#F0EDE8">'+esc(invSettings.bsb)+'</td></tr>':'')+
        (invSettings.accountNumber?'<tr><td style="padding:6px 0;color:#858585">Account Number</td><td style="padding:6px 0;font-weight:600;color:#F0EDE8">'+esc(invSettings.accountNumber)+'</td></tr>':'')+
        '</tbody></table>'+
        (invSettings.paymentTerms?'<div style="margin-top:12px;padding:12px 16px;background:rgba(240,237,232,0.06);border-left:3px solid #C0603C"><div style="font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;margin-bottom:5px;font-weight:700">Payment Terms</div><div style="font-size:10pt;color:#F0EDE8;line-height:1.65">'+esc(invSettings.paymentTerms)+'</div></div>':'')+
      '</div>';
  }
  return'<!DOCTYPE html><html><head><meta charset="UTF-8"><style>*{box-sizing:border-box;margin:0;padding:0}@page{size:letter;margin:0}@media print{.lower{-webkit-print-color-adjust:exact;print-color-adjust:exact;color-adjust:exact}}body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:10.5pt;color:#0E0E0E;background:#fff;width:8.5in;margin:0 auto}.upper{padding:42px 52px 36px;background:#fff}.lower{padding:36px 52px 42px;background:#0E0E0E}.sh{font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;font-weight:700;margin-bottom:12px;padding-bottom:7px;border-bottom:1px solid rgba(192,96,60,0.25)}table{border-collapse:collapse;width:100%}a{color:#4CAF82;text-decoration:none}</style></head><body>'+
    '<div class="upper">'+
      '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:34px;padding-bottom:22px;border-bottom:1px solid rgba(14,14,14,0.1)">'+
        (LOGO_B64?'<img src="data:image/png;base64,'+LOGO_B64+'" style="max-height:50px;width:auto;object-fit:contain;display:block">':'<div><div style="font-size:18pt;font-weight:900;letter-spacing:-.01em;color:#0E0E0E">LSC CREATIVE<span style="color:#C0603C">.</span></div><div style="font-size:8pt;text-transform:uppercase;letter-spacing:.22em;color:#7A7470;margin-top:4px">Motion Productions</div></div>')+
        '<div style="text-align:right">'+
          '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;margin-bottom:6px">Invoice</div>'+
          '<div style="font-size:16pt;font-weight:900;color:#0E0E0E;letter-spacing:-.01em">'+esc(proj.invoiceNumber||'—')+'</div>'+
          '<div style="font-size:9pt;color:#7A7470;margin-top:3px">'+esc(proj.date||'')+'</div>'+
        '</div>'+
      '</div>'+
      '<div style="margin-bottom:32px">'+
        '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;font-weight:700;margin-bottom:10px">Billed to</div>'+
        '<div style="font-size:20pt;font-weight:800;color:#0E0E0E;line-height:1.05;letter-spacing:-.01em">'+esc(proj.name)+'</div>'+
        (proj.businessName?'<div style="font-size:11pt;color:#3A4756;margin-top:5px;font-weight:500">'+esc(proj.businessName)+'</div>':'')+
        (proj.clientName?'<div style="font-size:9.5pt;color:#7A7470;margin-top:4px">'+esc(proj.clientName)+(proj.clientEmail?' &middot; <a href="mailto:'+esc(proj.clientEmail)+'">'+esc(proj.clientEmail)+'</a>':'')+'</div>':'')+
      '</div>'+
      (function(){
        var drows=(proj.activeRows&&proj.activeRows.deliverables||[]).filter(function(d){return d.name;});
        if(!drows.length)return'';
        return'<div style="margin-bottom:28px"><div class="sh">Deliverables</div>'+
          '<table style="font-size:10pt"><thead><tr style="background:#F2F0EC">'+
            '<th style="text-align:left;padding:8px 12px;font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid #E8E2D9">Deliverable</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid #E8E2D9">Format</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid #E8E2D9">Duration</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:8pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid #E8E2D9">Qty</th>'+
          '</tr></thead><tbody>'+
          drows.map(function(d,i){var bg=i%2===0?'#fff':'#F7F5F2';return'<tr style="background:'+bg+'"><td style="padding:8px 12px;font-weight:600;color:#0E0E0E">'+esc(d.name)+'</td><td style="text-align:right;padding:8px 12px;color:#3A4756">'+esc(d.format||'—')+'</td><td style="text-align:right;padding:8px 12px;color:#3A4756">'+esc(d.duration||'—')+'</td><td style="text-align:right;padding:8px 12px;font-weight:700;color:#C0603C">'+esc(String(d.qty||1))+'</td></tr>';}).join('')+
          '</tbody></table></div>';
      })()+
      '<div style="padding-bottom:8px"><div class="sh">Production Scope</div>'+serviceItems+'</div>'+
    '</div>'+
    '<div class="lower">'+
      '<div style="margin-bottom:26px">'+
        '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.28em;color:#C0603C;font-weight:700;margin-bottom:14px">Invoice Total</div>'+
        '<div style="display:flex;justify-content:space-between;align-items:baseline;padding:14px 0;border-top:1px solid rgba(240,237,232,0.15);border-bottom:1px solid rgba(240,237,232,0.15)">'+
          '<div style="color:#F0EDE8;font-size:13pt;font-weight:700">Project Total <span style="color:#858585;font-size:9pt;font-weight:400">inc. all services</span></div>'+
          '<div style="color:#C0603C;font-size:22pt;font-weight:900;letter-spacing:-.01em">'+fmt(proj.net)+'</div>'+
        '</div>'+
        '<div style="color:#858585;font-size:8pt;margin-top:10px;letter-spacing:.02em">All prices in AUD. GST not included.</div>'+
      '</div>'+
      payBlock+
      '<hr style="border:none;border-top:1px solid rgba(240,237,232,0.07);margin:0 0 26px">'+
      '<div style="display:flex;justify-content:space-between;align-items:flex-end">'+
        '<div>'+
          '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.22em;color:#858585;margin-bottom:10px">Questions?</div>'+
          '<div style="font-size:11pt;font-weight:700;color:#F0EDE8">Lachlan Sullivan-Carey</div>'+
          '<a href="mailto:lachlan@creativelsc.com" style="display:block;margin-top:5px;font-size:10pt">lachlan@creativelsc.com</a>'+
          '<div style="color:#858585;font-size:9.5pt;margin-top:3px">04 12 710 836</div>'+
        '</div>'+
        '<div style="text-align:right">'+
          (LOGO_B64?'<img src="data:image/png;base64,'+LOGO_B64+'" style="max-height:34px;width:auto;opacity:.4;display:block;margin-left:auto">':'')+
          '<div style="font-size:8pt;text-transform:uppercase;letter-spacing:.2em;color:#858585;margin-top:8px">LSC Creative.</div>'+
        '</div>'+
      '</div>'+
    '</div>'+
  '</body></html>';
}"""

# ── APPLY REPLACEMENTS ────────────────────────────────────────────────────────

# 1. Replace quote PDF return (from start of return statement to closing brace,
#    which is right before the INVOICE_BOUNDARY comment)
q_start = c.index(QUOTE_RET_START)
q_end   = c.index(INVOICE_BOUNDARY, q_start)  # pos of '\n\n// ── INVOICE PDF'
old_quote_block = c[q_start:q_end]
c = c[:q_start] + '\n' + NEW_QUOTE_RETURN + c[q_end:]
print('OK: Quote PDF return replaced (' + str(len(old_quote_block)) + ' → ' + str(len(NEW_QUOTE_RETURN)) + ' chars)')

# 2. Replace entire invoice PDF function (from function declaration to doExport)
inv_start = c.index(INVOICE_FUNC_START)
inv_end   = c.index(DOEXPORT_BOUNDARY, inv_start)
old_inv_block = c[inv_start:inv_end]
c = c[:inv_start] + NEW_INVOICE_FUNC + c[inv_end:]
print('OK: Invoice PDF function replaced (' + str(len(old_inv_block)) + ' → ' + str(len(NEW_INVOICE_FUNC)) + ' chars)')

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(c)
print('Written: ' + OUTPUT)
