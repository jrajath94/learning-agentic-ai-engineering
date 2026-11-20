#!/bin/sh
# Local red-then-green demo. No model. Shows the loop the TDD skill describes.
set -eu
DEMO=$(mktemp -d)
trap 'rm -rf "$DEMO"' EXIT
cat > "$DEMO/counter.py" << 'PY'
def inc(n):
    return n
PY
cat > "$DEMO/test_counter.py" << 'PY'
from counter import inc

assert inc(1) == 2, "inc(1) should be 2"
print("ok")
PY
echo '$ python3 test_counter.py'
set +e
(cd "$DEMO" && python3 test_counter.py)
red=$?
set -e
echo "exit $red"
cat > "$DEMO/counter.py" << 'PY'
def inc(n):
    return n + 1
PY
echo '$ python3 test_counter.py'
(cd "$DEMO" && python3 test_counter.py)
echo "exit $?"
echo '--- counter.py after the green run ---'
cat "$DEMO/counter.py"
