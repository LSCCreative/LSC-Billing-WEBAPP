#!/usr/bin/env python3
"""
patch_pdf_refactor.py
Full replacement of buildClientPDF + buildClientInvoicePDF:
  - Light palette: #F0EDE8 bg, #E8E2D9 accent block, #252930/#3A4756 text
  - Typography scale: .sh at 1.4rem, table data at 1rem, eyebrow at 7.5pt
  - "Media Productions" subtitle
  - Deposit clause under total
  - Inline single-row contact footer
  - payBlock updated to light theme
"""
import re, sys

SRC  = '/sessions/adoring-intelligent-curie/mnt/LSC Billing App [Phase 01]/index.html'
DEST = '/sessions/adoring-intelligent-curie/mnt/outputs/index.html'

with open(SRC, 'r', encoding='utf-8') as f:
    c = f.read()

# ══════════════════════════════════════════════════════════════════════════════
# NEW buildClientPDF
# ══════════════════════════════════════════════════════════════════════════════
NEW_QUOTE = r"""function buildClientPDF(proj){
  var ar=proj.activeRows||{};
  var serviceItems='';
  labourSections.forEach(function(sec){
    var rows=(ar[sec.id]||[]).filter(function(s){return(s.qty||0)>0;});if(!rows.length)return;
    serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(58,71,86,0.1)">'+
      '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">'+esc(sec.label)+'</div>';
    rows.forEach(function(s){serviceItems+='<div style="font-size:1rem;font-weight:600;color:#252930;margin-bottom:3px">'+esc(s.name)+'</div>';});
    serviceItems+='</div>';
  });
  var eqActive=(ar.equip||[]).filter(function(e){return e.vendor||(e.days&&e.cost);});
  if(eqActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(58,71,86,0.1)"><div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">Equipment Hire</div><div style="font-size:1rem;font-weight:600;color:#252930;margin-bottom:3px">Equipment Hire</div></div>';}
  var tvActive=(ar.travel||[]).filter(function(t){return(t.qty||0)>0;});
  if(tvActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(58,71,86,0.1)"><div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">Travel &amp; Accommodation</div>'+tvActive.map(function(s){return'<div style="font-size:1rem;color:#252930;margin-bottom:2px">'+esc(s.name)+'</div>';}).join('')+'</div>';}
  var crActive=(ar.crew||[]).filter(function(c){return c.role||(c.days&&c.cost);});
  if(crActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(58,71,86,0.1)"><div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">External Crew &amp; Contracts</div>'+crActive.map(function(c){return'<div style="font-size:1rem;color:#252930;margin-bottom:2px">'+esc(c.role||'Crew Member')+'</div>';}).join('')+'</div>';}

  return'<!DOCTYPE html><html><head><meta charset="UTF-8"><style>*{box-sizing:border-box;margin:0;padding:0}@page{size:letter;margin:.5in}@media print{body{-webkit-print-color-adjust:exact;print-color-adjust:exact;color-adjust:exact}}body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:10pt;color:#252930;background:#F0EDE8;width:8.5in;margin:0 auto}.wrap{padding:42px 52px;background:#F0EDE8}.sh{font-size:1.4rem;font-weight:700;color:#252930;letter-spacing:-.01em;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid rgba(192,96,60,0.3)}.eyebrow{font-size:7.5pt;text-transform:uppercase;letter-spacing:.2em;color:#7A7470;margin-bottom:6px}table{border-collapse:collapse;width:100%}a{color:#C0603C;text-decoration:none}</style></head><body>'+
    '<div class="wrap">'+
      '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:34px;padding-bottom:22px;border-bottom:1px solid rgba(58,71,86,0.15)">'+
        (LOGO_B64?'<img src="data:image/png;base64,'+LOGO_B64+'" style="max-height:50px;width:auto;object-fit:contain;display:block">':'<div><div style="font-size:18pt;font-weight:900;letter-spacing:-.01em;color:#252930">LSC CREATIVE<span style="color:#C0603C">.</span></div><div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.22em;color:#7A7470;margin-top:4px">Media Productions</div></div>')+
        '<div style="text-align:right">'+
          '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.2em;color:#C0603C;margin-bottom:6px">Project Quote</div>'+
          '<div style="font-size:15pt;font-weight:900;color:#252930;letter-spacing:-.01em">'+esc(proj.upid||'—')+'</div>'+
          '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.2em;color:#252930;opacity:.5;margin-top:3px">'+esc(proj.date||'')+'</div>'+
        '</div>'+
      '</div>'+
      '<div style="margin-bottom:32px">'+
        '<div class="eyebrow">Prepared for</div>'+
        '<div style="font-size:20pt;font-weight:800;color:#252930;line-height:1.05;letter-spacing:-.01em">'+esc(proj.name)+'</div>'+
        (proj.businessName?'<div style="font-size:11pt;color:#3A4756;margin-top:5px;font-weight:500">'+esc(proj.businessName)+'</div>':'')+
        (proj.clientName?'<div style="font-size:9pt;color:#7A7470;margin-top:4px">'+esc(proj.clientName)+(proj.clientEmail?' &middot; <a href="mailto:'+esc(proj.clientEmail)+'">'+esc(proj.clientEmail)+'</a>':'')+'</div>':'')+
      '</div>'+
      (function(){
        var drows=(proj.activeRows&&proj.activeRows.deliverables||[]).filter(function(d){return d.name;});
        if(!drows.length)return'';
        return'<div style="margin-bottom:28px"><div class="sh">Deliverables</div>'+
          '<table><thead><tr style="background:#E8E2D9">'+
            '<th style="text-align:left;padding:8px 12px;font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid rgba(58,71,86,0.15)">Deliverable</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid rgba(58,71,86,0.15)">Format</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid rgba(58,71,86,0.15)">Duration</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid rgba(58,71,86,0.15)">Qty</th>'+
          '</tr></thead><tbody>'+
          drows.map(function(d,i){var bg=i%2===0?'#F0EDE8':'#EDE8E1';return'<tr style="background:'+bg+'"><td style="padding:9px 12px;font-size:1rem;font-weight:600;color:#252930">'+esc(d.name)+'</td><td style="text-align:right;padding:9px 12px;font-size:1rem;color:#3A4756">'+esc(d.format||'—')+'</td><td style="text-align:right;padding:9px 12px;font-size:1rem;color:#3A4756">'+esc(d.duration||'—')+'</td><td style="text-align:right;padding:9px 12px;font-size:1rem;font-weight:700;color:#C0603C">'+esc(String(d.qty||1))+'</td></tr>';}).join('')+
          '</tbody></table></div>';
      })()+
      '<div style="padding-bottom:24px"><div class="sh">Production Scope</div>'+serviceItems+'</div>'+
      '<div style="background:#E8E2D9;padding:28px 32px">'+
        '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.2em;color:#C0603C;font-weight:700;margin-bottom:14px">Project Estimate</div>'+
        '<div style="display:flex;justify-content:space-between;align-items:baseline;padding:14px 0;border-top:1px solid rgba(58,71,86,0.15);border-bottom:1px solid rgba(58,71,86,0.15)">'+
          '<div style="color:#252930;font-size:13pt;font-weight:700">Project Total <span style="color:#7A7470;font-size:9pt;font-weight:400">inc. all services</span></div>'+
          '<div style="color:#C0603C;font-size:26pt;font-weight:900;letter-spacing:-.02em">'+fmt(proj.net)+'</div>'+
        '</div>'+
        '<div style="font-style:italic;font-size:8.5pt;color:#3A4756;margin-top:10px;letter-spacing:.01em">A 50% deposit is required to book all projects.</div>'+
        '<div style="font-size:7.5pt;color:#7A7470;margin-top:6px;opacity:.8">All prices in AUD. GST not included. Quote valid for 30 days from issue date.</div>'+
        '<hr style="border:none;border-top:1px solid rgba(58,71,86,0.15);margin:20px 0">'+
        '<div style="display:flex;justify-content:space-between;align-items:center">'+
          '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.22em;color:#7A7470">Questions?</div>'+
          '<div style="font-size:10pt;color:#252930;font-weight:600">Lachlan Sullivan-Carey &nbsp;&middot;&nbsp; <a href="mailto:lachlan@creativelsc.com" style="color:#C0603C;text-decoration:none">lachlan@creativelsc.com</a></div>'+
          '<div style="font-size:10pt;color:#3A4756">04 12 710 836</div>'+
        '</div>'+
      '</div>'+
    '</div>'+
  '</body></html>';
}"""

# ══════════════════════════════════════════════════════════════════════════════
# NEW buildClientInvoicePDF
# ══════════════════════════════════════════════════════════════════════════════
NEW_INVOICE = r"""function buildClientInvoicePDF(proj){
  var ar=proj.activeRows||{};
  var serviceItems='';
  labourSections.forEach(function(sec){
    var rows=(ar[sec.id]||[]).filter(function(s){return(s.qty||0)>0;});if(!rows.length)return;
    serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(58,71,86,0.1)">'+
      '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">'+esc(sec.label)+'</div>';
    rows.forEach(function(s){serviceItems+='<div style="font-size:1rem;font-weight:600;color:#252930;margin-bottom:3px">'+esc(s.name)+'</div>';});
    serviceItems+='</div>';
  });
  var eqActive=(ar.equip||[]).filter(function(e){return e.vendor||(e.days&&e.cost);});
  if(eqActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(58,71,86,0.1)"><div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">Equipment Hire</div><div style="font-size:1rem;font-weight:600;color:#252930;margin-bottom:3px">Equipment Hire</div></div>';}
  var tvActive=(ar.travel||[]).filter(function(t){return(t.qty||0)>0;});
  if(tvActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(58,71,86,0.1)"><div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">Travel &amp; Accommodation</div>'+tvActive.map(function(s){return'<div style="font-size:1rem;color:#252930;margin-bottom:2px">'+esc(s.name)+'</div>';}).join('')+'</div>';}
  var crActive=(ar.crew||[]).filter(function(c){return c.role||(c.days&&c.cost);});
  if(crActive.length){serviceItems+='<div style="margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(58,71,86,0.1)"><div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;font-weight:700;margin-bottom:5px">External Crew &amp; Contracts</div>'+crActive.map(function(c){return'<div style="font-size:1rem;color:#252930;margin-bottom:2px">'+esc(c.role||'Crew Member')+'</div>';}).join('')+'</div>';}
  var invSettings=loadInvoiceSettings();
  var payBlock='';
  if(invSettings.bankName||invSettings.accountName||invSettings.bsb||invSettings.accountNumber||invSettings.paymentTerms){
    payBlock=
      '<div style="margin-top:16px;padding-top:14px;border-top:1px solid rgba(58,71,86,0.15)">'+
        '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.2em;color:#C0603C;font-weight:700;margin-bottom:10px">Payment Details</div>'+
        '<table style="font-size:10pt"><tbody>'+
        (invSettings.bankName?'<tr><td style="padding:5px 0;color:#7A7470;width:160px">Bank</td><td style="padding:5px 0;font-weight:600;color:#252930">'+esc(invSettings.bankName)+'</td></tr>':'')+
        (invSettings.accountName?'<tr><td style="padding:5px 0;color:#7A7470">Account Name</td><td style="padding:5px 0;font-weight:600;color:#252930">'+esc(invSettings.accountName)+'</td></tr>':'')+
        (invSettings.bsb?'<tr><td style="padding:5px 0;color:#7A7470">BSB</td><td style="padding:5px 0;font-weight:600;color:#252930">'+esc(invSettings.bsb)+'</td></tr>':'')+
        (invSettings.accountNumber?'<tr><td style="padding:5px 0;color:#7A7470">Account Number</td><td style="padding:5px 0;font-weight:600;color:#252930">'+esc(invSettings.accountNumber)+'</td></tr>':'')+
        '</tbody></table>'+
        (invSettings.paymentTerms?'<div style="margin-top:10px;padding:10px 14px;background:rgba(58,71,86,0.08);border-left:3px solid #C0603C"><div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#C0603C;margin-bottom:5px;font-weight:700">Payment Terms</div><div style="font-size:10pt;color:#252930;line-height:1.65">'+esc(invSettings.paymentTerms)+'</div></div>':'')+
      '</div>';
  }
  return'<!DOCTYPE html><html><head><meta charset="UTF-8"><style>*{box-sizing:border-box;margin:0;padding:0}@page{size:letter;margin:.5in}@media print{body{-webkit-print-color-adjust:exact;print-color-adjust:exact;color-adjust:exact}}body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:10pt;color:#252930;background:#F0EDE8;width:8.5in;margin:0 auto}.wrap{padding:42px 52px;background:#F0EDE8}.sh{font-size:1.4rem;font-weight:700;color:#252930;letter-spacing:-.01em;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid rgba(192,96,60,0.3)}.eyebrow{font-size:7.5pt;text-transform:uppercase;letter-spacing:.2em;color:#7A7470;margin-bottom:6px}table{border-collapse:collapse;width:100%}a{color:#C0603C;text-decoration:none}</style></head><body>'+
    '<div class="wrap">'+
      '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:34px;padding-bottom:22px;border-bottom:1px solid rgba(58,71,86,0.15)">'+
        (LOGO_B64?'<img src="data:image/png;base64,'+LOGO_B64+'" style="max-height:50px;width:auto;object-fit:contain;display:block">':'<div><div style="font-size:18pt;font-weight:900;letter-spacing:-.01em;color:#252930">LSC CREATIVE<span style="color:#C0603C">.</span></div><div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.22em;color:#7A7470;margin-top:4px">Media Productions</div></div>')+
        '<div style="text-align:right">'+
          '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.2em;color:#C0603C;margin-bottom:6px">Invoice</div>'+
          '<div style="font-size:15pt;font-weight:900;color:#252930;letter-spacing:-.01em">'+esc(proj.invoiceNumber||'—')+'</div>'+
          '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.2em;color:#252930;opacity:.5;margin-top:3px">'+esc(proj.date||'')+'</div>'+
        '</div>'+
      '</div>'+
      '<div style="margin-bottom:32px">'+
        '<div class="eyebrow">Billed to</div>'+
        '<div style="font-size:20pt;font-weight:800;color:#252930;line-height:1.05;letter-spacing:-.01em">'+esc(proj.name)+'</div>'+
        (proj.businessName?'<div style="font-size:11pt;color:#3A4756;margin-top:5px;font-weight:500">'+esc(proj.businessName)+'</div>':'')+
        (proj.clientName?'<div style="font-size:9pt;color:#7A7470;margin-top:4px">'+esc(proj.clientName)+(proj.clientEmail?' &middot; <a href="mailto:'+esc(proj.clientEmail)+'">'+esc(proj.clientEmail)+'</a>':'')+'</div>':'')+
      '</div>'+
      (function(){
        var drows=(proj.activeRows&&proj.activeRows.deliverables||[]).filter(function(d){return d.name;});
        if(!drows.length)return'';
        return'<div style="margin-bottom:28px"><div class="sh">Deliverables</div>'+
          '<table><thead><tr style="background:#E8E2D9">'+
            '<th style="text-align:left;padding:8px 12px;font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid rgba(58,71,86,0.15)">Deliverable</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid rgba(58,71,86,0.15)">Format</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid rgba(58,71,86,0.15)">Duration</th>'+
            '<th style="text-align:right;padding:8px 12px;font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#7A7470;border-bottom:1px solid rgba(58,71,86,0.15)">Qty</th>'+
          '</tr></thead><tbody>'+
          drows.map(function(d,i){var bg=i%2===0?'#F0EDE8':'#EDE8E1';return'<tr style="background:'+bg+'"><td style="padding:9px 12px;font-size:1rem;font-weight:600;color:#252930">'+esc(d.name)+'</td><td style="text-align:right;padding:9px 12px;font-size:1rem;color:#3A4756">'+esc(d.format||'—')+'</td><td style="text-align:right;padding:9px 12px;font-size:1rem;color:#3A4756">'+esc(d.duration||'—')+'</td><td style="text-align:right;padding:9px 12px;font-size:1rem;font-weight:700;color:#C0603C">'+esc(String(d.qty||1))+'</td></tr>';}).join('')+
          '</tbody></table></div>';
      })()+
      '<div style="padding-bottom:24px"><div class="sh">Production Scope</div>'+serviceItems+'</div>'+
      '<div style="background:#E8E2D9;padding:28px 32px">'+
        '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.2em;color:#C0603C;font-weight:700;margin-bottom:14px">Invoice Total</div>'+
        '<div style="display:flex;justify-content:space-between;align-items:baseline;padding:14px 0;border-top:1px solid rgba(58,71,86,0.15);border-bottom:1px solid rgba(58,71,86,0.15)">'+
          '<div style="color:#252930;font-size:13pt;font-weight:700">Project Total <span style="color:#7A7470;font-size:9pt;font-weight:400">inc. all services</span></div>'+
          '<div style="color:#C0603C;font-size:26pt;font-weight:900;letter-spacing:-.02em">'+fmt(proj.net)+'</div>'+
        '</div>'+
        '<div style="font-size:7.5pt;color:#7A7470;margin-top:8px;opacity:.8">All prices in AUD. GST not included.</div>'+
        payBlock+
        '<hr style="border:none;border-top:1px solid rgba(58,71,86,0.15);margin:20px 0">'+
        '<div style="display:flex;justify-content:space-between;align-items:center">'+
          '<div style="font-size:7.5pt;text-transform:uppercase;letter-spacing:.22em;color:#7A7470">Questions?</div>'+
          '<div style="font-size:10pt;color:#252930;font-weight:600">Lachlan Sullivan-Carey &nbsp;&middot;&nbsp; <a href="mailto:lachlan@creativelsc.com" style="color:#C0603C;text-decoration:none">lachlan@creativelsc.com</a></div>'+
          '<div style="font-size:10pt;color:#3A4756">04 12 710 836</div>'+
        '</div>'+
      '</div>'+
    '</div>'+
  '</body></html>';
}"""

# ── REPLACE buildClientPDF ────────────────────────────────────────────────────
c, n1 = re.subn(
    r'function buildClientPDF\(proj\)\{.*?\n\}(?=\n\n// ── INVOICE PDF BUILDER)',
    NEW_QUOTE,
    c, flags=re.DOTALL
)
print('OK [buildClientPDF]' if n1 else 'MISS [buildClientPDF]', file=sys.stderr if not n1 else sys.stdout)

# ── REPLACE buildClientInvoicePDF ─────────────────────────────────────────────
c, n2 = re.subn(
    r'function buildClientInvoicePDF\(proj\)\{.*?\n\}(?=\n\nasync function doExport)',
    NEW_INVOICE,
    c, flags=re.DOTALL
)
print('OK [buildClientInvoicePDF]' if n2 else 'MISS [buildClientInvoicePDF]', file=sys.stderr if not n2 else sys.stdout)

if n1 and n2:
    with open(SRC,  'w', encoding='utf-8') as f: f.write(c)
    with open(DEST, 'w', encoding='utf-8') as f: f.write(c)
    print('Written: ' + SRC)
    print('Written: ' + DEST)
else:
    print('ABORTED — no files written', file=sys.stderr)
    sys.exit(1)
