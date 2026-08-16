from pathlib import Path

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'apps/js/calculadora-sobrecostos-laborales.js', ROOT / 'calculadora-sobrecostos-laborales/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')
    old = 'onClick:()=>s(!0),disabled:f.length===0'
    new = 'onClick:()=>VS(f,p,{nombre:``,correo:``},e,t===`anual`?`Anual (12 meses)`:`Mensual`),disabled:f.length===0'
    if old not in text:
        raise RuntimeError(f'No se encontró el botón de descarga condicionado en {path}')
    text = text.replace(old, new, 1)
    lead_start = ',(0,J.jsx)(Jd,{open:o,onClose:()=>s(!1)'
    lead_end = ',"data-visual-edit-component":`LeadModal`,"data-visual-edit-editable":`false`})'
    if lead_start in text and lead_end in text:
        start = text.index(lead_start)
        end = text.index(lead_end, start) + len(lead_end)
        text = text[:start] + ',null' + text[end:]
    text = text.replace('a.text(`Preparado para: ${n.nombre}  |  ${n.correo}  |  ${new Date().toLocaleDateString(`es-PE`)}`,40,62)', 'a.text(`Generado: ${new Date().toLocaleDateString(`es-PE`)}`,40,62)')
    definition_start = 'Jd=({open:e,onClose:t,onConfirm:n})=>{'
    definition_end = ',Yd='
    if definition_start in text and definition_end in text:
        start = text.index(definition_start)
        end = text.index(definition_end, start)
        text = text[:start] + 'Jd=()=>null' + text[end:]
    text = text.replace('LeadModal', 'div')
    text = text.replace('HS=async e=>{console.warn(`WEBHOOK_URL no configurada; se omite el envío del lead.`)}', 'HS=async()=>{}')
    path.write_text(text, encoding='utf-8')

print('Calculadora de Sobrecostos Laborales depurada: descarga local sin modal ni correo.')
