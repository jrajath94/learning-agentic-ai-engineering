"""Replay the offline workshops and record the observed command results."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='A new output directory.')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    journal = []

    def run(label, cwd, arguments, expected_exit=0, contains=None):
        result = subprocess.run(
            [sys.executable, '-B', *map(str, arguments)], cwd=cwd,
            capture_output=True, text=True, timeout=120,
        )
        relative_arguments = [str(value).replace(str(output), '<OUTPUT>') for value in arguments]
        observed = result.stdout + result.stderr
        journal.append({
            'step': label, 'cwd': str(cwd.relative_to(ROOT)),
            'command': ['python3', '-B', *relative_arguments],
            'expected_exit': expected_exit, 'observed_exit': result.returncode,
            'stdout': result.stdout.replace(str(output), '<OUTPUT>'),
            'stderr': result.stderr.replace(str(output), '<OUTPUT>'),
        })
        (output / 'commands.json').write_text(json.dumps(journal, indent=2) + '\n')
        if result.returncode != expected_exit or (contains and contains not in observed):
            raise SystemExit(f'{label} failed its expected result. Inspect {output / "commands.json"}.')
        print(label + ': expected result observed')

    run('Original three labs', ROOT, ['labs/replay.py', output / 'original'])
    run('Engineering branch and review sequence', ROOT / 'workshops/engineering',
        ['verify.py', '--record', output / 'engineering.txt'],
        contains='Verified base, red tests, candidate, review counterexamples, and combined revision.')
    research = ROOT / 'workshops/research'
    run('Research regression tests', research, ['-m', 'unittest', 'discover', '-s', '.', '-v'], contains='OK')
    run('Disjoint evaluation split', research, ['run.py', 'audit'], contains='PASS')
    run('Leakage counterexample', research, ['run.py', 'audit', '--holdout-file', 'leaky-holdout.json'], expected_exit=1)
    run('Development interruption', research, ['run.py', 'dev', '--out', output / 'research', '--stop-after', '2'])
    run('Development resume', research, ['run.py', 'dev', '--out', output / 'research'])
    run('Held-out decision', research, ['run.py', 'holdout', '--out', output / 'research'], contains='retain baseline')
    run('Automation crash and retry sequence', ROOT / 'workshops/automation', ['record_demo.py', output / 'automation'])
    run('Operator briefing fixture', ROOT, ['studies/operator-fixture.py'], contains='Missing calendar was reported.')
    run('Tool list and preview fixture', ROOT, ['studies/social-tool-fixture.py'])
    records = {}
    for filename in ('research/checkpoint.json', 'research/holdout-report.json', 'automation/replay.json',
                     'automation/inspect.json', 'automation/draft.txt'):
        records[filename] = hashlib.sha256((output / filename).read_bytes()).hexdigest()
    (output / 'artifact-hashes.json').write_text(json.dumps(records, indent=2) + '\n')
    print(f'{len(journal)} workflow checks passed. Results are in {output.name}.')


if __name__ == '__main__':
    main()
