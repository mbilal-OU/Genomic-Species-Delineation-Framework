#!/usr/bin/env bash
set -euo pipefail

GENOME_DIR="${1:-toy_genomes}"
OUT_DIR="${2:-example_outputs/drep/drep_dereplicate}"
THREADS="${3:-4}"
SECONDARY_ANI="${4:-0.95}"

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

dRep dereplicate "$OUT_DIR" \
  -g "${GENOMES[@]}" \
  -p "$THREADS" \
  -sa "$SECONDARY_ANI"

echo "dRep dereplication output: $OUT_DIR"
echo "Secondary ANI setting: $SECONDARY_ANI"
echo "For real data, provide and inspect genome-quality evidence before choosing representatives."
