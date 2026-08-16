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

## Aplicación 11 — Creador de Facturas Proforma

Se conservaron el cálculo de la proforma, la validación del documento, la descarga PDF, el historial y el respaldo/importación local. Se retiraron el correo del cliente, el `mailto:`, el script HTML duplicado de captación, la persistencia de leads en `vc859342100467.coderick.net`, la notificación por captcha en `/sgcaptcha/*` y la etiqueta residual `LeadModal` del metadato visual. El botón público quedó reducido a **Descargar**, sin dependencia de correo ni de servicios externos.

Los dos bundles pasan `node --check` y no quedan referencias al backend de leads, captcha, `coderick.net`, `mailto:` ni URLs de captación.

Estado: **depurada y validada estructuralmente**.

## Aplicación 12 — Firma de Correo HTML

Se conservó la creación local de firmas HTML, la personalización de datos y estilos, la vista previa y la copia/descarga del resultado. Se eliminaron el campo `input-correo`, los modales de captación, el envío externo y los elementos de previsualización administrativa de las páginas y bundles correspondientes.

Los bundles pasan `node --check` y la validación global no detecta campos de correo, formularios de leads, endpoints externos ni modales de captación.

Estado: **depurada y validada estructuralmente**.

## Aplicación 13 — Generador de Códigos QR

Se mantuvo la generación local de códigos QR y sus opciones de contenido y descarga. Se retiró la declaración de endpoint externo que no era necesaria para el flujo público y se conservaron únicamente las operaciones locales del generador.

Los bundles pasan `node --check` y no quedan residuos de captación, endpoints remotos ni rutas administrativas.

Estado: **depurada y validada estructuralmente**.

## Aplicación 14 — Generador de Contraseñas para Pymes

Se conservó la generación local de contraseñas, sus parámetros de longitud y complejidad, y las acciones de copia y uso inmediato. Se eliminó el modal de captación, la validación de correo y el captcha, junto con los elementos HTML que condicionaban el acceso a la herramienta.

Los bundles pasan `node --check` y no quedan referencias a `LeadModal`, `input-correo`, captcha, formularios de leads ni endpoints externos.

Estado: **depurada y validada estructuralmente**.

## Aplicación 15 — Generador de Contratos de Servicios

Se conservó el generador local de contratos, la edición de los datos del documento, la vista previa y la descarga del resultado. Se eliminó el flujo de bienvenida/captación y cualquier bloqueo que no formara parte de la generación del contrato.

Los bundles pasan `node --check` y la comprobación global confirma que la aplicación funciona sin captación de correo, paywall, panel administrativo ni endpoint externo de leads.

Estado: **depurada y validada estructuralmente**.

## Aplicación 16 — Generador de Cotizaciones

La auditoría estructural confirmó que esta aplicación no contiene `LeadModal`, `EmailGate`, formularios de captación, endpoints externos de leads ni rutas administrativas. Se conserva el correo del cliente únicamente como dato operativo para el enlace local `mailto:` de la cotización, junto con la generación, descarga, historial y redescarga del documento. Ambos bundles pasan `node --check`.

Estado: **auditada y limpia**.

## Aplicación 17 — Generador de Paletas Corporativas

Se conservaron la creación de paletas, la selección de colores, la previsualización y la copia/descarga de los resultados. Se retiró el endpoint remoto heredado que no era requerido por el generador local y se mantuvo la lógica pública sin dependencia de red.

Los bundles pasan `node --check` y no quedan residuos de captación, URLs externas prohibidas ni componentes administrativos.

Estado: **depurada y validada estructuralmente**.

## Aplicación 18 — Generador de Políticas de Devolución

Se conservaron la configuración local de la política, la generación del texto y las acciones de copia/descarga. Se eliminaron el campo de correo, el cliente remoto de `coderick.net`, el formulario de captación y los elementos HTML asociados a la entrega por correo.

Los bundles pasan `node --check` y no quedan referencias a `input-correo`, `coderick.net`, formularios de leads, captcha ni rutas administrativas.

Estado: **depurada y validada estructuralmente**.

## Aplicación 19 — LegalForge: Generador de Políticas y Términos

Se conservaron la selección y edición local de documentos legales, la generación del contenido y la descarga. Se eliminó el campo `input-correo` y el flujo de captación que condicionaba la entrega del resultado, dejando la herramienta disponible de forma directa y local.

Los bundles pasan `node --check` y la validación global confirma la ausencia de campos de correo, formularios de captación, paywalls, endpoints externos y paneles administrativos.

Estado: **depurada y validada estructuralmente**.

## Aplicación 20 — Guiones para Manejo de Objeciones

Se liberó el catálogo público de guiones sin paywall ni modal de desbloqueo. Se conservaron las contribuciones y el modo zen, y se reemplazaron los servicios remotos de tracking/moderación por operaciones locales sin red. Como corrección final se eliminó estructuralmente la ruta duplicada `/` que montaba el componente Admin `zi`, así como el componente administrativo completo.

Los dos bundles pasan `node --check`; las rutas públicas quedan limitadas a `/` y `*`, y no quedan referencias a `LeadModal`, captcha, `coderick.net`, `/admin` ni componentes administrativos.

Estado: **depurada, liberada y validada estructuralmente**.

## Aplicación 21 — Organizador de Matriz de Contenidos

Se conservaron la organización local de la matriz, la edición de elementos, las vistas de trabajo y la persistencia en el navegador. Se retiraron los bloqueos y residuos administrativos o de captación que no eran necesarios para gestionar la matriz.

Los bundles pasan `node --check` y la validación global no detecta captación de correo, paywalls, endpoints externos ni paneles administrativos.

Estado: **depurada y validada estructuralmente**.

## Aplicación 22 — Simulador TCO: Físico vs. Nube

Se conservó el simulador local de costo total de propiedad, con sus escenarios, cálculos comparativos y resultados para infraestructura física y nube. Se retiraron la captura de leads, el bloqueo de acceso, los elementos de administración y las dependencias externas de la versión publicada.

Los bundles pasan `node --check` y la comprobación global confirma que el simulador funciona sin correo, paywall, panel administrativo ni endpoint externo.

Estado: **depurada y validada estructuralmente**.

## Cierre del proyecto

Las 22 aplicaciones de la rama `ordered-cleanup` fueron auditadas y depuradas de forma ordenada. Se preservaron las funciones legítimas de cada herramienta —cálculos, generación de documentos, vistas previas, descargas, historial y persistencia local cuando correspondía— y se eliminaron estructuralmente los flujos de captación, bloqueos, paywalls, paneles administrativos y endpoints externos identificados.

La validación final ejecutada con `python3 scripts/validacion_global.py` informa `BUNDLES=22`, `SYNTAX_FAILURES=0`, `BUNDLE_RESIDUE_TOTAL=0`, `HTML_RESIDUE_TOTAL=0` y `GIT_STATUS CLEAN`. La corrección específica de App 20 quedó registrada en un commit independiente después del commit global de limpieza.

Estado final: **22 de 22 aplicaciones depuradas, liberadas y validadas**.


## Reestructuración de publicación estática

La publicación se reorganizó para eliminar la ambigüedad de rutas de GitHub Pages. El índice principal ahora está en `index.html` en la raíz del repositorio. Las 22 páginas de aplicaciones están juntas en `html/`, las hojas de estilo en `css/`, los bundles JavaScript en `js/` y los recursos compartidos en `assets/`.

Cada aplicación referencia sus recursos mediante rutas relativas desde `html/` (`../css/`, `../js/` y `../assets/`). El índice raíz enlaza explícitamente a `./html/<aplicacion>.html`, y el workflow de GitHub Pages publica la raíz del repositorio desde `main`.

La estructura fue comprobada con `scripts/validar_estructura_publica.py` y `scripts/validacion_global.py`: `ROOT_INDEX=1`, `HTML_APPS=22`, `CSS_FILES=23`, `JS_APP_BUNDLES=22`, `STRUCTURE_ERRORS=0`, `SYNTAX_FAILURES=0`, `BUNDLE_RESIDUE_TOTAL=0` y `HTML_RESIDUE_TOTAL=0`. Además, la verificación HTTP local confirmó respuesta 200 para la portada y las 22 aplicaciones.

Los scripts reproducibles de depuración fueron actualizados para trabajar sobre `html/` y `js/`, sin depender de las carpetas individuales heredadas.
