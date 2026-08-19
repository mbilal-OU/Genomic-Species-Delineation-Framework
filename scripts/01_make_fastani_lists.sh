#!/usr/bin/env bash
set -euo pipefail

GENOME_DIR="${1:-toy_genomes}"
OUT_DIR="${2:-example_outputs/fastani}"
EXTENSION="${3:-fna}"

if [ ! -d "$GENOME_DIR" ]; then
  echo "ERROR: genome directory not found: $GENOME_DIR" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"
QUERY_LIST="$OUT_DIR/query_list.txt"
REFERENCE_LIST="$OUT_DIR/reference_list.txt"

find "$GENOME_DIR" -type f -name "*.${EXTENSION}" | sort > "$QUERY_LIST"
COUNT=$(wc -l < "$QUERY_LIST" | tr -d ' ')

if [ "$COUNT" -lt 2 ]; then
  echo "ERROR: need at least two *.${EXTENSION} genomes in $GENOME_DIR" >&2
  exit 2
fi

cp "$QUERY_LIST" "$REFERENCE_LIST"

echo "Genomes found: $COUNT"
echo "Query list: $QUERY_LIST"
echo "Reference list: $REFERENCE_LIST"
