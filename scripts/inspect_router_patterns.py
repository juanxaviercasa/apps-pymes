from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
for path in sorted((ROOT / 'js').glob('*.js')):
    text = path.read_text(encoding='utf-8', errors='replace')
    print(f'--- {path.name} ---')
    for needle in ('BrowserRouter', 'basename', 'path:`/`', 'path:`*`', 'location.assign', 'window.location.reload'):
        positions = [m.start() for m in re.finditer(re.escape(needle), text)]
        if positions:
            print(needle, len(positions))
            for pos in positions[-3:]:
                start = max(0, pos - 260)
                end = min(len(text), pos + 520)
                print(text[start:end].replace('\n', ' ')[:800])
