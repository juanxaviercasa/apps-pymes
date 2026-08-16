from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'apps/firma-correo-html.html', ROOT / 'firma-correo-html/index.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'<a[^>]*href="/admin"[^>]*>.*?</a>', '', text, count=1, flags=re.S)
    text = re.sub(r'\s*<script>\s*function registrarLead\(event\).*?</script>\s*', '\n', text, count=1, flags=re.S)
    text = text.replace('{"isSPA":true,"routes":["/","/admin"]}', '{"isSPA":true,"routes":["/"]}')
    text = text.replace('id="btn-enviar-lead"', 'id="btn-descargar-html"')
    text = re.sub(r'\n[ \t]+\n', '\n\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'apps/js/firma-correo-html.js', ROOT / 'firma-correo-html/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    # Download/copy are local actions; do not route them through a lead modal.
    text = text.replace('ae=e=>i?ie(e):s(e)', 'ae=e=>ie(e)', 1)
    route_start = ',(0,M.jsx)(xt,{path:`/admin`'
    route_end = ',(0,M.jsx)(xt,{path:`*`'
    if route_start in text and route_end in text:
        start = text.index(route_start)
        end = text.index(route_end, start)
        text = text[:start] + text[end:]
    admin_start = 'function oa()'
    admin_end = 'function sa'
    if admin_start in text:
        start = text.index(admin_start)
        end = text.find(admin_end, start + len(admin_start))
        if end != -1:
            text = text[:start] + text[end:]
    # Remove the public LeadModal mount while preserving the install guide and other modals.
    mount_start = '(0,M.jsx)(Di,{open:o,onClose:()=>s(null),onSuccess:()=>{a(!0);let e=o;s(null),e&&ie(e)'
    if mount_start in text:
        start = text.index(mount_start)
        end_marker = '})'
        end = text.index(end_marker, start) + len(end_marker)
        text = text[:start] + 'null' + text[end:]
    # Remove the external lead backend and the Di implementation; keep the next component.
    start_marker = 'Ei=new F(`https://vc110257034931.coderick.net`);function Di'
    end_marker = 'function ki'
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + 'function ki' + text[end + len(end_marker):]
    text = text.replace('}},function ki', '}};function ki', 1)
    text = text.replace('LeadSignatureModal', 'SignaturePreviewModal')
    text = text.replace('Panel de administración', '')
    text = text.replace('/admin', '/')
    text = text.replace('LeadModal', 'SignatureModal')
    path.write_text(text, encoding='utf-8')

print('Firma de Correo HTML depurada: descarga/copia directas, captación y administración retiradas.')
