from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def historical(path):
    return subprocess.check_output(["git", "show", f"939dfee:{path}"], cwd=ROOT, text=True)


def extract(text, marker):
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"No se encontró {marker}")
    brace = text.find("{", start)
    depth = 0
    quote = None
    escaped = False
    for pos in range(brace, len(text)):
        ch = text[pos]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
        else:
            if ch in "'\"`":
                quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:pos + 1]
    raise RuntimeError(f"Llaves sin cerrar para {marker}")


def insert_before_mount(current, component):
    marker = "(0,v.createRoot)(document.getElementById(\"root\"))"
    if marker not in current:
        marker = "(0,F.createRoot)(document.getElementById(\"root\"))"
    if marker not in current:
        raise RuntimeError("No se encontró el punto de montaje React")
    return current.replace(marker, component + marker, 1)


# QR: recuperar el generador local y retirar únicamente la compuerta EmailGate y la ruta administrativa.
qr_path = ROOT / "js/generador-codigos-qr.js"
qr = qr_path.read_text(encoding="utf-8")
qr = qr.replace('path:"/",element:(0,F.jsx)(Fi,{"data-visual-edit-loc":"src/App.tsx:12:38"', 'path:"/ayuda",element:(0,F.jsx)(Ti,{"data-visual-edit-loc":"src/App.tsx:12:38"', 1)
if "function Ti(){" not in qr:
    component = extract(historical("generador-codigos-qr/assets/index.js"), "function Ti(){")
    component = component.replace("to:`/admin`", "to:`#`")
    component = re.sub(
        r"\(0,F\.jsx\)\(vi,\{open:y,lead:\{dial:n,phone:i,fullNumber:w,message:o,link:C\},onClose:\(\)=>b\(!1\),onConfirmed:k,\"data-visual-edit-loc\":`src/pages/Index\.tsx:229:6`,\"data-visual-edit-component\":`EmailGate`,\"data-visual-edit-editable\":`false`\}\)",
        "null",
        component,
        count=1,
    )
    if "EmailGate" in component or "/admin" in component:
        raise RuntimeError("La función QR aún contiene residuos prohibidos")
    qr_path.write_text(insert_before_mount(qr, component), encoding="utf-8")

# Consola: recuperar la consola local y retirar el modal de captación.
console_path = ROOT / "js/consola-campanas.js"
console = console_path.read_text(encoding="utf-8")
if "function Vi(){" not in console:
    component = extract(historical("consola-campanas/assets/index.js"), "function Vi(){")
    component = re.sub(
        r'f&&\(0,N\.jsx\)\(Bi,\{.*?"data-visual-edit-component":`LeadModal`,"data-visual-edit-editable":`false`\}\)',
        "null",
        component,
        count=1,
        flags=re.S,
    )
    if "LeadModal" in component or "EmailGate" in component:
        raise RuntimeError("La función Consola aún contiene residuos prohibidos")
    console_path.write_text(insert_before_mount(console, component), encoding="utf-8")

# Flete: recuperar únicamente el panel de historial, que no depende de red ni captación.
flete_path = ROOT / "js/calculadora-flete-envio-local.js"
flete = flete_path.read_text(encoding="utf-8")
if "Ir=({items:" not in flete:
    source = historical("calculadora-flete-envio-local/assets/index.js")
    start = source.find("Ir=({items:")
    end = source.find(",Qr=()", start)
    if start < 0 or end < 0:
        raise RuntimeError("No se encontró completo el panel de historial")
    component = source[start:end]
    if any(word in component for word in ["EmailGate", "LeadModal", "webhook", "script.google", "mailto"]):
        raise RuntimeError("El panel de historial contiene residuos prohibidos")
    flete_path.write_text(flete.replace("var Yr=[", component + ";var Yr=[", 1), encoding="utf-8")

# Paletas: el bundle vanilla estable ya incluye su propio panel local.
palette_path = ROOT / "js/generador-paletas-corporativas.js"
palette = palette_path.read_text(encoding="utf-8")
if "np-palette-app" not in palette and 'var vp={normal:' not in palette:
    palette = palette.replace(
        "function kp(",
        'var vp={normal:"visión normal",deuteranopia:"deuteranopía",protanopia:"protanopía",tritanopia:"tritanopía"};function kp(',
        1,
    )
    palette_path.write_text(palette, encoding="utf-8")

# Guiones: la limpieza eliminó una coma entre dos elementos de Routes y dejó referencias a PocketBase.
guiones_path = ROOT / "js/guiones-manejo-objeciones.js"
guiones = guiones_path.read_text(encoding="utf-8")
local_si = 'var si={collection:function(e){return{getFullList:async function(){try{let e=JSON.parse(localStorage.getItem("np_objeciones_comunidad_v1")||"[]");return Array.isArray(e)?e:[]}catch{return[]}},create:async function(t){let e=[];try{let n=JSON.parse(localStorage.getItem("np_objeciones_comunidad_v1")||"[]");e=Array.isArray(n)?n:[]}catch{}let n={...t,id:`local-${Date.now()}-${Math.random().toString(36).slice(2,8)}`,created:Date.now()};return e.push(n),localStorage.setItem("np_objeciones_comunidad_v1",JSON.stringify(e)),n}}}};'
if "np_objeciones_comunidad_v1" not in guiones:
    guiones = guiones.replace("function Mi(){", local_si + "function Mi(){", 1)
old = '"data-visual-edit-component":"Route","data-visual-edit-editable":"false"})(0,N.jsx)'
new = '"data-visual-edit-component":"Route","data-visual-edit-editable":"false"}),(0,N.jsx)'
if old in guiones:
    guiones = guiones.replace(old, new, 1)
    guiones_path.write_text(guiones, encoding="utf-8")

# QR: el bundle limpio conserva el historial local pero perdió el hook y dos componentes auxiliares.
qr = qr_path.read_text(encoding="utf-8")
if "np_qr_recent_v1" not in qr:
    qr_hook = 'var L=function(){var k=\'np_qr_recent_v1\',read=function(){try{var a=JSON.parse(localStorage.getItem(k)||\'[]\');return Array.isArray(a)?a:[]}catch(e){return[]}},write=function(a){try{localStorage.setItem(k,JSON.stringify(a.slice(0,30)))}catch(e){}};return{items:read(),add:function(e){var a=read().filter(function(t){return t.link!==e.link});a.unshift(Object.assign({id:\'qr-\'+Date.now()},e));write(a)},remove:function(e){write(read().filter(function(t){return t.id!==e}))},clear:function(){write([])}}};'
    qr = qr.replace("var L=function(){return null};", qr_hook, 1)
if "var bi=function(){return null};" not in qr:
    qr = qr.replace("var wi=function(){return null};", "var bi=function(){return null};var wi=function(){return null};", 1)
if "var wi=function(){return null};" not in qr:
    qr = qr.replace("var bi=function(){return null};", "var bi=function(){return null};var wi=function(){return null};", 1)
if "var si={collection:function()" not in qr:
    qr = qr.replace("function Ti(){", "var si={collection:function(){return{create:function(e){return Promise.resolve(e)},getFullList:function(){return Promise.resolve([])}}}};function Ti(){", 1)
qr_path.write_text(qr, encoding="utf-8")

# Guiones: conservar los adaptadores neutros de componentes visuales que ya no son necesarios.
guiones = guiones_path.read_text(encoding="utf-8")
if "var bi=function(){return null};" not in guiones and "function Mi(){" in guiones:
    guiones = guiones.replace("function Mi(){", "var bi=function(){return null};var wi=function(){return null};var L=function(){return null};function Mi(){", 1)
elif "var bi=function(){return null};" not in guiones and "var L=function(){return null};" in guiones:
    guiones = guiones.replace("var L=function(){return null};", "var bi=function(){return null};var wi=function(){return null};var L=function(){return null};", 1)
guiones_path.write_text(guiones, encoding="utf-8")

print("Bundles problemáticos curados sin captación ni servicios externos.")
