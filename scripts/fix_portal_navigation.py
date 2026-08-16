from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# The portal is rendered by this bundle at runtime; editing only index.html is insufficient.
bundle_path = ROOT / 'js' / 'index.js'
bundle = bundle_path.read_text(encoding='utf-8')
marker = 'icon:xp,category:"Operaciones"}];function vm'
new_records = (
    ',{name:"CRM y Pipeline Comercial",description:"Centraliza contactos, oportunidades y seguimientos para convertir conversaciones en ventas.",slug:"./crm-pymes.html",icon:am,category:"Ventas"}'
    ',{name:"Flujo de Caja y Cobranzas",description:"Registra ingresos, egresos, vencimientos y pendientes para anticipar problemas de liquidez.",slug:"./flujo-caja-pymes.html",icon:cm,category:"Finanzas"}'
    ',{name:"Inventario, Proveedores y Compras",description:"Controla productos, stock mínimo, proveedores y compras de reposición.",slug:"./inventario-compras-pymes.html",icon:kp,category:"Operaciones"}'
    ',{name:"Tareas y Proyectos Operativos",description:"Organiza proyectos, responsables, prioridades y fechas de entrega.",slug:"./tareas-proyectos-pymes.html",icon:_p,category:"Productividad"}'
)
if 'slug:"./crm-pymes.html"' not in bundle:
    if marker not in bundle:
        raise SystemExit('No se encontró el final esperado del arreglo de herramientas en js/index.js')
    bundle = bundle.replace(marker, 'icon:xp,category:"Operaciones"}' + new_records + '];function vm', 1)
bundle_path.write_text(bundle, encoding='utf-8')

index_path = ROOT / 'index.html'
index = index_path.read_text(encoding='utf-8')
index = index.replace('22 herramientas gratuitas', '26 herramientas gratuitas')
index = index.replace('22 resultados', '26 resultados')
index = index.replace('>22</span>', '>26</span>')

# Update the category counters in the filter bar only.
for category, old, new in (
    ('Finanzas', '4', '5'),
    ('Ventas', '4', '5'),
    ('Operaciones', '2', '3'),
    ('Productividad', '4', '5'),
):
    pattern = rf'(>\s*{category}\s*<span[^>]*>)\s*{old}(\s*</span>)'
    index, count = re.subn(pattern, rf'\g<1>{new}\g<2>', index, count=1, flags=re.S)
    if count == 0:
        already_new = re.search(rf'>\s*{category}\s*<span[^>]*>\s*{new}\s*</span>', index, flags=re.S)
        if not already_new:
            raise SystemExit(f'No se pudo actualizar el contador de {category}')

new_cards = '''
          <!-- Card 23 -->
          <div>
            <article class="group flex h-full flex-col rounded-panel border border-line bg-surface p-6 shadow-[0_1px_2px_rgba(10,25,47,0.04)] transition-all duration-300 hover:-translate-y-1 hover:border-brand hover:shadow-[0_18px_40px_-18px_rgba(30,58,138,0.35)]">
              <div class="mb-5 flex items-start justify-between"><div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand/10 text-royal transition-colors duration-300 group-hover:bg-brand group-hover:text-white dark:text-brand-soft"><span class="font-display text-lg font-extrabold">23</span></div><button type="button" aria-pressed="false" aria-label="Agregar CRM y Pipeline Comercial a favoritos" class="rounded-lg p-1.5 text-fg-muted transition-colors hover:bg-cta/10 hover:text-cta"><span aria-hidden="true">☆</span></button></div>
              <span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">Ventas</span>
              <h3 class="font-display text-lg font-bold leading-snug text-fg">CRM y Pipeline Comercial</h3>
              <p class="mt-2 flex-1 text-sm leading-relaxed text-fg-muted">Centraliza contactos, oportunidades y seguimientos para convertir conversaciones en ventas.</p>
              <a href="./crm-pymes.html" class="mt-6 inline-flex items-center justify-center gap-2 rounded-lg bg-cta px-4 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-cta-strong">Abrir Herramienta <span aria-hidden="true">→</span></a>
            </article>
          </div>
          <!-- Card 24 -->
          <div>
            <article class="group flex h-full flex-col rounded-panel border border-line bg-surface p-6 shadow-[0_1px_2px_rgba(10,25,47,0.04)] transition-all duration-300 hover:-translate-y-1 hover:border-brand hover:shadow-[0_18px_40px_-18px_rgba(30,58,138,0.35)]">
              <div class="mb-5 flex items-start justify-between"><div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand/10 text-royal transition-colors duration-300 group-hover:bg-brand group-hover:text-white dark:text-brand-soft"><span class="font-display text-lg font-extrabold">24</span></div><button type="button" aria-pressed="false" aria-label="Agregar Flujo de Caja y Cobranzas a favoritos" class="rounded-lg p-1.5 text-fg-muted transition-colors hover:bg-cta/10 hover:text-cta"><span aria-hidden="true">☆</span></button></div>
              <span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">Finanzas</span>
              <h3 class="font-display text-lg font-bold leading-snug text-fg">Flujo de Caja y Cobranzas</h3>
              <p class="mt-2 flex-1 text-sm leading-relaxed text-fg-muted">Registra ingresos, egresos, vencimientos y pendientes para anticipar problemas de liquidez.</p>
              <a href="./flujo-caja-pymes.html" class="mt-6 inline-flex items-center justify-center gap-2 rounded-lg bg-cta px-4 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-cta-strong">Abrir Herramienta <span aria-hidden="true">→</span></a>
            </article>
          </div>
          <!-- Card 25 -->
          <div>
            <article class="group flex h-full flex-col rounded-panel border border-line bg-surface p-6 shadow-[0_1px_2px_rgba(10,25,47,0.04)] transition-all duration-300 hover:-translate-y-1 hover:border-brand hover:shadow-[0_18px_40px_-18px_rgba(30,58,138,0.35)]">
              <div class="mb-5 flex items-start justify-between"><div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand/10 text-royal transition-colors duration-300 group-hover:bg-brand group-hover:text-white dark:text-brand-soft"><span class="font-display text-lg font-extrabold">25</span></div><button type="button" aria-pressed="false" aria-label="Agregar Inventario, Proveedores y Compras a favoritos" class="rounded-lg p-1.5 text-fg-muted transition-colors hover:bg-cta/10 hover:text-cta"><span aria-hidden="true">☆</span></button></div>
              <span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">Operaciones</span>
              <h3 class="font-display text-lg font-bold leading-snug text-fg">Inventario, Proveedores y Compras</h3>
              <p class="mt-2 flex-1 text-sm leading-relaxed text-fg-muted">Controla productos, stock mínimo, proveedores y compras de reposición.</p>
              <a href="./inventario-compras-pymes.html" class="mt-6 inline-flex items-center justify-center gap-2 rounded-lg bg-cta px-4 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-cta-strong">Abrir Herramienta <span aria-hidden="true">→</span></a>
            </article>
          </div>
          <!-- Card 26 -->
          <div>
            <article class="group flex h-full flex-col rounded-panel border border-line bg-surface p-6 shadow-[0_1px_2px_rgba(10,25,47,0.04)] transition-all duration-300 hover:-translate-y-1 hover:border-brand hover:shadow-[0_18px_40px_-18px_rgba(30,58,138,0.35)]">
              <div class="mb-5 flex items-start justify-between"><div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand/10 text-royal transition-colors duration-300 group-hover:bg-brand group-hover:text-white dark:text-brand-soft"><span class="font-display text-lg font-extrabold">26</span></div><button type="button" aria-pressed="false" aria-label="Agregar Tareas y Proyectos Operativos a favoritos" class="rounded-lg p-1.5 text-fg-muted transition-colors hover:bg-cta/10 hover:text-cta"><span aria-hidden="true">☆</span></button></div>
              <span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">Productividad</span>
              <h3 class="font-display text-lg font-bold leading-snug text-fg">Tareas y Proyectos Operativos</h3>
              <p class="mt-2 flex-1 text-sm leading-relaxed text-fg-muted">Organiza proyectos, responsables, prioridades y fechas de entrega.</p>
              <a href="./tareas-proyectos-pymes.html" class="mt-6 inline-flex items-center justify-center gap-2 rounded-lg bg-cta px-4 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-cta-strong">Abrir Herramienta <span aria-hidden="true">→</span></a>
            </article>
          </div>
'''
# Put the four cards in the same grid as the original 22.
grid_end = '\n        </div>\n\n      </main>'
if '<!-- Card 23 -->' not in index:
    if grid_end not in index:
        raise SystemExit('No se encontró el cierre de la cuadrícula principal')
    index = index.replace(grid_end, '\n' + new_cards + '        </div>\n\n      </main>', 1)
# Remove the old standalone block to prevent duplication in static fallback.
index, removed = re.subn(r'\n\s*<!-- Nuevas herramientas operativas para pymes -->.*?</section>\n', '\n', index, count=1, flags=re.S)
if removed not in (0, 1):
    raise SystemExit('Resultado inesperado al eliminar la sección operativa separada')
index_path.write_text(index, encoding='utf-8')

# Make the operational app logo an explicit home link.
for name in ('crm-pymes.html','flujo-caja-pymes.html','inventario-compras-pymes.html','tareas-proyectos-pymes.html'):
    path = ROOT / name
    html = path.read_text(encoding='utf-8')
    if 'class="op-brand-link"' not in html:
        pattern = r'<div class="op-brand"><div class="op-logo">([^<]*)</div><div><h1>'
        replacement = r'<div class="op-brand"><a class="op-brand-link" href="./index.html" aria-label="Volver al portal principal"><div class="op-logo">\1</div></a><div><h1>'
        html, count = re.subn(pattern, replacement, html, count=1)
        if count != 1:
            raise SystemExit(f'No se encontró el encabezado esperado en {name}')
    path.write_text(html, encoding='utf-8')

css_path = ROOT / 'css' / 'operaciones-pyme.css'
css = css_path.read_text(encoding='utf-8')
if '.op-brand-link' not in css:
    css += '\n.op-brand-link{display:inline-flex;color:inherit;text-decoration:none;border-radius:14px}.op-brand-link:focus-visible{outline:3px solid #60a5fa;outline-offset:3px}.op-brand-link:hover .op-logo{transform:translateY(-1px);box-shadow:0 10px 24px rgba(37,99,235,.25)}\n'
    css_path.write_text(css, encoding='utf-8')
print('PORTAL_NAVIGATION_FIXED')
