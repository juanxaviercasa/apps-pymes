from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'apps/generador-contrasenas-pymes.html', ROOT / 'generador-contrasenas-pymes/index.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'<form[^>]*(?:id|name)=["\'][^"\']*(?:lead|email)[^"\']*["\'][^>]*>.*?</form>', '', text, count=1, flags=re.S | re.I)
    text = re.sub(r'\s*<script>\s*function registrarLead\(event\).*?</script>\s*', '\n', text, count=1, flags=re.S)
    text = text.replace('registrarLead', '')
    text = re.sub(r'[ \t]+\n', '\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'apps/js/generador-contrasenas-pymes.js', ROOT / 'generador-contrasenas-pymes/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    start_marker = 'function zr({onClose:e})'
    end_marker = 'function Yr'
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + text[end:]
    text = text.replace('[n,r]=(0,_.useState)(!0),', '')
    text = re.sub(r'n&&\(0,q\.jsx\)\(zr,\{onClose:\(\)=>r\(!1\),.*?\}\),', '', text, count=1)
    text = text.replace('LeadModal', '')
    path.write_text(text, encoding='utf-8')

print('Generador de Contraseñas para Pymes depurado: captación y bloqueo por LeadModal retirados; generación, copia y exportación preservadas.')

if __name__ == '__main__':
    pass

