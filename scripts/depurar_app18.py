from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'apps/generador-politicas-devolucion.html', ROOT / 'generador-politicas-devolucion/index.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'<form[^>]*(?:id|name)=["\'][^"\']*(?:lead|email)[^"\']*["\'][^>]*>.*?</form>', '', text, count=1, flags=re.S | re.I)
    text = re.sub(r'<script>\s*function registrarLead\(event\).*?</script>', '', text, count=1, flags=re.S)
    text = re.sub(r'<a[^>]*href=["\']/admin["\'][^>]*>.*?</a>', '', text, count=1, flags=re.S | re.I)
    text = text.replace('registrarLead', '').replace('/admin', '/')
    text = re.sub(r'[ \t]+\n', '\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'apps/js/generador-politicas-devolucion.js', ROOT / 'generador-politicas-devolucion/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    # Remove Admin, its subcomponents and authentication/table logic up to NotFound.
    admin_start = 'function Ii'
    admin_end = 'function Ri'
    if admin_start in text and admin_end in text:
        start = text.index(admin_start)
        end = text.index(admin_end, start)
        text = text[:start] + text[end:]
    route_start = ',(0,P.jsx)(yt,{path:`/admin`'
    route_end = ',(0,P.jsx)(yt,{path:`*`'
    if route_start in text and route_end in text:
        start = text.index(route_start)
        end = text.index(route_end, start)
        text = text[:start] + text[end:]
    text = text.replace('/admin', '/')
    text = text.replace('registrarLead', '')
    path.write_text(text, encoding='utf-8')

print('Generador de Políticas de Devolución depurado: captación y administración retiradas; generación, edición, PDF y mailto preservados.')

if __name__ == '__main__':
    pass

