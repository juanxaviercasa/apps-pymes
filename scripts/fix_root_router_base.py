from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'js/index.js'
text = BUNDLE.read_text(encoding='utf-8', errors='replace')
old = '(0,K.jsx)(un,{"data-visual-edit-loc":`src/App.tsx:6:2`'
new = '(0,K.jsx)(un,{"basename":location.pathname.startsWith(`/apps-pymes`)?`/apps-pymes`:void 0,"data-visual-edit-loc":`src/App.tsx:6:2`'
if old not in text:
    if '"basename":location.pathname.startsWith(`/apps-pymes`)' in text:
        print('El basename del portal ya está configurado.')
    else:
        raise SystemExit('No se encontró el montaje BrowserRouter del portal raíz.')
else:
    BUNDLE.write_text(text.replace(old, new, 1), encoding='utf-8')
    print('Basename /apps-pymes añadido al BrowserRouter del portal raíz.')
