"""Render Mermaid sources for the offline edition with an installed Mermaid CLI."""
import argparse
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', default='mmdc')
    parser.add_argument('--puppeteer-config')
    parser.add_argument('--config')
    parser.add_argument('--only-workshops', action='store_true')
    args = parser.parse_args()
    cli = shutil.which(args.cli)
    if not cli:
        raise SystemExit('Install the Mermaid CLI to edit diagrams. The supplied SVG files work offline without it.')
    sources = sorted((ROOT / 'workshops' if args.only_workshops else ROOT).rglob('*.mmd'))
    for source in sources:
        output = source.with_suffix('.svg')
        command = [cli, '-i', str(source), '-o', str(output), '-b', '#000000', '-t', 'dark']
        if args.puppeteer_config:
            command += ['-p', args.puppeteer_config]
        if args.config:
            command += ['-c', args.config]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode:
            raise SystemExit(f'{source.relative_to(ROOT)} failed:\n{result.stderr}')
        rendered = output.read_text()
        if '<svg' not in rendered or 'Syntax error in text' in rendered:
            raise SystemExit(f'{source.relative_to(ROOT)} did not produce a valid diagram')
        print(source.relative_to(ROOT))


if __name__ == '__main__':
    main()
