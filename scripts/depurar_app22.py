from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

html_files = [
    ROOT / 'simulador-tco-fisico-nube.html',
]
for path in html_files:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(
        r'\s*<!-- Formulario de Captura de Leads Inyectado -->.*?</section>',
        '',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(
        r'\s*<!-- Script Nativo de Captura de Leads.*?</script>',
        '',
        text,
        count=1,
        flags=re.S | re.I,
    )
    text = re.sub(r'[ \t]+\n', '\n', text)
    path.write_text(text, encoding='utf-8')

bundle_files = [
    ROOT / 'js/simulador-tco-fisico-nube.js',
]
for path in bundle_files:
    text = path.read_text(encoding='utf-8', errors='replace')

    # El reporte ya dispone de Yx/jsPDF local; eliminar el envío de leads y dejar un callback local.
    text = re.sub(
        r'E=async\(e,t\)=>\{.*?\}Yx\(\{state:r,proj:h,sens:g,be:v,summary:x,company:e,email:t,chartImage:p\.current\?\.getImage\(\)\?\?null,sensImage:m\.current\?\.getImage\(\)\?\.null\}\)',
        'E=()=>{Yx({state:r,proj:h,sens:g,be:v,summary:x,chartImage:p.current?.getImage()??null,sensImage:m.current?.getImage()??null})}',
        text,
        count=1,
        flags=re.S,
    )
    # Variante correcta del patrón anterior, por si el bundle usa ??null sin el punto opcional final.
    text = re.sub(
        r'E=async\(e,t\)=>\{.*?\}Yx\(\{state:r,proj:h,sens:g,be:v,summary:x,company:e,email:t,chartImage:p\.current\?\.getImage\(\)\?\?null,sensImage:m\.current\?\.getImage\(\)\?\?null\}\)',
        'E=()=>{Yx({state:r,proj:h,sens:g,be:v,summary:x,chartImage:p.current?.getImage()??null,sensImage:m.current?.getImage()??null})}',
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(r'var nS=`https://webhook\.site/your-endpoint-id`,', '', text, count=1)

    gate_start = 'var Of=/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;function kf('
    gate_end = 'function Af(e)'
    if gate_start in text and gate_end in text:
        start = text.index(gate_start)
        end = text.index(gate_end, start)
        text = text[:start] + 'function kf({open:e,onClose:t,onSubmit:n}){return null}' + text[end:]

    text = text.replace('})}},D=', '})},D=', 1)
    text = text.replace('onClick:()=>u(!0)', 'onClick:E', 1)
    text = re.sub(
        r',\(0,J\.jsx\)\(kf,\{open:l,onClose:\(\)=>u\(!1\),onSubmit:E.*?\}\)',
        '',
        text,
        count=1,
        flags=re.S,
    )
    text = text.replace('EmailGateModal', 'ReportePDFLocal')
    text = text.replace('EmailGate', '')
    text = text.replace('input-correo', '')
    text = text.replace('registrarLead', '')
    text = text.replace('script.google.com', '')
    text = text.replace('Webhook lead capture failed:', '')
    path.write_text(text, encoding='utf-8')

print('Simulador TCO depurado: captación, webhook y EmailGate retirados; reporte PDF, CSV, escenarios y cálculos locales preservados.')
