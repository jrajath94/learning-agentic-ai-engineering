"""Convert editable study notes into chapters with an installed Pandoc."""
from html import escape
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    pandoc = shutil.which('pandoc')
    if pandoc is None:
        raise SystemExit('Pandoc is required only to edit study Markdown. The supplied HTML works offline.')
    pages = []
    for path in sorted((ROOT / 'studies').glob('*.md')):
        lines = path.read_text().splitlines()
        if not lines or not lines[0].startswith('# '):
            continue
        title = lines[0][2:].strip()
        slug = 'study-' + path.stem
        result = subprocess.run(
            [pandoc, '-f', 'gfm', '-t', 'html5', '--no-highlight'],
            input='\n'.join(lines[1:]), capture_output=True, text=True, check=True,
        )
        introduction = ('<p><a href="resource-study.html">Back to implementation studies</a> · '
                        f'<a href="studies/{escape(path.name)}" download>Download the editable study</a></p>')
        rendered = re.sub(r'<h2 id="worked-answers">Worked answers</h2>(.*)$',
                          r'<details><summary>Show worked answers</summary>\1</details>',
                          result.stdout, flags=re.S)
        rendered = rendered.replace('href="../', 'href="')
        content = introduction + rendered
        # Keep all generated IDs and filenames within the local chapter.
        content = re.sub(r'href="([a-z0-9-]+)\.md"', r'href="study-\1.html"', content)
        (ROOT / 'fragments' / (slug + '.html')).write_text(content)
        pages.append([slug, path.stem.replace('-', ' ').capitalize(), title, 'Source studies', ''])
    (ROOT / 'data/study-pages.json').write_text(json.dumps(pages, indent=2) + '\n')
    print(f'{len(pages)} study chapters prepared. Run scripts/build.py next.')


if __name__ == '__main__':
    main()
