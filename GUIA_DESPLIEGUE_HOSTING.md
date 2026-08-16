# Guía de despliegue e instalación de NubeParaPymes

**Versión:** estructura estática consolidada en `main`  
**Autor:** Manus AI  
**Tipo de proyecto:** sitio estático HTML, CSS y JavaScript; no requiere Node.js, PHP, base de datos ni variables de entorno para ejecutarse en producción.

## 1. Objetivo de esta guía

Esta guía documenta la forma correcta de instalar y publicar las 22 aplicaciones de NubeParaPymes en GitHub Pages, cPanel, Apache, Nginx, Netlify, Cloudflare Pages u otro hosting estático. El objetivo es evitar los dos problemas que aparecieron durante las primeras publicaciones: errores **404 por rutas o carpetas incorrectas** y pantallas vacías o azules producidas por recursos JavaScript/CSS que no se cargan o por errores de ejecución.

La versión publicada es completamente local y estática. Las aplicaciones no deben instalarse ejecutando cada carpeta por separado. Debe publicarse el **contenido completo de la raíz del repositorio** como un único sitio.

> **Regla principal:** el archivo `index.html`, los 22 HTML de aplicaciones, `css/`, `js/` y `assets/` deben quedar en el mismo nivel raíz del directorio público del hosting.

## 2. Estructura que debe publicarse

La estructura pública correcta es la siguiente:

```text
DIRECTORIO_PUBLICO/
├── index.html
├── auditor-seo-basico.html
├── analizador-titulares.html
├── calculadora-descuentos-promociones.html
├── calculadora-flete-envio-local.html
├── calculadora-precios-venta-igv.html
├── calculadora-prestamos-amortizaciones.html
├── calculadora-sobrecostos-laborales.html
├── comparador-campanas-avanzado.html
├── consola-campanas.html
├── conversor-optimizador-imagenes.html
├── creador-facturas-proforma.html
├── firma-correo-html.html
├── generador-codigos-qr.html
├── generador-contrasenas-pymes.html
├── generador-contratos-servicios.html
├── generador-cotizaciones.html
├── generador-paletas-corporativas.html
├── generador-politicas-devolucion.html
├── generador-politicas-terminos.html
├── guiones-manejo-objeciones.html
├── organizador-matriz-contenidos.html
├── simulador-tco-fisico-nube.html
├── css/
│   ├── index.css
│   └── *.css
├── js/
│   ├── index.js
│   └── *.js
└── assets/
    └── favicon.png
```

La carpeta `apps/` corresponde al historial de desarrollo y no debe convertirse en un segundo nivel de publicación. Tampoco deben utilizarse las rutas antiguas `/apps/...` ni `/html/...`. Las URLs públicas correctas tienen esta forma:

```text
https://DOMINIO/auditor-seo-basico.html
https://DOMINIO/analizador-titulares.html
```

En GitHub Pages del repositorio actual, el prefijo del proyecto forma parte de la URL:

```text
https://juanxaviercasa.github.io/apps-pymes/auditor-seo-basico.html
```

## 3. Instalación en un hosting mediante ZIP o administrador de archivos

Descarga o copia los archivos de la raíz del repositorio. No subas solamente la carpeta `apps/`, una carpeta `html/` antigua ni el directorio que contiene al proyecto completo como una carpeta adicional.

Si el hosting utiliza cPanel, el contenido debe quedar directamente en `public_html`:

```text
public_html/index.html
public_html/auditor-seo-basico.html
public_html/css/auditor-seo-basico.css
public_html/js/auditor-seo-basico.js
public_html/assets/favicon.png
```

La instalación incorrecta crea una carpeta adicional y produce una URL como esta:

```text
public_html/apps-pymes/index.html
```

En ese caso, el sitio real queda en `/apps-pymes/`, mientras que el dominio busca `/index.html`; el resultado habitual es un 404. Si se sube un ZIP, ábrelo y comprueba que al entrar en la carpeta pública se vea `index.html` inmediatamente, no otra carpeta intermedia.

Después de copiar los archivos, conserva exactamente las mayúsculas, minúsculas, guiones y extensiones. En servidores Linux, `Auditor-SEO-Basico.html` y `auditor-seo-basico.html` son nombres diferentes.

## 4. Publicación recomendada en GitHub Pages

La configuración recomendada para este repositorio es publicar mediante **GitHub Actions**, usando la rama `main` y cargando la raíz completa del repositorio. GitHub Pages permite publicar desde una rama y la raíz o `/docs`; cuando se necesita un flujo más controlado, GitHub recomienda un workflow personalizado de Pages [1].

En **Settings → Pages**, selecciona:

| Campo | Valor correcto |
|---|---|
| Source | `GitHub Actions` |
| Rama de trabajo | `main` |
| Directorio que se publica | `.` — raíz del repositorio |
| Índice | `index.html` en la raíz |
| Workflow | `.github/workflows/static.yml` |

El workflow actual utiliza `actions/configure-pages`, `actions/upload-pages-artifact` y `actions/deploy-pages`. Estos componentes son el flujo oficial para empaquetar y desplegar un sitio estático mediante Pages [2]. No cambies el `path: "."` por `apps/`, `html/` u otra carpeta: hacerlo volvería a introducir la discrepancia de rutas.

Después de cada despliegue, revisa la ejecución en la pestaña **Actions**. El resultado debe ser `success` y el job debe completar los pasos **Checkout**, **Setup Pages**, **Upload static site root** y **Deploy to GitHub Pages**.

## 5. Configuración para Apache y cPanel

La configuración básica no necesita un framework. El servidor debe servir los archivos estáticos con sus tipos MIME correctos. Si se desean URLs sin `.html`, crea un archivo `.htaccess` en el mismo directorio que `index.html`:

```apache
Options -MultiViews
RewriteEngine On

# No reescribir archivos y carpetas que existen.
RewriteCond %{REQUEST_FILENAME} -f [OR]
RewriteCond %{REQUEST_FILENAME} -d
RewriteRule ^ - [L]

# Permitir /nombre-app como alias de /nombre-app.html.
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^(.+?)/?$ $1.html [L]
```

Esta regla no mueve ni renombra los archivos. Solo permite que una solicitud a `/auditor-seo-basico` encuentre `auditor-seo-basico.html`. La URL con `.html` continúa siendo válida y es la forma más portable entre hostings.

Si no tienes permiso para usar `.htaccess`, utiliza siempre las URLs con `.html`. No intentes resolver el problema mediante una redirección HTML automática: un `meta refresh` puede generar bucles, demora y una nueva ruta que el servidor tampoco sabe resolver [4].

## 6. Configuración para Nginx

En un servidor Nginx, define como raíz el directorio que contiene `index.html` y utiliza `try_files` para las URLs limpias:

```nginx
server {
    listen 80;
    server_name ejemplo.com;
    root /var/www/nubeparapymes;
    index index.html;

    location / {
        try_files $uri $uri.html $uri/ =404;
    }

    location ~* \.css$ {
        add_header Content-Type "text/css; charset=utf-8";
    }

    location ~* \.js$ {
        add_header Content-Type "text/javascript; charset=utf-8";
    }
}
```

Después de cambiar Nginx, valida la configuración con `nginx -t` y recarga el servicio. Si el hosting administrado no permite cambiar Nginx, usa las URLs con `.html` y no dependas de rutas limpias.

## 7. Codificación UTF-8 y tipos MIME

Todos los HTML, CSS y JavaScript deben conservarse como archivos UTF-8. Cada documento HTML debe declarar la codificación al principio del `<head>`:

```html
<meta charset="UTF-8">
```

La declaración debe estar dentro de los primeros 1024 bytes del documento; UTF-8 es la codificación válida para documentos HTML5 [4]. Evita guardar nuevamente los archivos desde un editor configurado en ANSI, Windows-1252 o Latin-1. Esa conversión produce títulos como `Auditor BÃ¡sico` y daña la ñ, los signos de apertura y otros caracteres.

El servidor debe entregar los tipos MIME adecuados. Los navegadores utilizan el encabezado `Content-Type` para decidir cómo procesar un recurso; un MIME incorrecto puede hacer que CSS sea ignorado o que JavaScript no se ejecute [3]. La tabla mínima es:

| Extensión | `Content-Type` recomendado |
|---|---|
| `.html` | `text/html; charset=utf-8` |
| `.css` | `text/css; charset=utf-8` |
| `.js` | `text/javascript; charset=utf-8` |
| `.json` | `application/json; charset=utf-8` |
| `.png` | `image/png` |
| `.jpg` / `.jpeg` | `image/jpeg` |
| `.svg` | `image/svg+xml` |

Si una solicitud a `js/auditor-seo-basico.js` devuelve el HTML de una página 404 con estado 200, el navegador no ejecutará el bundle y la aplicación puede mostrar solamente su fondo. Comprueba siempre la respuesta real del archivo, no solo el código HTTP.

## 8. Diagnóstico de una pantalla azul o aplicación vacía

Una pantalla azul no significa necesariamente que falte el HTML. En esta colección, el HTML puede cargar el fondo y el contenedor `#root`, mientras que el bundle JavaScript falla al montarse. Sigue este orden:

Primero abre directamente la aplicación con su nombre completo, por ejemplo `/auditor-seo-basico.html`, y después prueba la variante sin extensión si el hosting tiene la regla de reescritura configurada. En ambos casos, la respuesta del documento debe ser `200`.

Después abre las herramientas de desarrollador del navegador y revisa **Console** y **Network**. El HTML, su CSS y su JS deben responder correctamente, y el JS debe venir como JavaScript, no como HTML. En Console no debe aparecer `ReferenceError`, `SyntaxError`, `MIME type`, `Unexpected token` ni un error de módulo.

Usa estas comprobaciones desde una terminal:

```bash
BASE="https://tu-dominio.example"

curl -I "$BASE/"
curl -I "$BASE/auditor-seo-basico.html"
curl -I "$BASE/css/auditor-seo-basico.css"
curl -I "$BASE/js/auditor-seo-basico.js"
curl -I "$BASE/assets/favicon.png"
```

Para comprobar que un recurso JavaScript no está devolviendo una página 404 disfrazada de éxito:

```bash
curl -fsSL "$BASE/js/auditor-seo-basico.js" | head -c 120
```

La salida debe comenzar con código JavaScript minificado, no con `<!DOCTYPE html>`, `404`, `Not Found` o un documento de error del proveedor.

Si la consola muestra que una variable o tabla legítima del bundle está indefinida, no ocultes el error con CSS ni reemplaces la aplicación por una pantalla estática. Restaura la definición funcional, ejecuta `node --check js/nombre-app.js`, abre la aplicación localmente y solo después vuelve a desplegar.

## 9. Lista de comprobación antes de entregar el sitio

| Comprobación | Resultado esperado |
|---|---|
| `index.html` está en el directorio público | Sí |
| Las 22 páginas HTML están junto a `index.html` | Sí |
| Las carpetas `css/`, `js/` y `assets/` están junto a los HTML | Sí |
| Las referencias HTML comienzan por `./css/`, `./js/` o `./assets/` | Sí |
| El índice enlaza a `./nombre-app.html` | Sí |
| La rama publicada es `main` | Sí |
| GitHub Actions terminó en `success` | Sí |
| Cada HTML responde con `200` | Sí |
| Cada CSS responde con `Content-Type: text/css` | Sí |
| Cada JS responde con `Content-Type: text/javascript` o equivalente válido | Sí |
| Los títulos muestran tildes y ñ correctamente | Sí |
| La consola no muestra errores de ejecución | Sí |
| Una recarga directa conserva la aplicación | Sí |
| No se utilizan `/apps/...` ni `/html/...` | Sí |

## 10. Procedimiento de actualización futura

Para publicar una modificación, trabaja sobre `main`, modifica los archivos de la raíz o los recursos de `css/`, `js/` y `assets/`, ejecuta los validadores del proyecto y revisa `git diff --check`. No copies manualmente una aplicación a una carpeta nueva ni cambies la ubicación del HTML sin actualizar sus tres referencias principales: hoja CSS, bundle JS y favicon/assets.

El flujo mínimo recomendado es:

```bash
git checkout main
git pull --ff-only origin main

python3 scripts/validar_estructura_publica.py
python3 scripts/validacion_global.py

node --check js/nombre-app.js
git diff --check

git add -A
git commit -m "fix: describir el cambio realizado"
git push origin main
```

Después del `push`, espera a que el workflow de Pages termine correctamente y prueba una URL nueva en una ventana privada o con `Ctrl + F5`. Los navegadores y algunas redes pueden conservar HTML, CSS o JavaScript anteriores en caché.

## Referencias

[1]: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site "GitHub Docs — Configuring a publishing source for your GitHub Pages site"

[2]: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages "GitHub Docs — Using custom workflows with GitHub Pages"

[3]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types "MDN — Media types (MIME types)"

[4]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta "MDN — <meta> HTML metadata element"
