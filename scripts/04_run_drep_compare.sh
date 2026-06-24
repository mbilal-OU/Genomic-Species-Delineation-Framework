#!/usr/bin/env bash
set -euo pipefail

# dRep comparison workflow.
# Useful when you have many genomes and want clustering/dereplication.
# Requires dRep installed and available in PATH.

mkdir -p example_outputs/drep

dRep compare example_outputs/drep/drep_compare \
  -g toy_genomes/*.fna \
  -p 4

echo "dRep output folder:"
echo "  example_outputs/drep/drep_compare"
