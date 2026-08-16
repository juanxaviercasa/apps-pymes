from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

html_files = [
    ROOT / 'html/organizador-matriz-contenidos.html',
]
for path in html_files:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(
        r'\s*<!-- Upsell / Lead Capture Form.*?</section>',
        '',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(
        r'\s*<!-- SCRIPT DE CAPTURA DE LEADS -->.*?</script>',
        '',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(r'[ \t]+\n', '\n', text)
    path.write_text(text, encoding='utf-8')

bundle_files = [
    ROOT / 'js/organizador-matriz-contenidos.js',
]
for path in bundle_files:
    text = path.read_text(encoding='utf-8', errors='replace')

    lead_start = 'var _i=null;function vi()'
    lead_end = 'function bi({cards:e,onClose:t})'
    if lead_start in text and lead_end in text:
        start = text.index(lead_start)
        end = text.index(lead_end, start)
        text = text[:start] + text[end:]

    modal_start = 'function bi({cards:e,onClose:t})'
    modal_end = 'function xi({suggestions:e,onApply:t,onClose:n})'
    if modal_start in text and modal_end in text:
        start = text.index(modal_start)
        end = text.index(modal_end, start)
        replacement = 'function bi({cards:e,onClose:t}){(0,_.useEffect)(()=>{er(e),t()},[e,t]);return null}'
        text = text[:start] + replacement + text[end:]

    text = text.replace('sgcaptcha', '')
    text = text.replace('registrarLead', '')
    text = text.replace('LeadModal', '')
    path.write_text(text, encoding='utf-8')

print('Organizador de Matriz de Contenidos depurado: captación, captcha y gate de exportación retirados; CSV, calendario y almacenamiento local preservados.')
