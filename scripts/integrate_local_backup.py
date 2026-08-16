from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "generador-cotizaciones": {
        "label": "Generador de cotizaciones",
        "keys": ["qg_clients", "qg_catalog", "qg_history", "qg_theme", "qg_counter"],
    },
    "creador-facturas-proforma": {
        "label": "Creador de facturas proforma",
        "keys": ["pf_clients_v1", "pf_products_v1", "pf_history_v1"],
    },
    "comparador-campanas-avanzado": {
        "label": "Comparador de campañas avanzado",
        "keys": ["campaigns", "scenarios", "theme"],
    },
    "consola-campanas": {
        "label": "Consola de campañas",
        "keys": ["utm_campaigns"],
    },
    "organizador-matriz-contenidos": {
        "label": "Organizador de matriz de contenidos",
        "keys": ["matriz-contenidos-v2"],
    },
}


def integrate(name: str, config: dict) -> None:
    html_path = ROOT / f"{name}.html"
    text = html_path.read_text(encoding="utf-8")
    css_ref = '<link rel="stylesheet" href="./css/respaldo-local.css">'
    if css_ref not in text:
        text = text.replace("</head>", f"{css_ref}\n</head>", 1)

    marker = '<script src="./js/respaldo-local.js"></script>'
    if marker not in text:
        payload = json.dumps(
            {"appId": name, "label": config["label"], "storageKeys": config["keys"]},
            ensure_ascii=False,
            separators=(",", ":"),
        )
        injection = (
            f'<script>window.NP_BACKUP_CONFIG={payload};</script>\n'
            f"{marker}\n"
        )
        text = text.replace("</body>", f"{injection}</body>", 1)
    html_path.write_text(text, encoding="utf-8")


for app_name, app_config in TARGETS.items():
    integrate(app_name, app_config)
print(f"Integradas {len(TARGETS)} aplicaciones con respaldo JSON local.")
