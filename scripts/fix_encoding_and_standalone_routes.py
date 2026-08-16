from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SUSPICIOUS = ('Ã', 'Â', 'â', 'ð', '�')
REPLACEMENTS = {
    'â€”': '—', 'â€“': '–', 'â€¦': '…', 'â€™': '’',
    'â€œ': '“', 'â€': '”', 'â‚¬': '€', 'Â·': '·', 'Â ': '\u00a0',
}

def score(text: str) -> int:
    return sum(text.count(token) for token in SUSPICIOUS)

encoding_fixed = 0
for path in sorted(list(ROOT.glob('*.html')) + list((ROOT / 'js').glob('*.js'))):
    text = path.read_text(encoding='utf-8', errors='replace')
    chunks = re.findall(r'[\\x00-\\xff]+|[^\\x00-\\xff]+', text)
    repaired_chunks = []
    changed = False
    for chunk in chunks:
        current = chunk
        for _ in range(3):
            if not any(token in current for token in SUSPICIOUS):
                break
            try:
                candidate = current.encode('latin1').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                break
            if score(candidate) >= score(current):
                break
            current = candidate
            changed = True
        repaired_chunks.append(current)
    repaired = ''.join(repaired_chunks)
    for old, new in REPLACEMENTS.items():
        repaired = repaired.replace(old, new)
    if repaired != text:
        path.write_text(repaired, encoding='utf-8')
        encoding_fixed += 1

route_fixed = 0
for path in sorted((ROOT / 'js').glob('*.js')):
    text = path.read_text(encoding='utf-8', errors='replace')
    root_match = re.search(
        r'\(0,(?P<jsx>[A-Za-z_$][\w$]*)\.jsx\)\((?P<route>[A-Za-z_$][\w$]*),\{path:`/`,element:\(0,(?P=jsx)\.jsx\)\((?P<index>[A-Za-z_$][\w$]*),',
        text,
    )
    wildcard_match = re.search(
        r'\(0,(?P<jsx>[A-Za-z_$][\w$]*)\.jsx\)\((?P<route>[A-Za-z_$][\w$]*),\{path:`\*`,element:\(0,(?P=jsx)\.jsx\)\((?P<notfound>[A-Za-z_$][\w$]*),',
        text,
    )
    if not root_match or not wildcard_match:
        continue
    if root_match.group('jsx') != wildcard_match.group('jsx') or root_match.group('route') != wildcard_match.group('route'):
        continue
    if root_match.group('index') == wildcard_match.group('notfound'):
        continue
    prefix = (
        f"(0,{wildcard_match.group('jsx')}.jsx)"
        f"({wildcard_match.group('route')},{{path:`*`,element:(0,{wildcard_match.group('jsx')}.jsx)("
    )
    old = prefix + wildcard_match.group('notfound')
    new = prefix + root_match.group('index')
    updated, count = text.replace(old, new, 1), text.count(old)
    if count:
        path.write_text(updated, encoding='utf-8')
        route_fixed += 1

print(f'ENCODING_FILES_FIXED={encoding_fixed}')
print(f'STANDALONE_ROUTE_BUNDLES_FIXED={route_fixed}')
