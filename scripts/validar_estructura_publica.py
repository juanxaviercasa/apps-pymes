from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
errors = []

if not (ROOT / 'index.html').is_file():
    errors.append('Falta index.html en la raíz.')
html_files = sorted((ROOT / 'html').glob('*.html'))
css_files = sorted((ROOT / 'css').glob('*.css'))
js_files = sorted((ROOT / 'js').glob('*.js'))
app_js_files = [path for path in js_files if path.name != 'index.js']
if len(html_files) != 22:
    errors.append(f'Se esperaban 22 HTML de aplicaciones y hay {len(html_files)}.')
if len(css_files) != 22 + 1:
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
root_links = set(re.findall(r'href="(\./html/[^"?]+\.html)"', root_text))
if len(root_links) != 22:
    errors.append(f'El índice raíz debe contener 22 enlaces de aplicaciones y contiene {len(root_links)}.')
for path in html_files:
    if f'href="./html/{path.name}"' not in root_text:
        errors.append(f'El índice no contiene el enlace visible a {path.name}.')

for path in html_files:
    text = path.read_text(encoding='utf-8', errors='replace')
    name = path.stem
    expected = (f'../css/{name}.css', f'../js/{name}.js', '../assets/favicon.png')
    for ref in expected:
        if ref not in text:
            errors.append(f'{path.name} no referencia {ref}.')
    for ref in (f'../css/{name}.css', f'../js/{name}.js', '../assets/favicon.png'):
        target = ROOT / ref[3:]
        if not target.is_file():
            errors.append(f'{path.name} apunta a recurso inexistente: {ref}.')

bundle = (ROOT / 'js/index.js').read_text(encoding='utf-8', errors='replace')
for path in html_files:
    if f'./html/{path.name}' not in bundle:
        errors.append(f'El portal no contiene el enlace ./html/{path.name}.')
for old in ('/apps/', './analizador-titulares.html', './auditor-seo-basico.html'):
    if old in bundle:
        errors.append(f'El bundle conserva una ruta antigua: {old}.')

print(f'ROOT_INDEX={int((ROOT / "index.html").is_file())}')
print(f'HTML_APPS={len(html_files)}')
print(f'CSS_FILES={len(css_files)}')
print(f'JS_APP_BUNDLES={len(app_js_files)}')
print(f'STRUCTURE_ERRORS={len(errors)}')
for error in errors:
    print(f'STRUCTURE_ERROR {error}')
if errors:
    raise SystemExit(1)
