from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'
text = INDEX.read_text(encoding='utf-8', errors='replace')
html_names = {path.name for path in ROOT.glob('*.html') if path.name != 'index.html'}
fixed = 0
missing = []
for name in sorted(html_names):
    old = f'href="./html/{name}"'
    new = f'href="./{name}"'
    text, count = re.subn(re.escape(old), new, text)
    fixed += count
    if new not in text:
        missing.append(name)
INDEX.write_text(text, encoding='utf-8')
print(f'ENLACES_INDEX_CORREGIDOS={fixed}')
if missing:
    raise SystemExit('Faltan enlaces en el índice: ' + ', '.join(missing))
