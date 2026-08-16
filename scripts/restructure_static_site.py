from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'apps'
HTML = ROOT / 'html'
CSS = ROOT / 'css'
JS = ROOT / 'js'
ASSETS = ROOT / 'assets'

if not SOURCE.exists():
    raise SystemExit('No existe la carpeta apps/ de origen.')
for target in (HTML, CSS, JS, ASSETS):
    target.mkdir(exist_ok=True)

# Consolidar el portal y los recursos públicos en una estructura simple.
shutil.move(str(SOURCE / 'index.html'), str(ROOT / 'index.html'))
for path in sorted(SOURCE.glob('*.html')):
    shutil.move(str(path), str(HTML / path.name))
for path in sorted((SOURCE / 'css').glob('*.css')):
    shutil.move(str(path), str(CSS / path.name))
for path in sorted((SOURCE / 'js').glob('*.js')):
    shutil.move(str(path), str(JS / path.name))
shutil.move(str(SOURCE / 'assets' / 'index.css'), str(CSS / 'index.css'))
shutil.move(str(SOURCE / 'assets' / 'index.js'), str(JS / 'index.js'))
shutil.move(str(SOURCE / 'favicon.png'), str(ASSETS / 'favicon.png'))

# Las copias antiguas por aplicación son redundantes: sus versiones publicables
# ya quedaron consolidadas en html/, css/ y js/.
shutil.rmtree(SOURCE)
for path in sorted(ROOT.iterdir()):
    if path.is_dir() and (path / 'index.html').exists() and (path / 'assets' / 'index.js').exists():
        shutil.rmtree(path)

# Actualizar rutas de scripts reproducibles a la nueva estructura.
for path in sorted((ROOT / 'scripts').glob('*.py')):
    text = path.read_text(encoding='utf-8')
    updated = text.replace("js/index.js", "js/index.js")
    updated = updated.replace("js", "js")
    updated = updated.replace("css", "css")
    updated = updated.replace("html/*.html", "html/*.html")
    if updated != text:
        path.write_text(updated, encoding='utf-8')

# El portal vive en la raíz; las aplicaciones y recursos quedan agrupados.
root_index = (ROOT / 'index.html').read_text(encoding='utf-8')
root_index = root_index.replace('./assets/index.css', './css/index.css')
root_index = root_index.replace('./assets/index.js', './js/index.js')
root_index = root_index.replace('href="favicon.png"', 'href="./assets/favicon.png"')
(ROOT / 'index.html').write_text(root_index, encoding='utf-8')

# Cada aplicación está dentro de html/, por lo que sube un nivel para sus recursos.
for path in sorted(HTML.glob('*.html')):
    text = path.read_text(encoding='utf-8')
    text = text.replace('./css/', '../css/')
    text = text.replace('./js/', '../js/')
    text = text.replace('./favicon.png', '../assets/favicon.png')
    path.write_text(text, encoding='utf-8')

# Los enlaces del portal apuntan a html/<aplicacion>.html.
index_bundle = JS / 'index.js'
text = index_bundle.read_text(encoding='utf-8')
for path in sorted(HTML.glob('*.html')):
    text = text.replace(f'./{path.name}', f'./html/{path.name}')
index_bundle.write_text(text, encoding='utf-8')

print(f'HTML={len(list(HTML.glob("*.html")))}')
print(f'CSS={len(list(CSS.glob("*.css")))}')
print(f'JS={len(list(JS.glob("*.js")))}')
print('ESTRUCTURA=ROOT')
