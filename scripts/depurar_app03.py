from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'apps/calculadora-descuentos-promociones.html', ROOT / 'calculadora-descuentos-promociones/index.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    original = text
    text = re.sub(r'\s*<!-- SecciÃ³n Captura de Lead -->.*?</section>\s*', '\n', text, count=1, flags=re.S)
    text = re.sub(r'\s*<a[^>]+href="/admin".*?</a>\s*', '\n', text, count=1, flags=re.S)
    text = re.sub(r'\s*<script>\s*function registrarLead\(event\).*?</script>\s*', '\n', text, count=1, flags=re.S)
    if text == original:
        raise RuntimeError(f'No se encontraron residuos de captaciÃ³n en {path}')
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'apps/js/calculadora-descuentos-promociones.js', ROOT / 'calculadora-descuentos-promociones/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')

    home_start = ',(0,N.jsxs)(`section`,{className:`rounded-panel border border-navy-800 bg-navy-900/40 p-5 sm:p-7`,"data-visual-edit-loc":`src/pages/Home.tsx:184:8`'
    home_end = ',(0,N.jsxs)(`footer`,{className:`flex flex-col items-center gap-3 pt-4 pb-8 text-center text-xs text-blue-light/40`'
    if home_start in text:
        start = text.index(home_start)
        end = text.index(home_end, start)
        text = text[:start] + text[end:]
    elif 'LeadForm' in text:
        raise RuntimeError(f'LeadForm visible pero no se encontrÃ³ su secciÃ³n en {path}')

    for start_marker, end_marker, label in [
        ('function Jp', 'function Yp', 'LeadForm'),
        ('function nm', 'function rm', 'Admin'),
    ]:
        if start_marker in text:
            start = text.index(start_marker)
            end = text.index(end_marker, start)
            text = text[:start] + text[end:]
        elif label in text:
            raise RuntimeError(f'{label} no se pudo retirar de {path}')

    admin_start = ',(0,N.jsx)(yt,{path:`/admin`,element:'
    admin_end = ',(0,N.jsx)(yt,{path:`*`,element:'
    if admin_start in text:
        start = text.index(admin_start)
        end = text.index(admin_end, start)
        text = text[:start] + text[end:]

    path.write_text(text, encoding='utf-8')

print('Calculadora de Descuentos depurada: LeadForm, administración y rutas de captación retirados.')
