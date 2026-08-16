from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
print('--- TITULOS CON POSIBLE MOJIBAKE ---')
for path in sorted(ROOT.glob('*.html')):
    text = path.read_text(encoding='utf-8', errors='replace')
    title = re.search(r'<title>(.*?)</title>', text, re.S)
    value = title.group(1).strip() if title else '<sin title>'
    if any(token in value for token in ('Ã', 'Â', 'â', 'ð', '�')):
        print(f'{path.name}: {value}')
print('--- NAVEGACION EXTERNA/RECARGA ---')
patterns = [
    r'window\.location[^;]{0,220}',
    r'location\.href[^;]{0,220}',
    r'location\.assign\([^)]{0,160}',
    r'location\.replace\([^)]{0,160}',
    r'history\.pushState\([^;]{0,220}',
    r'<a href=[`\"]/[^`\"]{0,160}',
    r'navigate\([`\"]/[^`\"]{0,160}',
]
for path in sorted((ROOT / 'js').glob('*.js')):
    text = path.read_text(encoding='utf-8', errors='replace')
    hits = []
    for pattern in patterns:
        hits.extend(re.findall(pattern, text))
    if hits:
        print(f'[{path.name}]')
        for hit in sorted(set(hits))[:30]:
            print(hit[:260])
