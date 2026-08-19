#!/usr/bin/env bash
set -euo pipefail

GENOME_DIR="${1:-toy_genomes}"
OUT_DIR="${2:-example_outputs/gtdbtk/gtdbtk_classify}"
CPUS="${3:-4}"
EXTENSION="${4:-fna}"

if ! command -v gtdbtk >/dev/null 2>&1; then
  echo "ERROR: gtdbtk is not available in PATH." >&2
  echo "Install GTDB-Tk separately and configure its reference database first." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT_DIR")"

gtdbtk classify_wf \
  --genome_dir "$GENOME_DIR" \
  --out_dir "$OUT_DIR" \
  --extension "$EXTENSION" \
  --cpus "$CPUS"

echo "GTDB-Tk output: $OUT_DIR"
echo "Record the GTDB-Tk version and GTDB reference release with your analysis."
