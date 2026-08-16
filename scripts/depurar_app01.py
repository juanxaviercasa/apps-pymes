from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

html_paths = [
    ROOT / 'html/analizador-titulares.html',
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
    if text != original:
        path.write_text(text, encoding='utf-8')
    path.write_text(text, encoding='utf-8')

mount = '(0,$.jsx)(`section`,{className:`mt-8`,"data-visual-edit-loc":`src/pages/Index.tsx:207:8`,"data-visual-edit-component":`section`,"data-visual-edit-editable":`false`,children:(0,$.jsx)(br,{headline:e===`single`?u.text:``,"data-visual-edit-loc":`src/pages/Index.tsx:208:10`,"data-visual-edit-component":`LeadCapture`,"data-visual-edit-editable":`false`})})'
for path in [ROOT / 'js/analizador-titulares.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    if text.count(mount) == 1:
        text = text.replace(mount, '')
    helper_start = ',vr=null;function yr()'
    helper_end = 'var br='
    if helper_start in text and helper_end in text:
        start = text.index(helper_start)
        end = text.index(helper_end, start)
        text = text[:start] + ',' + text[end:]
    text = text.replace('sgcaptcha', 'local-captcha-disabled')
    text = text.replace('LeadCapture', 'LocalCaptureDisabled')
    path.write_text(text, encoding='utf-8')

print('Analizador de Titulares depurado: captura de correo retirada y componente LeadCapture desmontado.')
