from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'js/index.js'
text = BUNDLE.read_text(encoding='utf-8', errors='replace')
fixed, count = re.subn(r"/apps/([a-z0-9-]+)(?=[`\"'])", r"./html/\1.html", text)
if count == 0:
    raise SystemExit('No se encontraron rutas absolutas /apps/... en el bundle del índice.')
BUNDLE.write_text(fixed, encoding='utf-8')
print(f'Rutas del índice corregidas: {count}')
