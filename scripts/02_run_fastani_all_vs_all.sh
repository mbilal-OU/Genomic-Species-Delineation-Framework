#!/usr/bin/env bash
set -euo pipefail

QUERY_LIST="${1:-example_outputs/fastani/query_list.txt}"
REFERENCE_LIST="${2:-example_outputs/fastani/reference_list.txt}"
OUT_FILE="${3:-example_outputs/fastani/fastani_all_vs_all.tsv}"
THREADS="${4:-4}"

if ! command -v fastANI >/dev/null 2>&1; then
  echo "ERROR: fastANI is not available in PATH." >&2
  exit 1
fi

for file in "$QUERY_LIST" "$REFERENCE_LIST"; do
  if [ ! -s "$file" ]; then
    echo "ERROR: list file is missing or empty: $file" >&2
    exit 2
  fi
done

mkdir -p "$(dirname "$OUT_FILE")"

fastANI \
  --ql "$QUERY_LIST" \
  --rl "$REFERENCE_LIST" \
  -o "$OUT_FILE" \
  -t "$THREADS"

echo "FastANI output: $OUT_FILE"
echo "Parse with: python scripts/08_parse_fastani_and_plot.py --input $OUT_FILE"
