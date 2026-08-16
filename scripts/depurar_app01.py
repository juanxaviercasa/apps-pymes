from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

html_paths = [
    ROOT / 'apps/analizador-titulares.html',
    ROOT / 'analizador-titulares/index.html',
]
for path in html_paths:
    text = path.read_text(encoding='utf-8', errors='replace')
    original = text
    text = re.sub(
        r'\s*<!-- Lead Capture \(Templates\) -->.*?</section>\s*',
        '\n', text, count=1, flags=re.S
    )
    text = re.sub(
        r'\s*<!-- SCRIPT DE CAPTURA DE LEADS -->.*?</script>\s*',
        '\n', text, count=1, flags=re.S
    )
    if text == original:
        raise RuntimeError(f'No se encontró el bloque de captura en {path}')
    path.write_text(text, encoding='utf-8')

mount = '(0,$.jsx)(`section`,{className:`mt-8`,"data-visual-edit-loc":`src/pages/Index.tsx:207:8`,"data-visual-edit-component":`section`,"data-visual-edit-editable":`false`,children:(0,$.jsx)(br,{headline:e===`single`?u.text:``,"data-visual-edit-loc":`src/pages/Index.tsx:208:10`,"data-visual-edit-component":`LeadCapture`,"data-visual-edit-editable":`false`})})'
for path in [ROOT / 'apps/js/analizador-titulares.js', ROOT / 'analizador-titulares/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    if text.count(mount) != 1:
        raise RuntimeError(f'Montaje LeadCapture ambiguo o ausente en {path}: {text.count(mount)}')
    text = text.replace(mount, '')
    path.write_text(text, encoding='utf-8')

print('Analizador de Titulares depurado: captura de correo retirada y componente LeadCapture desmontado.')
