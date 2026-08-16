from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'apps/generador-contratos-servicios.html', ROOT / 'generador-contratos-servicios/index.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'<form[^>]*id=["\']form-captura-lead["\'][^>]*>.*?</form>', '', text, count=1, flags=re.S | re.I)
    text = re.sub(r'\s*<script>\s*function registrarLead\(event\).*?</script>\s*', '\n', text, count=1, flags=re.S)
    text = text.replace('registrarLead', '')
    text = text.replace('TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI', '')
    text = re.sub(r'[ \t]+\n', '\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'apps/js/generador-contratos-servicios.js', ROOT / 'generador-contratos-servicios/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    # Remove the external lead persistence function and its endpoint declaration.
    start_marker = 'var gr=`https://script.google.com/'
    end_marker = 'var vr=`gcps-draft-v1`'
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + text[end:]
    text = re.sub(r'_r\(c,o\)\.catch\(e=>console\.error\(`Error al enviar lead:`,e\)\),', '', text, count=1)
    text = text.replace('script.google.com', '')
    text = text.replace('Error al enviar lead', '')
    path.write_text(text, encoding='utf-8')

print('Generador de Contratos de Servicios depurado: captación y persistencia externa retiradas; correo operativo, PDF y mailto preservados.')

if __name__ == '__main__':
    pass

