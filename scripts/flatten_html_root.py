from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
HTML_DIR = ROOT / 'html'
if not HTML_DIR.exists():
    raise SystemExit('No existe html/.')
html_files = sorted(HTML_DIR.glob('*.html'))
if len(html_files) != 22:
    raise SystemExit(f'Se esperaban 22 HTML y se encontraron {len(html_files)}.')

for path in html_files:
    destination = ROOT / path.name
    if destination.exists():
        raise SystemExit(f'Ya existe el destino {destination.name}.')
    text = path.read_text(encoding='utf-8', errors='replace')
    text = text.replace('../css/', './css/')
    text = text.replace('../js/', './js/')
    text = text.replace('../assets/', './assets/')
    destination.write_text(text, encoding='utf-8')
    path.unlink()
HTML_DIR.rmdir()

# El portal raíz enlaza directamente a cada HTML.
for target in (ROOT / 'index.html', ROOT / 'js/index.js'):
    text = target.read_text(encoding='utf-8', errors='replace')
    for path in html_files:
        text = text.replace(f'./html/{path.name}', f'./{path.name}')
    target.write_text(text, encoding='utf-8')

# Los scripts reproducibles deben seguir la ubicación final de los HTML.
for path in sorted((ROOT / 'scripts').glob('*.py')):
    text = path.read_text(encoding='utf-8')
    updated = re.sub(r"ROOT / 'html/([^']+\.html)'", r"ROOT / '\1'", text)
    if updated != text:
        path.write_text(updated, encoding='utf-8')

print('HTML_EN_RAIZ=22')
print('RUTAS_REESCRITAS=1')
