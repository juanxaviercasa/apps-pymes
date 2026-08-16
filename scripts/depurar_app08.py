from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'apps/comparador-campanas-avanzado.html', ROOT / 'comparador-campanas-avanzado/index.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text, count = re.subn(r'\s*<section data-visual-edit-loc="src/pages/Index.tsx:183:10".*?</section>\s*', '\n', text, count=1, flags=re.S)
    text, count = re.subn(r'\s*<script>\s*function registrarLead.*?</script>\s*', '\n', text, count=1, flags=re.S)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'apps/js/comparador-campanas-avanzado.js', ROOT / 'comparador-campanas-avanzado/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = text.replace('useState)(()=>localStorage.getItem(`unlocked`)===`true`)', 'useState)(!0)', 1)
    text = text.replace('(0,_.useEffect)(()=>{localStorage.setItem(`unlocked`,String(i))},[i]);', '', 1)
    text = text.replace('h=e=>{a(!0),localStorage.setItem(`leadEmail`,e)}', 'h=()=>{}', 1)
    text = text.replace('},[n]),let d', '},[n]);let d', 1)
    gate_start = 'tS=e=>'
    gate_end = ',rS=()=>'
    if gate_start in text and gate_end in text:
        start = text.index(gate_start)
        end = text.index(gate_end, start)
        text = text[:start] + 'nS=({children:e})=>e' + text[end:]
    else:
        raise RuntimeError(f'No se encontró EmailGate bundle en {path}')
    text = text.replace('EmailGate', 'div')
    text = text.replace('leadEmail', 'freeAccess')
    text = text.replace('unlocked', 'freeAccess')
    path.write_text(text, encoding='utf-8')

print('Comparador de Campañas depurado: funciones avanzadas públicas sin EmailGate ni correo.')
