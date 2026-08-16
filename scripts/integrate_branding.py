from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = '<link rel="stylesheet" href="./css/np-brand.css">'
SCRIPT = '<script src="./js/np-theme.js"></script>'


def integrate(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text
    if 'href="./css/np-brand.css"' not in text:
        if '</head>' not in text:
            raise RuntimeError(f'No se encontró </head> en {path.name}')
        text = text.replace('</head>', f'  {LINK}\n</head>', 1)
    if 'src="./js/np-theme.js"' not in text:
        if '</head>' not in text:
            raise RuntimeError(f'No se encontró </head> en {path.name}')
        text = text.replace('</head>', f'  {SCRIPT}\n</head>', 1)
    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


if __name__ == '__main__':
    pages = sorted(ROOT.glob('*.html'))
    changed = [p.name for p in pages if integrate(p)]
    print(f'Páginas revisadas: {len(pages)}')
    print(f'Páginas actualizadas: {len(changed)}')
    for name in changed:
        print(f'  - {name}')
