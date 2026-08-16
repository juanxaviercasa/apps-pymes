from pathlib import Path

ROOT = Path('/home/ubuntu/apps-pymes')
FILES = [
    ROOT / 'apps/js/guiones-manejo-objeciones.js',
    ROOT / 'guiones-manejo-objeciones/assets/index.js',
]


def remove_function(text: str, marker: str) -> str:
    start = text.find(marker)
    if start < 0:
        return text
    brace = text.find('{', start)
    if brace < 0:
        return text
    depth = 0
    quote = None
    escaped = False
    for i in range(brace, len(text)):
        ch = text[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in ('`', '"', "'"):
            quote = ch
        elif ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return text[:start] + text[i + 1:]
    raise ValueError(f'No se encontró el cierre de {marker}')


def remove_admin_route(text: str) -> str:
    marker = ',(0,N.jsx)(bt,{path:`/`,element:(0,N.jsx)(zi,'
    start = text.find(marker)
    if start < 0:
        return text
    loc = text.find(',"data-visual-edit-loc":', start)
    if loc < 0:
        raise ValueError('No se encontró el metadato de la ruta Admin')
    end = text.find('}),', loc)
    if end < 0:
        raise ValueError('No se encontró el cierre de la ruta Admin')
    return text[:start] + text[end + 3:]


for path in FILES:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = remove_admin_route(text)
    text = remove_function(text, 'function zi(')
    path.write_text(text, encoding='utf-8')

print('App 20: ruta y componente Admin eliminados con límites balanceados.')
