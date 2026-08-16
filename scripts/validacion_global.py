from pathlib import Path
import subprocess

ROOT = Path('/home/ubuntu/apps-pymes')
all_js_files = sorted((ROOT / 'js').glob('*.js'))
app_js_files = [path for path in all_js_files if path.name not in {'index.js', 'ayuda-apps.js', 'respaldo-local.js', 'datos-compartidos.js'}]
patterns = [
    'LeadModal', 'EmailGate', 'EmailGateModal', 'registrarLead',
    'script.google.com', 'TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI',
    'TU_ID_DE_SCRIPT', 'sgcaptcha', 'coderick.net', 'webhook.site',
    'input-correo', 'lead-form', '/admin', 'AdminPanel',
]
print(f'BUNDLES={len(app_js_files)}')
syntax_failures = []
for path in all_js_files:
    result = subprocess.run(['node', '--check', str(path)], capture_output=True, text=True)
    if result.returncode:
        syntax_failures.append((path.name, result.stderr.strip().splitlines()[-1] if result.stderr else 'unknown'))
print(f'SYNTAX_FAILURES={len(syntax_failures)}')
for name, err in syntax_failures:
    print(f'SYNTAX_FAIL {name}: {err}')
print('RESIDUES_BY_BUNDLE')
residue_total = 0
for path in all_js_files:
    text = path.read_text(encoding='utf-8', errors='replace')
    found = [(pattern, text.count(pattern)) for pattern in patterns if pattern in text]
    if found:
        residue_total += sum(count for _, count in found)
        print(path.name + ': ' + ', '.join(f'{pattern}={count}' for pattern, count in found))
print(f'BUNDLE_RESIDUE_TOTAL={residue_total}')
print('HTML_RESIDUES')
html_paths = [ROOT / 'index.html'] + sorted(path for path in ROOT.glob('*.html') if path.name not in {'index.html', 'guia-uso-22-apps.html'})
html_total = 0
for path in html_paths:
    text = path.read_text(encoding='utf-8', errors='replace')
    found = [(pattern, text.count(pattern)) for pattern in patterns if pattern in text]
    if found:
        html_total += sum(count for _, count in found)
        print(path.relative_to(ROOT).as_posix() + ': ' + ', '.join(f'{pattern}={count}' for pattern, count in found))
print(f'HTML_RESIDUE_TOTAL={html_total}')
print('GIT_STATUS')
status = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True, text=True)
print(status.stdout.strip() or 'CLEAN')
