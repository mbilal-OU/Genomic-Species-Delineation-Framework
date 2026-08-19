#!/usr/bin/env bash
set -euo pipefail

cat >&2 <<'EOF'
NOTE: upstream pyani is deprecated. SpeciesResolve now uses pyANI-plus.
This compatibility script forwards to scripts/03_run_pyani_plus.sh.
EOF

exec bash scripts/03_run_pyani_plus.sh "$@"
