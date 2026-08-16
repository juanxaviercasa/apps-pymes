from pathlib import Path
import subprocess
import re

ROOT = Path('/home/ubuntu/apps-pymes')
js_files = sorted((ROOT / 'apps/js').glob('*.js'))
patterns = [
    'LeadModal', 'EmailGate', 'EmailGateModal', 'registrarLead',
    'script.google.com', 'TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI',
    'TU_ID_DE_SCRIPT', 'sgcaptcha', 'coderick.net', 'webhook.site',
    'input-correo', 'lead-form', '/admin', 'AdminPanel',
]
print(f'BUNDLES={len(js_files)}')
syntax_failures = []
for path in js_files:
    result = subprocess.run(['node', '--check', str(path)], capture_output=True, text=True)
    if result.returncode:
        syntax_failures.append((path.name, result.stderr.strip().splitlines()[-1] if result.stderr else 'unknown'))
print(f'SYNTAX_FAILURES={len(syntax_failures)}')
for name, err in syntax_failures:
    print(f'SYNTAX_FAIL {name}: {err}')
print('RESIDUES_BY_BUNDLE')
residue_total = 0
for path in js_files:
    text = path.read_text(encoding='utf-8', errors='replace')
    found = [(p, text.count(p)) for p in patterns if p in text]
    if found:
        residue_total += sum(n for _, n in found)
        print(path.name + ': ' + ', '.join(f'{p}={n}' for p, n in found))
print(f'BUNDLE_RESIDUE_TOTAL={residue_total}')
print('HTML_RESIDUES')
html_paths = sorted((ROOT / 'apps').glob('*.html'))
html_paths += sorted(p for p in ROOT.glob('*/index.html') if p.parent.name != 'node_modules')
html_total = 0
for path in html_paths:
    text = path.read_text(encoding='utf-8', errors='replace')
    found = [(p, text.count(p)) for p in patterns if p in text]
    if found:
        html_total += sum(n for _, n in found)
        print(path.relative_to(ROOT).as_posix() + ': ' + ', '.join(f'{p}={n}' for p, n in found))
print(f'HTML_RESIDUE_TOTAL={html_total}')
print('GIT_STATUS')
status = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True, text=True)
print(status.stdout.strip() or 'CLEAN')
