#!/usr/bin/env bash
set -euo pipefail

# GTDB-Tk classification example.
# GTDB-Tk performs taxonomic placement and also uses ANI-related logic for species assignment.
# Requires GTDB-Tk database configured in your environment.

mkdir -p example_outputs/gtdbtk

gtdbtk classify_wf \
  --genome_dir toy_genomes \
  --out_dir example_outputs/gtdbtk/gtdbtk_classify \
  --extension fna \
  --cpus 4

echo "GTDB-Tk output folder:"
echo "  example_outputs/gtdbtk/gtdbtk_classify"
