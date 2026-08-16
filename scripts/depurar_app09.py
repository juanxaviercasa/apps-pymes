from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'consola-campanas.html', ROOT / 'consola-campanas.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    marker = '<!-- SecciÃ³n de Captura de Leads Integrada -->'
    if marker not in text:
        marker = '<!-- Sección de Captura de Leads Integrada -->'
    if marker in text:
        start = text.index(marker)
        end = text.index('                    </section>', start)
        text = text[:start] + text[end:]
    text = re.sub(r'\s*<script>\s*function registrarLead.*?</script>\s*', '\n', text, count=1, flags=re.S)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'js/consola-campanas.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    mount_start = ',(0,N.jsx)(Bi,{intent:f,summary:C,onClose:()=>p(null),onConfirmed:T'
    mount_end = ',"data-visual-edit-component":`LeadModal`,"data-visual-edit-editable":`false`})'
    if mount_start in text and mount_end in text:
        start = text.index(mount_start)
        end = text.index(mount_end, start) + len(mount_end)
        text = text[:start] + ',null' + text[end:]
    captcha_start = 'var Ii=null;function Li()'
    captcha_end = 'var zi=/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;function Bi('
    if captcha_start in text and captcha_end in text:
        start = text.index(captcha_start)
        end = text.index(captcha_end, start)
        text = text[:start] + text[end:]
    definition_start = 'var zi=/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;function Bi('
    definition_end = 'function Hi()'
    if definition_start in text and definition_end in text:
        start = text.index(definition_start)
        end = text.index(definition_end, start)
        text = text[:start] + 'function Bi(){return null}' + text[end:]
    text = text.replace('LeadModal', 'div')
    text = text.replace('URL_DE_TU_GOOGLE_APPS_SCRIPT', '')
    path.write_text(text, encoding='utf-8')

print('Consola de Campañas depurada: captación, captcha y LeadModal retirados.')
