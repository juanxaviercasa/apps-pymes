from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SHARED_SRC = '<script defer src="./js/datos-compartidos.js"></script>'
EXCLUDE = {'index.html', 'guia-uso-22-apps.html'}
BACKUP_PAGES = {
    'generador-cotizaciones.html',
    'creador-facturas-proforma.html',
    'comparador-campanas-avanzado.html',
    'consola-campanas.html',
    'organizador-matriz-contenidos.html',
    'crm-pymes.html',
    'flujo-caja-pymes.html',
    'inventario-compras-pymes.html',
    'tareas-proyectos-pymes.html',
}


def app_id(path: Path) -> str:
    return path.stem


def app_name(path: Path, text: str) -> str:
    match = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    title = re.sub(r'\s+', ' ', match.group(1)).strip() if match else path.stem.replace('-', ' ').title()
    return re.sub(r'<[^>]+>', '', title)


def add_identity(path: Path, text: str) -> str:
    body_match = re.search(r'<body([^>]*)>', text, re.I)
    if not body_match:
        raise RuntimeError(f'No se encontró <body> en {path.name}')
    attrs = body_match.group(1)
    attrs = re.sub(r'\sdata-app-id="[^"]*"', '', attrs)
    attrs = re.sub(r'\sdata-app-name="[^"]*"', '', attrs)
    attrs += f' data-app-id="{app_id(path)}" data-app-name="{app_name(path, text)}"'
    replacement = '<body' + attrs + '>'
    return text[:body_match.start()] + replacement + text[body_match.end():]


def add_backup_shared_key(text: str) -> str:
    pattern = r'(["\']?storageKeys["\']?\s*:\s*\[)([^\]]*)(\])'
    match = re.search(pattern, text)
    if not match or "np_shared_v1" in match.group(0):
        return text
    inside = match.group(2).strip()
    if inside:
        inside += ', '
    quote = '"' if '"' in inside else "'"
    inside += quote + 'np_shared_v1' + quote
    return text[:match.start(2)] + inside + text[match.end(2):]


changed = []
for path in sorted(ROOT.glob('*.html')):
    if path.name in EXCLUDE:
        continue
    text = path.read_text(encoding='utf-8')
    original = text
    if SHARED_SRC not in text:
        marker = '<head>'
        if marker not in text:
            raise RuntimeError(f'No se encontró <head> en {path.name}')
        text = text.replace(marker, marker + '\n    ' + SHARED_SRC, 1)
    text = add_identity(path, text)
    if path.name in BACKUP_PAGES:
        text = add_backup_shared_key(text)
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(path.name)
print(f'Actualizadas {len(changed)} páginas: {", ".join(changed)}')
