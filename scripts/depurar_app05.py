from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'apps/calculadora-precios-venta-igv.html', ROOT / 'calculadora-precios-venta-igv/index.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    start_marker = '<!-- Formulario de Captura de Leads (Modificado) -->'
    end_marker = '\n            </section>\n          </div>\n        </div>\n        \n        <!-- Footer -->'
    if start_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + text[end + len('\n            </section>'):]
    text = re.sub(r'\s*<!-- Script Funcionalidad Captura de Leads -->.*?</script>\s*', '\n', text, count=1, flags=re.S)
    text = re.sub(r'\n[ \t]+\n', '\n\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'apps/js/calculadora-precios-venta-igv.js', ROOT / 'calculadora-precios-venta-igv/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    mount = '(0,J.jsx)(nr,{result:m,symbol:e,cost:n,margin:i,tax:o,"data-visual-edit-loc":`src/pages/sections/ForwardCalculator.tsx:135:8`,"data-visual-edit-component":`LeadCapture` ,"data-visual-edit-editable":`false`})'
    if mount not in text:
        mount = '(0,J.jsx)(nr,{result:m,symbol:e,cost:n,margin:i,tax:o,"data-visual-edit-loc":`src/pages/sections/ForwardCalculator.tsx:135:8`,"data-visual-edit-component":`LeadCapture`,"data-visual-edit-editable":`false`})'
    if mount in text:
        text = text.replace(mount, 'null', 1)
    text = text.replace('LeadCapture', 'div')
    path.write_text(text, encoding='utf-8')

print('Calculadora de Precios IGV depurada: captura de correo y envío externo retirados.')
