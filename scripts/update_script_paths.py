from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
for path in sorted((ROOT / 'scripts').glob('depurar_*.py')):
    text = path.read_text(encoding='utf-8')
    # HTML publicados: apps/<nombre>.html o <nombre>/index.html -> html/<nombre>.html.
    updated = re.sub(r"ROOT / 'apps/([^']+\.html)'", r"ROOT / 'html/\1'", text)
    updated = re.sub(r"ROOT / '([^']+)/index\.html'", r"ROOT / '\1.html'", updated)
    # Bundles: conservar un único destino por aplicación en js/.
    updated = re.sub(r", ROOT / '[^']+/assets/index\.js'", '', updated)
    updated = re.sub(r"(    ROOT / 'html/[^']+\.html',\n)\1", r"\1", updated)
    if updated != text:
        path.write_text(updated, encoding='utf-8')

# Scripts de corrección del portal también deben operar sobre js/index.js.
for name in ('fix_root_index_links.py', 'fix_root_router_base.py'):
    path = ROOT / 'scripts' / name
    if path.exists():
        text = path.read_text(encoding='utf-8')
        text = text.replace("ROOT / 'apps/assets/index.js'", "ROOT / 'js/index.js'")
        path.write_text(text, encoding='utf-8')

print('RUTAS_SCRIPTS_ACTUALIZADAS')
