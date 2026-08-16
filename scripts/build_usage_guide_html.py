from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "GUIA_USO_22_APPS.md"
target = ROOT / "guia-uso-22-apps.html"

body = markdown.markdown(
    source.read_text(encoding="utf-8"),
    extensions=["tables", "fenced_code", "toc"],
    output_format="html5",
)

html = f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Guía completa de uso de las 22 herramientas gratuitas de NubeParaPymes.">
  <title>Guía de uso · NubeParaPymes</title>
  <style>
    :root {{ color-scheme: dark; --bg:#071426; --panel:#0d2037; --line:#28415c; --text:#edf4ff; --muted:#aabbd0; --accent:#ff7a18; --link:#7db8ff; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--text); font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; line-height:1.65; }}
    header {{ border-bottom:1px solid var(--line); background:#091a2e; }}
    .top {{ max-width:1160px; margin:auto; padding:18px 24px; display:flex; justify-content:space-between; gap:16px; align-items:center; }}
    .brand {{ color:var(--text); font-weight:800; text-decoration:none; letter-spacing:.01em; }}
    .back {{ color:var(--link); text-decoration:none; font-size:.95rem; }}
    main {{ max-width:1160px; margin:0 auto; padding:42px 24px 72px; }}
    article {{ background:rgba(13,32,55,.72); border:1px solid var(--line); border-radius:18px; padding:34px clamp(22px,5vw,64px); box-shadow:0 18px 60px rgba(0,0,0,.2); }}
    h1,h2,h3 {{ line-height:1.2; color:#fff; margin-top:1.65em; }}
    h1 {{ margin-top:0; font-size:clamp(2rem,4vw,3.2rem); }}
    h2 {{ border-bottom:1px solid var(--line); padding-bottom:.4em; font-size:clamp(1.45rem,2.4vw,2rem); }}
    h3 {{ color:#dceaff; font-size:1.2rem; }}
    p,li {{ color:var(--muted); }}
    strong {{ color:#fff; }}
    a {{ color:var(--link); }}
    blockquote {{ margin:1.5em 0; padding:1em 1.2em; border-left:4px solid var(--accent); background:rgba(255,122,24,.09); border-radius:0 10px 10px 0; }}
    blockquote p {{ margin:.1em 0; color:#e8eef7; }}
    code {{ padding:.15em .35em; border-radius:5px; background:#06101e; color:#ffd5af; }}
    pre {{ overflow:auto; padding:16px; border-radius:10px; background:#06101e; }}
    pre code {{ padding:0; }}
    table {{ width:100%; border-collapse:collapse; display:block; overflow-x:auto; margin:1.4em 0; }}
    th,td {{ text-align:left; vertical-align:top; padding:10px 12px; border:1px solid var(--line); min-width:120px; }}
    th {{ color:#fff; background:#132d4b; }}
    td {{ color:var(--muted); }}
    hr {{ border:0; border-top:1px solid var(--line); margin:2.4em 0; }}
    footer {{ max-width:1160px; margin:0 auto; padding:0 24px 36px; color:var(--muted); font-size:.9rem; }}
  </style>
</head>
<body>
  <header><div class="top"><a class="brand" href="./index.html">NubeParaPymes</a><a class="back" href="./index.html">Volver al directorio</a></div></header>
  <main><article>{body}</article></main>
  <footer>Guía de uso de las 22 aplicaciones · NubeParaPymes</footer>
</body>
</html>
'''

target.write_text(html, encoding="utf-8")
print(f"GENERATED {target.name} ({target.stat().st_size} bytes)")
