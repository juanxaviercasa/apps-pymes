# Depuración ordenada de apps-pymes

## Criterio de trabajo

La rama `ordered-cleanup` parte de `origin/main`, commit `939dfee`, sin reutilizar el parche anterior. Cada aplicación se revisará de forma individual. Primero se identificará su flujo real; después se separarán las funciones útiles de los residuos; finalmente se modificará el HTML, el bundle y la copia publicada, y se comprobarán sintaxis y comportamiento antes de pasar a la siguiente.

No se eliminarán enlaces o funciones que formen parte del resultado esperado de una herramienta. Sí se eliminarán capturas de correo, endpoints de leads, bloqueos, checkout, paneles administrativos, telemetría, editores de previsualización y dependencias sin uso cuando no sean necesarios para la función principal.

## Aplicación 01 — Analizador de Titulares

La aplicación contiene un analizador local con edición de titular, sugerencias heurísticas, clasificación de tono, vista previa SERP, cálculo Bayesiano, comparación A/B, copia de informe y exportación PDF. Además incluía una captura de leads para “50 plantillas de titulares”.

La captura no tenía una entrega local de plantillas: el HTML apuntaba a `TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI` y el bundle enviaba el correo a `/sgcaptcha/contact` mediante un desafío PoW. Ese flujo era residuo de captación y no una función del analizador, por lo que se retiró estructuralmente de las dos páginas y de los dos bundles.

La función principal se conservó. Ambos bundles pasan `node --check`, y no quedan referencias activas a `LeadCapture`, `registrarLeadTitulares`, `TU_URL_DE_GOOGLE_APPS_SCRIPT`, `sgcaptcha/contact` ni al montaje de la sección de plantillas.

Estado: **depurada y validada estructuralmente**.

## Aplicación 02 — Auditor Básico de SEO On-Page

La aplicación conserva el auditor local de URL, metatítulos, descripciones, palabras clave, H1, vistas previas SERP y sociales, checklist de salud, sugerencias, lista de tareas, densidad de contenido, comparador, historial local y los controles de análisis existentes.

Se identificó una sección de upsell que prometía una auditoría completa y abría `LeadModal`. El modal enviaba un correo a `/sgcaptcha/contact` y no producía el informe avanzado dentro de la aplicación. Se eliminó la sección del HTML, el script de captación, el montaje del modal y la definición completa del componente muerto en ambos bundles. También se conservaron las funciones locales y el historial.

Ambos bundles pasan `node --check` y no quedan referencias a `LeadModal`, `sgcaptcha/contact`, `Obtener auditoría completa gratis`, la sección de upsell ni `TU_URL_DE_GOOGLE_APPS_SCRIPT`.

Estado: **depurada y validada estructuralmente**.

## Aplicación 03 — Calculadora de Descuentos y Promociones

La función útil de esta aplicación está compuesta por las calculadoras de precio promocional, margen, punto de equilibrio, combos, valor de vida del cliente, textos de copywriting y campaña flash. Todas trabajan con los datos ingresados localmente y se conservaron.

Se eliminaron la sección `LeadForm`, los campos de nombre, correo y negocio, el envío a `TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI`, el enlace y la ruta `/admin`, y las funciones completas de administración y captación que quedaron sin consumidor. La depuración se aplicó en las dos páginas y en los dos bundles.

Ambos bundles pasan `node --check` y no quedan referencias a `LeadForm`, `input-correo`, `registrarLead`, `TU_URL_DE_GOOGLE_APPS_SCRIPT`, `Panel de administración`, `function nm`, `function Jp` ni la ruta `/admin`.

Estado: **depurada y validada estructuralmente**.
