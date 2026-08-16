from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'html/generador-contrasenas-pymes.html', ROOT / 'html/generador-contrasenas-pymes.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'<form[^>]*(?:id|name)=["\'][^"\']*(?:lead|email)["\'][^>]*>.*?</form>', '', text, count=1, flags=re.S | re.I)
    # El modal heredado no está dentro de un formulario; quitarlo por su contenedor balanceado.
    marker = 'id="lead-modal"'
    if marker in text:
        open_pos = text.rfind('<div', 0, text.index(marker))
        depth = 0
        pos = open_pos
        while pos < len(text):
            next_open = text.find('<div', pos)
            next_close = text.find('</div>', pos)
            if next_close < 0:
                break
            if next_open >= 0 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                end = next_close + len('</div>')
                if depth == 0:
                    text = text[:open_pos] + text[end:]
                    break
                pos = end
    text = re.sub(r'\s*<script>.*?(?:SecuKey|TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI).*?</script>\s*', '\n', text, count=1, flags=re.S | re.I)
    text = re.sub(r'\s*<script>\s*function registrarLead\(event\).*?</script>\s*', '\n', text, count=1, flags=re.S)
    text = text.replace('registrarLead', '')
    text = re.sub(r'[ \t]+\n', '\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'js/generador-contrasenas-pymes.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    start_marker = 'function zr({onClose:e})'
    end_marker = 'function Yr'
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + text[end:]
    text = text.replace('[n,r]=(0,_.useState)(!0),', '')
    text = re.sub(r'n&&\(0,q\.jsx\)\(zr,\{onClose:\(\)=>r\(!1\),.*?\}\),', '', text, count=1)
    # Eliminar el helper de captcha y envío que ya no tiene ningún consumidor público.
    start_marker = 'var Fr=null;function Ir()'
    end_marker = 'var Rr='
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + end_marker + text[end + len(end_marker):]
    text = text.replace('LeadModal', '')
    path.write_text(text, encoding='utf-8')

print('Generador de Contraseñas para Pymes depurado: captación y bloqueo por LeadModal retirados; generación, copia y exportación preservadas.')

if __name__ == '__main__':
    pass

