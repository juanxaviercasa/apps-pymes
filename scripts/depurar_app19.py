from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'apps/generador-politicas-terminos.html', ROOT / 'generador-politicas-terminos/index.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'<form[^>]*(?:id|name)=["\'][^"\']*(?:lead|email)["\'][^>]*>.*?</form>', '', text, count=1, flags=re.S | re.I)
    text = re.sub(r'\s*<label[^>]*>.*?<input[^>]*id="input-correo".*?</label>\s*', '\n', text, count=1, flags=re.S | re.I)
    text = re.sub(r'<script>\s*function registrarLead\(event\).*?</script>', '', text, count=1, flags=re.S)
    text = text.replace('registrarLead', '').replace('URL_DE_TU_GOOGLE_APPS_SCRIPT', '')
    text = re.sub(r'[ \t]+\n', '\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'apps/js/generador-politicas-terminos.js', ROOT / 'generador-politicas-terminos/assets/index.js']:
    text = path.read_text(encoding='utf-8', errors='replace')

    # Remove PocketBase/captcha lead persistence and notification helpers.
    start_marker = 'si=new oi(`https://vc412399443444.coderick.net`);'
    end_marker = 'var di=o('
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        text = text[:start] + end_marker + text[end + len(end_marker):]
        text = text.replace('}},var di=o(', '}};var di=o(', 1)

    # Remove the complete StepContact component, leaving the legal and document components intact.
    contact_start = 'function vi({form:e,set:t,errors:n})'
    contact_end = 'function yi('
    if contact_start in text and contact_end in text:
        start = text.index(contact_start)
        end = text.index(contact_end, start)
        text = text[:start] + text[end:]

    # Skip the former contact step and render the document-ready state after the legal step.
    text = text.replace('n===2&&(0,j.jsx)(vi,{form:e,set:g,errors:i,"data-visual-edit-loc":`src/pages/Index.tsx:151:31`,"data-visual-edit-component":`StepContact`,"data-visual-edit-editable":`false`}),', '')
    text = text.replace('n===2&&`Recibe tus documentos`,', 'n===2&&`¡Documentos listos!`,')
    text = text.replace('n===2&&`Te enviaremos una copia a tu correo.`,', 'n===2&&`Cópialos, descárgalos o publica el banner en tu web.`,')
    text = text.replace('n===2&&(e.contactName.trim()||(t.contactName=`Indica tu nombre.`),/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(e.email.trim())||(t.email=`Introduce un correo electrónico válido.`)),', '')
    text = re.sub(r'if\(n===2\)\{s\(!0\);try\{await ui\(e\),r\(3\),d\(`preview`\)\}catch\(e\)\{console\.error\(e\),a\(e=>\(\{\.\.\.e,email:`No se pudo enviar\. Revisa tus datos e inténtalo de nuevo\.`\}\)\)\}finally\{s\(!1\)\}return\}', 'if(n===2){r(3),d(`preview`);return}', text, count=1)
    text = text.replace('locked:!h', 'locked:!1')
    text = text.replace('LeadModal', '').replace('/sgcaptcha/', '')
    path.write_text(text, encoding='utf-8')

print('Generador de Políticas y Términos depurado: leads, captcha, contacto obligatorio y bloqueo retirados; generación, copia y descargas preservadas.')

if __name__ == '__main__':
    pass

