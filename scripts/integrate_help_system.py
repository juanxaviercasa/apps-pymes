from __future__ import annotations

import json
from pathlib import Path

from help_configs import CONFIGS

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- NUBEPYME_HELP_START -->"
END = "<!-- NUBEPYME_HELP_END -->"

for app_id, config in CONFIGS.items():
    path = ROOT / f"{app_id}.html"
    if not path.is_file():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    if START in text:
        before = text.split(START, 1)[0]
        after = text.split(END, 1)[1]
        text = before + after
    payload = {
        "id": app_id,
        "name": config["name"],
        "purpose": config["purpose"],
        "quick": config["quick"],
        "tip": config["tip"],
        "guide": f"./guia-uso-22-apps.html#{config['anchor']}",
        "steps": [
            {"title": title, "text": step_text, "selector": selector.split(",")}
            for selector, title, step_text in config["steps"]
        ],
    }
    block = (
        f"{START}\n"
        f"<link rel=\"stylesheet\" href=\"./css/ayuda-apps.css\">\n"
        f"<script>window.NP_HELP_CONFIG={json.dumps(payload, ensure_ascii=False, separators=(',', ':'))};</script>\n"
        f"<script defer src=\"./js/ayuda-apps.js\"></script>\n"
        f"{END}"
    )
    marker = "</head>"
    if marker not in text:
        raise ValueError(f"No se encontró </head> en {path.name}")
    text = text.replace(marker, block + "\n" + marker, 1)
    path.write_text(text, encoding="utf-8")

print(f"HELP_INTEGRATED={len(CONFIGS)}")
