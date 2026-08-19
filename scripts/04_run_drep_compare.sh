#!/usr/bin/env bash
set -euo pipefail

GENOME_DIR="${1:-toy_genomes}"
OUT_DIR="${2:-example_outputs/drep/drep_compare}"
THREADS="${3:-4}"
PRIMARY_ANI="${4:-0.90}"
SECONDARY_ANI="${5:-0.95}"

if ! command -v dRep >/dev/null 2>&1; then
  echo "ERROR: dRep is not available in PATH." >&2
  exit 1
fi

shopt -s nullglob
GENOMES=("$GENOME_DIR"/*.fna)
if [ "${#GENOMES[@]}" -lt 2 ]; then
  echo "ERROR: need at least two .fna genomes in $GENOME_DIR" >&2
  exit 2
fi

mkdir -p "$(dirname "$OUT_DIR")"

dRep compare "$OUT_DIR" \
  -g "${GENOMES[@]}" \
  -p "$THREADS" \
  -pa "$PRIMARY_ANI" \
  -sa "$SECONDARY_ANI"

echo "dRep comparison output: $OUT_DIR"
echo "Primary ANI setting: $PRIMARY_ANI"
echo "Secondary ANI setting: $SECONDARY_ANI"
echo "These are clustering parameters, not independent species evidence."
