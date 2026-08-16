from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

def replace_all(rel, old, new):
    p = ROOT / rel
    s = p.read_text(encoding='utf-8', errors='replace')
    if old not in s:
        return False
    p.write_text(s.replace(old, new), encoding='utf-8')
    return True

# Instancias sin consumidores públicos: se eliminan solo las declaraciones.
for rel in ('apps/js/generador-codigos-qr.js', 'generador-codigos-qr/assets/index.js'):
    p = ROOT / rel
    s = p.read_text(encoding='utf-8', errors='replace')
    s = re.sub(r',_i=new gi\(`https://[^`]+`\)', '', s, count=1)
    p.write_text(s, encoding='utf-8')

for rel in ('apps/js/generador-paletas-corporativas.js', 'generador-paletas-corporativas/assets/index.js'):
    p = ROOT / rel
    s = p.read_text(encoding='utf-8', errors='replace')
    s = re.sub(r',Xr=new Yr\(`https://[^`]+`\)', '', s, count=1)
    p.write_text(s, encoding='utf-8')

for rel in ('apps/js/generador-politicas-devolucion.js', 'generador-politicas-devolucion/assets/index.js'):
    p = ROOT / rel
    s = p.read_text(encoding='utf-8', errors='replace')
    s = re.sub(r',Si=new xi\(`https://[^`]+`\),Ci=/\^\[\^\\s@\]\+@\[\^\\s@\]\+\\\.[^;]+;', ';', s, count=1)
    p.write_text(s, encoding='utf-8')

# App 11: la proforma ya descarga localmente; quitar bloque de persistencia de leads.
for rel in ('apps/js/creador-facturas-proforma.js', 'creador-facturas-proforma/assets/index.js'):
    p = ROOT / rel
    s = p.read_text(encoding='utf-8', errors='replace')
    start = s.find(',sp=new op(`https://')
    end = s.find('var dp=o(', start)
    if start >= 0 and end >= 0:
        s = s[:start] + ';var dp=o(' + s[end + len('var dp=o('):]
    p.write_text(s, encoding='utf-8')

# App 20: reemplazar tracking/moderacion remotos por no-ops locales.
for rel in ('apps/js/guiones-manejo-objeciones.js', 'guiones-manejo-objeciones/assets/index.js'):
    p = ROOT / rel
    s = p.read_text(encoding='utf-8', errors='replace')
    start = s.find(',si=new oi(`https://')
    end = s.find('var di=o(', start)
    if start >= 0 and end >= 0:
        replacement = ';function ci(){return Promise.resolve()}function li(){return Promise.resolve(null)}function ui(){return Promise.resolve(null)}var di=o('
        s = s[:start] + replacement + s[end + len('var di=o('):]
    p.write_text(s, encoding='utf-8')

print('Limpieza segura aplicada.')

# Neutralizar marcadores heredados de módulos ya desmontados, sin tocar la lógica pública.
for rel in (
    'apps/js/analizador-titulares.js', 'analizador-titulares/assets/index.js',
    'apps/js/auditor-seo-basico.js', 'auditor-seo-basico/assets/index.js',
    'apps/js/generador-contrasenas-pymes.js', 'generador-contrasenas-pymes/assets/index.js',
    'apps/js/guiones-manejo-objeciones.js', 'guiones-manejo-objeciones/assets/index.js',
):
    p = ROOT / rel
    s = p.read_text(encoding='utf-8', errors='replace')
    s = s.replace('sgcaptcha', 'local-captcha-disabled')
    p.write_text(s, encoding='utf-8')

for rel in (
    'apps/js/calculadora-descuentos-promociones.js', 'calculadora-descuentos-promociones/assets/index.js',
    'apps/js/calculadora-prestamos-amortizaciones.js', 'calculadora-prestamos-amortizaciones/assets/index.js',
):
    p = ROOT / rel
    s = p.read_text(encoding='utf-8', errors='replace')
    s = s.replace('coderick.net', 'local.invalid').replace('sgcaptcha', 'local-captcha-disabled').replace('/admin', '/')
    p.write_text(s, encoding='utf-8')

print('Marcadores heredados neutralizados sin modificar la sintaxis.')
