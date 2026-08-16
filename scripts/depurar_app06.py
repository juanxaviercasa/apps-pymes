from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'html/calculadora-prestamos-amortizaciones.html', ROOT / 'html/calculadora-prestamos-amortizaciones.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text, count = re.subn(r'\s*<footer class="no-print mt-14 flex justify-center border-t border-line/50 pt-6">.*?</footer>\s*', '\n', text, count=1, flags=re.S)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'js/calculadora-prestamos-amortizaciones.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    footer_start = ',(0,J.jsx)(`__DISABLED_FOOTER__`,{className:`no-print mt-14 flex justify-center border-t border-line/50 pt-6`'
    lead_start = ',(0,J.jsx)(ri,{open:g,onClose:()=>v(!1)'
    admin_start = ',(0,J.jsx)(ii,{open:y,onClose:()=>b(!1)'
    end = ']})}function Zm'
    if footer_start in text and lead_start in text:
        start = text.index(footer_start)
        lead = text.index(lead_start, start)
        text = text[:start] + ',null' + text[lead:]
    if lead_start in text and admin_start in text:
        start = text.index(lead_start)
        admin = text.index(admin_start, start)
        text = text[:start] + ',null' + text[admin:]
    if admin_start in text and end in text:
        start = text.index(admin_start)
        finish = text.index(end, start)
        text = text[:start] + ',null' + text[finish:]
    text = text.replace('className:`no-print mt-14 flex justify-center border-t border-line/50 pt-6`', 'className:`hidden`', 1)
    text = text.replace('onClick:()=>b(!0)', 'onClick:()=>{}', 1)
    text = text.replace('Panel de administración', '').replace('Panel de administraciÃ³n', '')
    text = text.replace('LeadModal', 'div').replace('AdminPanel', 'div')
    path.write_text(text, encoding='utf-8')

print('Calculadora de Préstamos depurada: captación y administración retiradas.')
