# Prompt adaptado: datos compartidos locales para las 26 apps

## Objetivo

Implementa una capa de datos compartidos para las **26 aplicaciones** de `apps.nubeparapymes.online`. Todas viven en el mismo origen, por lo que pueden acceder al mismo `localStorage`. La solución debe permitir que una app lea referencias creadas por otra sin mezclar sus claves privadas, sin sobrescribir datos de trabajo y sin usar correo, Google Sheets, Apps Script, APIs, webhooks, `fetch` ni servicios externos.

La solución debe seguir siendo estática, gratuita, local y compatible con GitHub Pages y un hosting que solo sirva `public_html`.

## Reglas obligatorias

1. No crear captura de correo, formularios de lead, paywalls ni bloqueos.
2. No enviar datos fuera del navegador.
3. No reemplazar las claves privadas de ninguna app.
4. Guardar el estado compartido únicamente bajo `np_shared_v1`.
5. Mantener una identidad por aplicación mediante `data-app-id` y `data-app-name`.
6. El puente no debe mostrar modales, avisos obligatorios ni interponerse al cargar una app.
7. La importación y exportación JSON son opcionales y deben funcionar por solicitud del usuario.
8. Si una app no tiene datos, no crear copias vacías ni registros fantasma.
9. Ante conflicto, conservar el registro más reciente y mantener el registro original de la app de origen.
10. Cualquier dato desconocido o corrupto debe ignorarse y no debe entrar al estado compartido.

## Contrato de datos

La clave común tiene el siguiente esquema:

```json
{
  "schema": "nubepymes-shared",
  "schemaVersion": 1,
  "updatedAt": "ISO-8601",
  "contacts": [],
  "companies": [],
  "opportunities": [],
  "quotes": [],
  "transactions": [],
  "products": [],
  "suppliers": [],
  "projects": [],
  "tasks": [],
  "campaigns": [],
  "scenarios": [],
  "content": [],
  "sources": {}
}
```

Cada registro reflejado debe conservar `_sourceKey`, `_sharedId` y `_mirroredAt`. Las claves privadas actuales de cada app siguen existiendo y continúan siendo la fuente de trabajo de esa app.

## Mapa de fuentes conocidas

| Clave local de origen | Datos compartidos |
|---|---|
| `np_crm_pymes_v1` | `contacts`, `opportunities` |
| `qg_clients`, `pf_clients_v1` | `contacts` |
| `qg_catalog`, `pf_products_v1` | `products` |
| `qg_history`, `pf_history_v1` | `quotes` |
| `np_flujo_caja_pymes_v1` | `transactions` |
| `np_inventario_compras_pymes_v1` | `products`, `suppliers` |
| `np_tareas_proyectos_pymes_v1` | `projects`, `tasks` |
| `campaigns` | `campaigns` |
| `scenarios` | `scenarios` |
| `utm_campaigns` | `campaigns` |
| `matriz-contenidos-v2` | `content` |
| `tco-saved-scenarios` | `scenarios` |

Las claves de cotizaciones y proformas se incorporan mediante adaptadores explícitos: clientes a `contacts`, catálogos/productos a `products` e historiales a `quotes`. Sus claves privadas permanecen intactas.

## API disponible

El runtime común se carga como `./js/datos-compartidos.js` antes del bundle de cada aplicación y expone `window.npShared`:

```javascript
const contactos = window.npShared.list('contacts');
const oportunidades = window.npShared.list('opportunities');
const productos = window.npShared.list('products');

const unsubscribe = window.npShared.subscribe((tipo, detalle) => {
  // Actualizar solo una vista no destructiva cuando otra app cambie datos.
});

window.npShared.upsert('tasks', {
  id: 'tarea-local-1',
  name: 'Revisar propuesta',
  status: 'Pendiente'
});
```

`list()` devuelve copias, `upsert()` solo acepta colecciones conocidas y `remove()` requiere un identificador explícito. Ninguna operación del puente borra una clave privada de aplicación.

## Integración por aplicación

Las 26 páginas deben cargar el runtime común y recibir identidad local. Las aplicaciones operativas nuevas utilizan sus modelos existentes y se reflejan automáticamente al escribir en `localStorage`. Las aplicaciones de campañas, contenidos y escenarios se reflejan mediante el mapa anterior. Las aplicaciones de cotizaciones y proformas deben usar adaptadores controlados para publicar contactos, productos y documentos solo después de confirmar la forma real de sus datos.

Las vistas que consuman información compartida deben mostrarla como referencia o selector opcional. No deben sustituir automáticamente formularios ni crear relaciones silenciosas. El usuario siempre debe poder continuar trabajando aunque el estado compartido esté vacío, corrupto o no exista.

## Respaldo

Las aplicaciones con respaldo local incluyen `np_shared_v1` dentro del respaldo, junto a sus propias claves. El respaldo debe ignorar estados vacíos, validar esquema y mantener copias preventivas antes de restaurar. La exportación e importación permanecen locales y no requieren correo.

## Pruebas obligatorias

1. Abrir cada una de las 26 apps en un origen limpio.
2. Confirmar que ninguna muestra un modal al cargar.
3. Crear un contacto en CRM y comprobar que aparece en `npShared.list('contacts')` desde otra app.
4. Crear un producto en inventario y comprobar su reflejo compartido.
5. Crear una campaña y verificar que el registro común se actualiza.
6. Confirmar que borrar datos propios de una app no elimina automáticamente otras colecciones.
7. Probar importación de un respaldo válido, antiguo, corrupto y perteneciente a otra app.
8. Confirmar ausencia de `fetch`, correo, Apps Script, webhooks y endpoints externos.
9. Ejecutar validadores estructural y global.

## Resultado esperado

Las 26 aplicaciones deben seguir funcionando de forma independiente, pero compartir referencias útiles de clientes, oportunidades, caja, inventario, proyectos, campañas y contenidos cuando exista información. La arquitectura debe permanecer local, explícita, reversible y sin dependencias de servidor.
