from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'html/generador-codigos-qr.html', ROOT / 'html/generador-codigos-qr.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'<form[^>]*id="form-captura-lead".*?</form>', '', text, count=1, flags=re.S)
    text = re.sub(r'<a[^>]*href="/admin"[^>]*>.*?</a>', '', text, count=1, flags=re.S)
    text = re.sub(r'\s*<script>\s*function registrarLead\(event\).*?</script>\s*', '\n', text, count=1, flags=re.S)
    text = text.replace('{"isSPA":true,"routes":["/","/admin"]}', '{"isSPA":true,"routes":["/"]}')
    text = re.sub(r'\n[ \t]+\n', '\n\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'js/generador-codigos-qr.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    # The QR download is already local; invoke it directly instead of opening EmailGate.
    text = text.replace('}b(!0)}async function k()', '}k()}async function k()', 1)
    # Remove the public EmailGate mount.
    start_marker = '(0,F.jsx)(vi,{open:y'
    end_marker = '"data-visual-edit-component":`EmailGate`,"data-visual-edit-editable":`false`})'
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start) + len(end_marker)
        text = text[:start] + text[end:]
    # Remove the complete EmailGate implementation, keeping the next admin login component.
    start_marker = 'function vi'
    end_marker = 'function Ei'
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + text[end:]
    # Remove the admin route from the public router.
    route_start = ',(0,vt.jsx)(vt,{path:`/admin`'
    route_end = ',(0,vt.jsx)(vt,{path:`*`'
    if route_start in text and route_end in text:
        start = text.index(route_start)
        end = text.index(route_end, start)
        text = text[:start] + text[end:]
    text = text.replace('/admin', '/')
    # Remove the complete admin page; it is no longer reachable from the public router.
    admin_start = 'function Ei'
    admin_end = 'function Ii'
    if admin_start in text and admin_end in text:
        start = text.index(admin_start)
        end = text.index(admin_end, start)
        text = text[:start] + text[end:]
    text = text.replace('EmailGate', 'QrGate')
    path.write_text(text, encoding='utf-8')

print('Generador QR depurado: descarga directa, EmailGate, captación y ruta administrativa retirados.')
