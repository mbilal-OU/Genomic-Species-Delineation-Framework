#!/usr/bin/env bash
set -euo pipefail

# dRep dereplication workflow.
# This selects representative genomes from highly similar genome clusters.
# For real projects, use genome quality information and inspect parameters carefully.

mkdir -p example_outputs/drep

dRep dereplicate example_outputs/drep/drep_dereplicate \
  -g toy_genomes/*.fna \
  -p 4 \
  -sa 0.95

echo "dRep dereplication output folder:"
echo "  example_outputs/drep/drep_dereplicate"
