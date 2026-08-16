from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'html/conversor-optimizador-imagenes.html', ROOT / 'html/conversor-optimizador-imagenes.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'\s*<section id="curso".*?</section>\s*', '\n', text, count=1, flags=re.S)
    text = re.sub(r'\s*<!-- SCRIPT DE CAPTURA DE LEADS Y CURSO WPO -->\s*<script>.*?</script>\s*', '\n', text, count=1, flags=re.S)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'js/conversor-optimizador-imagenes.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'\(0,P\.jsx\)\(Rr,\{[^{}]*\}\)', 'null', text, count=1)
    start_marker = 'Pr=null;function Fr()'
    end_marker = '},zr='
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start) + 2
        text = text[:start] + text[end:]
    text = text.replace('LeadCapture', 'div')
    text = text.replace('Curso WPO gratis', 'Conversor de imágenes')
    text = text.replace('href:`#curso`', 'href:`#`')
    path.write_text(text, encoding='utf-8')

print('Conversor de Imágenes depurado: curso, captación y captcha retirados.')
