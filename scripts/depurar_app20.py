from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'html/guiones-manejo-objeciones.html', ROOT / 'html/guiones-manejo-objeciones.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'<form[^>]*(?:id|name)=["\'][^"\']*(?:lead|email)[^"\']*["\'][^>]*>.*?</form>', '', text, count=1, flags=re.S | re.I)
    text = re.sub(r'<script>\s*function registrarLead\(event\).*?</script>', '', text, count=1, flags=re.S)
    text = re.sub(r'<a[^>]*href=["\']/admin["\'][^>]*>.*?</a>', '', text, count=1, flags=re.S | re.I)
    text = re.sub(r'<div[^>]*data-visual-edit-loc="src/pages/Home.tsx:201:14"[^>]*>.*?</div>\s*</div>', '', text, count=1, flags=re.S)
    text = text.replace('registrarLead', '').replace('/admin', '/')
    text = re.sub(r'[ \t]+\n', '\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'js/guiones-manejo-objeciones.js']:
    text = path.read_text(encoding='utf-8', errors='replace')

    # Remove the LeadModal component, preserving the contribution modal that follows it.
    lead_start = 'function yi({open:e,onClose:t'
    lead_end = 'function Ci({open:e,onClose:t'
    if lead_start in text and lead_end in text:
        start = text.index(lead_start)
        end = text.index(lead_end, start)
        text = text[:start] + text[end:]

    # Remove the full admin page and all its chart/editor subcomponents up to NotFound.
    # El panel administrativo real empieza en zi; Fi es solo un subcomponente público heredado.
    admin_start = 'function zi('
    admin_end = 'function Gi('
    if admin_start in text and admin_end in text:
        start = text.index(admin_start)
        end = text.index(admin_end, start)
        text = text[:start] + text[end:]

    # Make premium scripts public; remove the lead-gate overlay and its counter.
    text = text.replace('e.premium&&!o', 'false')
    text = re.sub(r'\(0,N\.jsx\)\(yi,\{open:c,onClose:\(\)=>l\(!1\),onSuccess:x,.*?\}\),', '', text, count=1)
    text = re.sub(r'\(0,N\.jsx\)\(bt,\{path:`/`,element:\(0,N\.jsx\)\(zi,.*?\}\),', '', text, count=1)
    text = text.replace('/admin', '/')
    paywall_start = 're&&(0,N.jsxs)(N.Fragment,{children:[!o&&e===`all`'
    if paywall_start in text:
        text = text.replace('re&&', 'false&&', 1)
    text = text.replace('scripts premium bloqueados', '')
    text = text.replace('Desbloquear gratis', '')
    text = text.replace('Regístrate gratis y accede a toda la biblioteca al instante.', '')
    text = text.replace('LeadModal', '')
    path.write_text(text, encoding='utf-8')

print('Guiones de Manejo de Objeciones depurado: paywall, captación, LeadModal y administración retirados; catálogo, favoritos, contribuciones y modo zen preservados.')

if __name__ == '__main__':
    pass

