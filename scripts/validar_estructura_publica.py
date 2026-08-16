from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
html_paths = sorted(path for path in ROOT.glob('*.html') if path.name != 'index.html')
js_files = sorted((ROOT / 'js').glob('*.js'))
app_js_files = [path for path in js_files if path.name != 'index.js']
css_files = sorted((ROOT / 'css').glob('*.css'))
errors = []

if not (ROOT / 'index.html').is_file():
    errors.append('Falta index.html en la raíz.')
if len(html_paths) != 22:
    errors.append(f'Se esperaban 22 HTML en la raíz y hay {len(html_paths)}.')
if len(css_files) != 23:
    errors.append(f'Se esperaban 23 CSS incluyendo el portal y hay {len(css_files)}.')
if len(app_js_files) != 22:
    errors.append(f'Se esperaban 22 JS de aplicaciones y hay {len(app_js_files)}.')

for path in js_files:
    result = subprocess.run(['node', '--check', str(path)], capture_output=True, text=True)
    if result.returncode:
        errors.append(f'Sintaxis JS inválida: {path.relative_to(ROOT)}')

root_text = (ROOT / 'index.html').read_text(encoding='utf-8', errors='replace')
for ref in ('./css/index.css', './js/index.js', './assets/favicon.png'):
    if ref not in root_text:
        errors.append(f'El índice no referencia {ref}.')
root_links = set(re.findall(r'href="(\./[^"?]+\.html)"', root_text))
if len(root_links) != 22:
    errors.append(f'El índice raíz debe contener 22 enlaces de aplicaciones y contiene {len(root_links)}.')
for path in html_paths:
    if f'href="./{path.name}"' not in root_text:
        errors.append(f'El índice no contiene el enlace visible a {path.name}.')

for path in html_paths:
    text = path.read_text(encoding='utf-8', errors='replace')
    name = path.stem
    title = re.search(r'<title>(.*?)</title>', text, re.S)
    if not title or any(token in title.group(1) for token in ('Ã', 'Â', 'â', 'ð', '�')):
        errors.append(f'{path.name} tiene un título ausente o con codificación dañada.')
    expected = (f'./css/{name}.css', f'./js/{name}.js', './assets/favicon.png')
    for ref in expected:
        if ref not in text:
            errors.append(f'{path.name} no referencia {ref}.')
    for ref in expected:
        target = ROOT / ref[2:]
        if not target.is_file():
            errors.append(f'{path.name} apunta a recurso inexistente: {ref}.')
    bundle_path = ROOT / 'js' / f'{name}.js'
    bundle_text = bundle_path.read_text(encoding='utf-8', errors='replace') if bundle_path.is_file() else ''
    root_match = re.search(r'\.jsx\)\([^,]+,\{path:`/`,element:\(0,[^)]*\.jsx\)\(([^,]+),', bundle_text)
    wildcard_match = re.search(r'\.jsx\)\([^,]+,\{path:`\*`,element:\(0,[^)]*\.jsx\)\(([^,]+),', bundle_text)
    if not root_match or not wildcard_match or root_match.group(1) != wildcard_match.group(1):
        errors.append(f'{name}.js no tiene ruta wildcard standalone apuntando al componente principal.')

bundle = (ROOT / 'js/index.js').read_text(encoding='utf-8', errors='replace')
for path in html_paths:
    if f'./{path.name}' not in bundle:
        errors.append(f'El portal no contiene el enlace ./{path.name}.')
for old in ('/apps/', './html/', '../css/', '../js/', '../assets/'):
    if old in root_text or old in bundle:
        errors.append(f'El portal conserva una ruta antigua: {old}.')

print(f'ROOT_INDEX={int((ROOT / "index.html").is_file())}')
print(f'HTML_APPS_ROOT={len(html_paths)}')
print(f'CSS_FILES={len(css_files)}')
print(f'JS_APP_BUNDLES={len(app_js_files)}')
print(f'STRUCTURE_ERRORS={len(errors)}')
for error in errors:
    print(f'STRUCTURE_ERROR {error}')
if errors:
    raise SystemExit(1)
