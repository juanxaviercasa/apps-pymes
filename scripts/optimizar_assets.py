from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_DIR = ROOT / 'css'
JS_DIR = ROOT / 'js'


def size(path: Path) -> int:
    return path.stat().st_size


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def optimize() -> None:
    css_files = sorted(CSS_DIR.glob('*.css'))
    js_files = sorted(JS_DIR.glob('*.js'))
    if len(css_files) != 25 or len(js_files) != 25:
        raise SystemExit(f'Se esperaban 25 CSS y 25 JS; encontrados {len(css_files)} CSS y {len(js_files)} JS.')

    before = {str(p.relative_to(ROOT)): size(p) for p in [*css_files, *js_files]}
    with tempfile.TemporaryDirectory(prefix='apps-pymes-assets-') as tmp:
        backup = Path(tmp)
        for path in [*css_files, *js_files]:
            target = backup / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

        for path in css_files:
            temp_out = backup / 'out' / path.name
            temp_out.parent.mkdir(parents=True, exist_ok=True)
            run(['pnpm', 'dlx', '--yes', 'clean-css-cli', '-O2', '-o', str(temp_out), str(path)])
            shutil.copy2(temp_out, path)

        for path in js_files:
            temp_out = backup / 'out' / path.name
            temp_out.parent.mkdir(parents=True, exist_ok=True)
            run([
                'pnpm', 'dlx', '--yes', 'terser', str(path),
                '--compress', 'passes=2,ecma=2020',
                '--mangle',
                '--format', 'comments=false',
                '--output', str(temp_out),
            ])
            shutil.copy2(temp_out, path)

    after = {str(p.relative_to(ROOT)): size(p) for p in [*css_files, *js_files]}
    report = {
        'before_bytes': sum(before.values()),
        'after_bytes': sum(after.values()),
        'saved_bytes': sum(before.values()) - sum(after.values()),
        'saved_percent': round((1 - sum(after.values()) / sum(before.values())) * 100, 2),
        'files': {
            name: {'before': before[name], 'after': after[name], 'saved': before[name] - after[name]}
            for name in before
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


def check() -> None:
    css_files = sorted(CSS_DIR.glob('*.css'))
    js_files = sorted(JS_DIR.glob('*.js'))
    for path in js_files:
        run(['node', '--check', str(path)])
    print(f'JS_SYNTAX_OK={len(js_files)}')
    print(f'CSS_FILES_OK={len(css_files)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['optimize', 'check'])
    args = parser.parse_args()
    if args.command == 'optimize':
        optimize()
    else:
        check()
