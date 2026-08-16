from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'html/creador-facturas-proforma.html', ROOT / 'html/creador-facturas-proforma.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'\s*<!-- SCRIPT DE CAPTURA DE LEADS -->\s*<script>.*?</script>\s*', '\n', text, count=1, flags=re.S)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'js/creador-facturas-proforma.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = text.replace('await cp(t,a),up(t,a).catch(e=>console.error(`notifyOwner:`,e)),', '', 1)
    start_marker = 'sp=new op(`https://vc859342100467.coderick.net`);async function cp'
    end_marker = 'var dp='
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + text[end:]
    text = text.replace('}},var dp=', '}};var dp=', 1)
    text = text.replace('LeadModal', 'SendConfirmationModal')
    path.write_text(text, encoding='utf-8')

print('Creador de Facturas Proforma depurado: leads, backend de captación y captcha retirados; mailto operativo conservado.')
