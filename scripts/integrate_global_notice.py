from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(p for p in ROOT.glob('*.html') if p.name not in {'index.html', 'guia-uso-22-apps.html'})
DISCLAIMER = (
    'Aviso: los resultados son orientativos y se generan localmente. '
    'Verifica los datos, las fuentes y las normas aplicables antes de tomar '
    'decisiones comerciales, financieras, legales, laborales o tributarias.'
)
FOOTER = (
    '<footer class="np-global-footer">'
    '<span class="np-global-brand">NubeParaPymes · Herramienta local y gratuita.</span>'
    f'<span class="np-global-disclaimer">{DISCLAIMER}</span>'
    '<span class="np-global-links">'
    '<a class="np-footer-link np-footer-primary" href="https://apps.nubeparapymes.online/">Portal de apps</a>'
    '<a class="np-footer-link np-footer-secondary" href="https://nubeparapymes.online/">Sitio principal</a>'
    '</span>'
    '</footer>'
)

for path in PAGES:
    text = path.read_text(encoding='utf-8')
    if 'class="op-footer' in text:
        start = text.index('<footer class="op-footer')
        end = text.index('</footer>', start) + len('</footer>')
        text = text[:start] + FOOTER.replace('np-global-footer', 'op-footer np-global-footer', 1) + text[end:]
    elif '<footer class="np-global-footer"' in text:
        start = text.index('<footer class="np-global-footer"')
        end = text.index('</footer>', start) + len('</footer>')
        text = text[:start] + FOOTER + text[end:]
    elif 'class="np-global-footer"' not in text:
        marker = '</body>'
        if marker not in text:
            raise RuntimeError(f'No se encontró cierre body en {path.name}')
        text = text.replace(marker, FOOTER + '\n' + marker, 1)
    path.write_text(text, encoding='utf-8')

print(f'UPDATED_PAGES={len(PAGES)}')
