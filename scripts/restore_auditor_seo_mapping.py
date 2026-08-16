from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / 'js' / 'auditor-seo-basico.js'
text = target.read_text(encoding='utf-8')
if 'title-len' in text and re.search(r'var\s+ki=\{', text):
    print('MAPPING_ALREADY_PRESENT=1')
    raise SystemExit(0)
original = subprocess.check_output(
    ['git', 'show', '939dfee:apps/js/auditor-seo-basico.js'],
    cwd=ROOT,
    text=True,
)
match = re.search(r'var\s+ki=\{.*?\};(?=function\s+Ai\()', original)
if not match:
    raise SystemExit('No se encontró la tabla ki en el bundle original.')
marker = 'function Ai(e,t){'
if marker not in text:
    raise SystemExit('No se encontró el componente que consume la tabla ki.')
text = text.replace(marker, match.group(0) + marker, 1)
target.write_text(text, encoding='utf-8')
print(f'MAPPING_RESTORED=1 BYTES={len(match.group(0))}')
