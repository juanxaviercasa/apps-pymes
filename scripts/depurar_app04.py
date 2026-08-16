from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'html/calculadora-flete-envio-local.html', ROOT / 'html/calculadora-flete-envio-local.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    original = text
    start_marker = '<!-- Lead Capture -->'
    end_marker = '\n        </div>\n        \n      </main>'
    if start_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + '\n      </main>' + text[end + len(end_marker):]
    text = re.sub(r'\s*<!-- SCRIPT DE CAPTURA DE LEADS Y SOLICITUD DE PROVEEDOR -->.*?</script>\s*', '\n', text, count=1, flags=re.S)
    if text == original and (start_marker in text or 'registrarLeadFlete' in text or 'id="lead-form"' in text):
        raise RuntimeError(f'No se modificÃ³ la captura de proveedor en {path}')
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'js/calculadora-flete-envio-local.js']:
    text = path.read_text(encoding='utf-8', errors='replace')

    home_start = ',(0,M.jsx)(`div`,{className:`__NO_LEAD_WRAPPER__`'
    home_end = ',(0,M.jsx)(`footer`,{className:`border-t border-navy-700/60 py-6 text-center text-xs text-brand-300/40`'
    if home_start in text:
        start = text.index(home_start)
        end = text.index(home_end, start)
        text = text[:start] + ',(0,M.jsx)(`div`,{className:`hidden`})' + text[end:]
    elif 'data-visual-edit-component`:`LeadForm`' in text:
        raise RuntimeError(f'LeadForm visible pero su montaje no se encontrÃ³ en {path}')

    lead_start = ',Mr=`https://script.google.com/macros/s/REEMPLAZA_CON_TU_ID/exec`'
    lead_end = 'function Lr'
    if lead_start in text:
        start = text.index(lead_start)
        end = text.index(lead_end, start)
        text = text[:start] + ',Pr=()=>null;' + text[end:]
    elif 'REEMPLAZA_CON_TU_ID' in text or 'function Pr' in text:
        raise RuntimeError(f'DefiniciÃ³n LeadForm incompleta en {path}')

    text = text.replace('LeadForm', 'div')
    path.write_text(text, encoding='utf-8')

print('Calculadora de Flete depurada: solicitud de proveedor y dependencia de correo retiradas.')
