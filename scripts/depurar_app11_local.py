from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'apps/creador-facturas-proforma.html', ROOT / 'creador-facturas-proforma/index.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'\s*<!-- SCRIPT DE CAPTURA DE LEADS -->\s*<script>.*?</script>', '', text, count=1, flags=re.S | re.I)
    text = re.sub(r'<script>\s*function registrarLead\(event\).*?</script>', '', text, count=1, flags=re.S)
    text = re.sub(r'\s*<label[^>]*>\s*<span[^>]*>Correo del cliente</span>.*?</label>', '', text, count=1, flags=re.S | re.I)
    text = text.replace('Enviar al Cliente', 'Descargar para compartir')
    text = text.replace('registrarLead', '')
    text = re.sub(r'[ \t]+\n', '\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'apps/js/creador-facturas-proforma.js', ROOT / 'creador-facturas-proforma/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')

    modal_start = 'function um({open:e,onClose:t,onSubmit:n})'
    modal_end = 'function dm('
    if modal_start in text and modal_end in text:
        start = text.index(modal_start)
        end = text.index(modal_end, start)
        text = text[:start] + text[end:]

    field_start = '(0,$.jsx)(tm,{label:`Correo del cliente`'
    field_end = ',(0,$.jsx)(tm,{label:`Dirección`'
    if field_start in text and field_end in text:
        start = text.index(field_start)
        end = text.index(field_end, start)
        text = text[:start] + text[end + 1:]
    text = text.replace('a({name:``,taxId:``,address:``,email:``})', 'a({name:``,taxId:``,address:``})')

    send_start = 'Oe=()=>{if(!we())return;'
    send_end = ',G=`inline-flex items-center'
    if send_start in text and send_end in text:
        start = text.index(send_start)
        end = text.index(send_end, start)
        local_action = 'Oe=()=>{if(!we())return;let t=Ee();try{xf({issuer:e,logo:n,client:i,meta:o,items:t,subtotal:R,taxAmount:te,total:z,template:u,watermark:f}),B(`ok`,`¡Proforma descargada! Revisa tu carpeta de descargas.`)}catch(e){console.error(e),B(`err`,`No se pudo generar la proforma localmente.`)}}'
        text = text[:start] + local_action + text[end:]

    text = re.sub(r'\(0,\$\.jsx\)\(um,\{open:T,onClose:\(\)=>E\(!1\),onSubmit:De,.*?\}\),', '', text, count=1)
    text = text.replace('Enviar al Cliente', 'Descargar para compartir')
    text = text.replace('mailto:', '')
    path.write_text(text, encoding='utf-8')

print('Creador de Facturas Proforma convertido a flujo local: sin correo del cliente, modal de envío ni mailto; descarga y generación preservadas.')
