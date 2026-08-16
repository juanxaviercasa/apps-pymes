# Depuración ordenada de apps-pymes

## Criterio de trabajo

La rama `ordered-cleanup` parte de `origin/main`, commit `939dfee`, sin reutilizar el parche anterior. Cada aplicación se revisará de forma individual. Primero se identificará su flujo real; después se separarán las funciones útiles de los residuos; finalmente se modificará el HTML, el bundle y la copia publicada, y se comprobarán sintaxis y comportamiento antes de pasar a la siguiente.

No se eliminarán enlaces o funciones que formen parte del resultado esperado de una herramienta. Sí se eliminarán capturas de correo, endpoints de leads, bloqueos, checkout, paneles administrativos, telemetría, editores de previsualización y dependencias sin uso cuando no sean necesarios para la función principal.

## Aplicación 01 — Analizador de Titulares

La aplicación contiene un analizador local con edición de titular, sugerencias heurísticas, clasificación de tono, vista previa SERP, cálculo Bayesiano, comparación A/B, copia de informe y exportación PDF. Además incluía una captura de leads para “50 plantillas de titulares”.

La captura no tenía una entrega local de plantillas: el HTML apuntaba a `TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI` y el bundle enviaba el correo a `/sgcaptcha/contact` mediante un desafío PoW. Ese flujo era residuo de captación y no una función del analizador, por lo que se retiró estructuralmente de las dos páginas y de los dos bundles.

La función principal se conservó. Ambos bundles pasan `node --check`, y no quedan referencias activas a `LeadCapture`, `registrarLeadTitulares`, `TU_URL_DE_GOOGLE_APPS_SCRIPT`, `sgcaptcha/contact` ni al montaje de la sección de plantillas.

Estado: **depurada y validada estructuralmente**.
