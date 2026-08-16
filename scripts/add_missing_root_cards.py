from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'
text = INDEX.read_text(encoding='utf-8', errors='replace')
marker = '\n        </div>\n\n      </main>'
if text.count(marker) != 1:
    raise SystemExit('No se encontró un cierre único del catálogo de herramientas.')

cards = '''

          <!-- Card 21 -->
          <div>
            <article class="group flex h-full flex-col rounded-panel border border-line bg-surface p-6 shadow-[0_1px_2px_rgba(10,25,47,0.04)] transition-all duration-300 hover:-translate-y-1 hover:border-brand hover:shadow-[0_18px_40px_-18px_rgba(30,58,138,0.35)]">
              <div class="mb-5 flex items-start justify-between">
                <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand/10 text-royal transition-colors duration-300 group-hover:bg-brand group-hover:text-white dark:text-brand-soft">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6" aria-hidden="true"><rect x="3" y="11" width="18" height="10" rx="2"></rect><path d="M7 11V8a5 5 0 0 1 10 0v3"></path><path d="M8 16h.01M12 16h.01M16 16h.01"></path></svg>
                </div>
                <button type="button" aria-pressed="false" aria-label="Agregar Generador de Contraseñas para Pymes a favoritos" class="rounded-lg p-1.5 text-fg-muted transition-colors hover:bg-cta/10 hover:text-cta focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cta">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5" aria-hidden="true"><path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9z"></path></svg>
                </button>
              </div>
              <span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">Seguridad</span>
              <h3 class="font-display text-lg font-bold leading-snug text-fg">Generador de Contraseñas para Pymes</h3>
              <p class="mt-2 flex-1 text-sm leading-relaxed text-fg-muted">Crea contraseñas seguras y personalizadas de forma local, rápida y gratuita.</p>
              <a href="./generador-contrasenas-pymes.html" class="mt-6 inline-flex items-center justify-center gap-2 rounded-lg bg-cta px-4 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-cta-strong focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cta">Abrir Herramienta<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></a>
            </article>
          </div>

          <!-- Card 22 -->
          <div>
            <article class="group flex h-full flex-col rounded-panel border border-line bg-surface p-6 shadow-[0_1px_2px_rgba(10,25,47,0.04)] transition-all duration-300 hover:-translate-y-1 hover:border-brand hover:shadow-[0_18px_40px_-18px_rgba(30,58,138,0.35)]">
              <div class="mb-5 flex items-start justify-between">
                <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand/10 text-royal transition-colors duration-300 group-hover:bg-brand group-hover:text-white dark:text-brand-soft">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><path d="M14 2v6h6"></path><path d="M8 13h8M8 17h6"></path></svg>
                </div>
                <button type="button" aria-pressed="false" aria-label="Agregar Generador de Contratos de Servicios a favoritos" class="rounded-lg p-1.5 text-fg-muted transition-colors hover:bg-cta/10 hover:text-cta focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cta">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5" aria-hidden="true"><path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9z"></path></svg>
                </button>
              </div>
              <span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">Legal y Administración</span>
              <h3 class="font-display text-lg font-bold leading-snug text-fg">Generador de Contratos de Servicios</h3>
              <p class="mt-2 flex-1 text-sm leading-relaxed text-fg-muted">Redacta contratos de servicios editables con una plantilla local para tu negocio.</p>
              <a href="./generador-contratos-servicios.html" class="mt-6 inline-flex items-center justify-center gap-2 rounded-lg bg-cta px-4 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-cta-strong focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cta">Abrir Herramienta<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></a>
            </article>
          </div>'''
INDEX.write_text(text.replace(marker, cards + marker), encoding='utf-8')
print('TARJETAS_RAIZ_AGREGADAS=2')
