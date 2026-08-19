#!/usr/bin/env bash
set -euo pipefail

INPUT_DIR="${1:-toy_genomes}"
OUT_DIR="${2:-example_outputs/pyani_plus}"
METHOD="${3:-anib}"

mkdir -p "$OUT_DIR"
DB="$OUT_DIR/speciesresolve_pyani_plus.sqlite"
EXPORT_DIR="$OUT_DIR/export"

if ! command -v pyani-plus >/dev/null 2>&1; then
  echo "ERROR: pyani-plus is not available in PATH." >&2
  echo "Install it with: conda install -c bioconda -c conda-forge pyani-plus" >&2
  exit 1
fi

case "$METHOD" in
  anib|anim|dnadiff|fastani)
    ;;
  *)
    echo "ERROR: supported methods are anib, anim, dnadiff, or fastani" >&2
    exit 2
    ;;
esac

rm -f "$DB"
rm -rf "$EXPORT_DIR"

pyani-plus "$METHOD" "$INPUT_DIR" \
  --database "$DB" \
  --create-db \
  --name "SpeciesResolve $METHOD comparison"

mkdir -p "$EXPORT_DIR"
pyani-plus export-run \
  --database "$DB" \
  --outdir "$EXPORT_DIR"

echo "pyANI-plus database: $DB"
echo "Exported results: $EXPORT_DIR"
