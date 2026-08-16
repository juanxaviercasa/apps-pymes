from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'auditor-seo-basico.html', ROOT / 'auditor-seo-basico.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    original = text
    text = re.sub(r'\s*<!-- Upsell / Lead Capture Section -->.*?</div>\s*\n\s*</main>', '\n\n      </main>', text, count=1, flags=re.S)
    text = re.sub(r'\s*<!-- SCRIPT DE CAPTURA DE LEADS -->.*?</script>\s*', '\n', text, count=1, flags=re.S)
    if text != original:
        path.write_text(text, encoding='utf-8')

modal_mount = 'i&&(0,M.jsx)(Oi,{audit:e,score:y,onClose:()=>a(!1),"data-visual-edit-loc":`src/pages/Index.tsx:357:8`,"data-visual-edit-component":`LeadModal`,"data-visual-edit-editable":`false`})'
for path in [ROOT / 'js/auditor-seo-basico.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    count = text.count(modal_mount)
    if count > 1:
        raise RuntimeError(f'Montaje de LeadModal ambiguo en {path}: {count}')
    if count == 1:
        text = text.replace(modal_mount, '')
    if 'function Oi' in text:
        start = text.index('function Oi')
        end = text.index('function Ai', start)
        text = text[:start] + text[end:]
    start_marker = ',(0,M.jsxs)(`div`,{className:`rounded-panel border border-accent/40 bg-navy-700 p-7 text-center`'
    end_marker = ']}):(0,M.jsx)(P'
    if start_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + text[end:]
    elif 'Obtener auditoría completa gratis' in text:
        raise RuntimeError(f'Upsell no eliminado en {path}')
    path.write_text(text, encoding='utf-8')

print('Auditor SEO depurado: upsell, captura de correo y modal de informe retirados del flujo visible.')
