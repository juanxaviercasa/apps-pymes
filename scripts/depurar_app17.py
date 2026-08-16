from pathlib import Path
import re

ROOT = Path('/home/ubuntu/apps-pymes')

for path in [ROOT / 'generador-paletas-corporativas.html', ROOT / 'generador-paletas-corporativas.html']:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'<form[^>]*(?:id|name)=["\'][^"\']*(?:lead|email)[^"\']*["\'][^>]*>.*?</form>', '', text, count=1, flags=re.S | re.I)
    text = re.sub(r'\s*<script>\s*function registrarLeadChroma\(event\).*?</script>\s*', '\n', text, count=1, flags=re.S)
    text = text.replace('registrarLeadChroma', '')
    text = text.replace('TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI', '')
    text = re.sub(r'[ \t]+\n', '\n', text)
    path.write_text(text, encoding='utf-8')

for path in [ROOT / 'js/generador-paletas-corporativas.js']:
    text = path.read_text(encoding='utf-8', errors='replace')

    # Captcha/contact helper and LeadModal are used only by the lead-capture flow.
    captcha_start = 'function fp(e,t)'
    captcha_end = 'var gp=/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;'
    if captcha_start in text and captcha_end in text:
        start = text.index(captcha_start)
        end = text.index(captcha_end, start)
        text = text[:start] + text[end:]

    lead_start = 'var gp=/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;function _p'
    lead_end = 'function bp'
    if lead_start in text and lead_end in text:
        start = text.index(lead_start)
        end = text.index(lead_end, start)
        text = text[:start] + text[end:]

    text = re.sub(r'\(0,J\.jsx\)\(_p,\{open:i,onClose:\(\)=>a\(!1\),.*?\}\),', '', text, count=1)
    text = text.replace('LeadModal', '')
    text = text.replace('/sgcaptcha/contact', '')
    text = text.replace('/sgcaptcha/', '')
    path.write_text(text, encoding='utf-8')

print('Generador de Paletas Corporativas depurado: captación, captcha y LeadModal retirados; paletas, compilador y descarga PDF preservados.')

if __name__ == '__main__':
    pass

