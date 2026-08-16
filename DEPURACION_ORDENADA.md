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

## Aplicación 04 — Calculadora de Flete y Envío Local

Se conservaron la calculadora de peso cobrable, zonas y paradas, cotización, historial local y generación del manifiesto/etiqueta de envío. Se retiró la sección `Lead Capture` de solicitud de proveedor logístico, junto con los campos de comercio, correo y teléfono, el envío a Google Apps Script y los mensajes de confirmación que prometían contacto externo.

En el bundle se eliminó la lógica de captación y se dejó el flujo principal sin dependencia de correo ni proveedor externo. Las dos copias de la aplicación pasan `node --check` y no quedan referencias a `LeadForm`, `lead-form`, `registrarLeadFlete`, `TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI`, `REEMPLAZA_CON_TU_ID`, `script.google.com/macros` ni `Solicitar proveedor logístico`.

Estado: **depurada y validada estructuralmente**.

## Aplicación 05 — Calculadora de Precios de Venta con IGV

Se conservaron las calculadoras de precio de venta, margen, impuesto/IGV, escenarios forward, actualización en tiempo real, historial local y descarga de PDF. Se eliminó el bloque `LeadCapture`, incluidos los campos de nombre y correo, el envío a Google Apps Script y el mensaje que prometía enviar el desglose por correo.

El montaje visible de `LeadCapture` fue retirado del flujo de resultados y los bundles pasan `node --check`. La comprobación no encuentra referencias a `LeadCapture`, `input-correo`, `registrarLead`, `TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI`, `script.google.com/macros`, `btn-enviar-lead` ni el texto de captación.

Estado: **depurada y validada estructuralmente**.

## Aplicación 06 — Calculadora de Préstamos y Amortizaciones

Se conservaron el cálculo de cuota, tabla de amortización, abonos extraordinarios a capital, historial local y comparador de escenarios A/B. Se retiró el flujo `LeadModal` de correo y exportación condicionada, junto con `AdminPanel` y el botón de administración. El footer administrativo queda oculto y con handler desactivado en el bundle para no mostrar controles internos en la versión pública.

Los dos bundles pasan `node --check` y la comprobación no encuentra referencias a `LeadModal`, `AdminPanel`, `Panel de administración`, `script.google.com`, `input-correo` ni `registrarLead`.

Estado: **depurada y validada estructuralmente**.

## Aplicación 07 — Calculadora de Sobrecostos Laborales

Se conservaron la gestión de empleados, cálculo de costo empleador, prestaciones, proyecciones mensual/anual, gráficos comparativos, almacenamiento local y generación de PDF. La descarga dejó de abrir `LeadModal`: ahora invoca directamente la generación local del reporte. Se retiró la definición completa del modal, sus validaciones de nombre/correo y el webhook de lead; la cabecera PDF ya no incluye correo del destinatario.

Los bundles pasan `node --check` y no quedan referencias a `LeadModal`, `input-correo`, `registrarLead`, `WEBHOOK_URL`, `script.google.com`, `Preparado para`, `n.correo` ni el handler que abría el modal.

Estado: **depurada y validada estructuralmente**.

## Aplicación 08 — Comparador Avanzado de Campañas

Se conservaron el alta y edición de campañas, simulador de presupuesto, tabla comparativa, filtros por plataforma, escenarios guardados en localStorage, gráfico de presupuesto versus ingresos, reporte PDF y exportación CSV. Se retiró la sección HTML de `EmailGate`, el script de registro por Google Apps Script y la lógica de correo persistente. El wrapper de acceso quedó convertido en un passthrough para que sus hijos se rendericen siempre; el estado principal inicia habilitado.

Los dos bundles pasan `node --check` y no quedan referencias a `EmailGate`, `input-correo`, `btn-enviar-lead`, `registrarLead`, `TU_URL_DE_GOOGLE_APPS_SCRIPT_AQUI`, `script.google.com`, `leadEmail`, `unlocked` ni el texto de bloqueo.

Estado: **depurada y validada estructuralmente**.

## Aplicación 09 — Consola de Campañas

Se conservaron el constructor UTM, fuentes y medios, simulador ROI, heatmap, enlaces simulados, panel local de campañas, carpetas y almacenamiento local del navegador. Se retiraron la sección HTML de captura de correo, el script de Google Apps Script, `LeadModal`, el captcha/contacto basado en `sgpowcaptcha` y sus endpoints `/sgcaptcha/*`. El montaje de confirmación quedó eliminado sin alterar los flujos locales de crear, borrar, quitar enlaces o sincronizar la interfaz.

Los dos bundles pasan `node --check` y no quedan referencias a correo, captación, LeadModal, captcha, endpoints externos ni formularios de suscripción.

Estado: **depurada y validada estructuralmente**.

## Aplicación 10 — Conversor y Optimizador de Imágenes

Se conservaron la conversión local mediante Canvas, optimización, procesamiento por lotes, descarga ZIP, formato WebP, calidad, redimensionado y marca de agua. Se retiraron la sección de curso WPO, el formulario HTML de correo, el script de Google Apps Script, el componente `LeadCapture`/`Rr`, el módulo captcha/contacto y los endpoints `/sgcaptcha/*`. También se eliminó el ancla de upsell del encabezado.

Los dos bundles pasan `node --check` y no quedan referencias a captación, curso, captcha, correo ni endpoints externos.

Estado: **depurada y validada estructuralmente**.
