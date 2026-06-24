#!/usr/bin/env bash
set -euo pipefail

# pyani example.
# pyani versions differ. Modern installs may provide 'pyani', while older installs
# provide 'average_nucleotide_identity.py'.
# Check your installed command using:
#   pyani --help
# or:
#   average_nucleotide_identity.py --help

mkdir -p example_outputs/pyani

# Older/classic pyani command style:
average_nucleotide_identity.py \
  -i toy_genomes \
  -o example_outputs/pyani \
  -m ANIb \
  -g \
  --workers 4

echo "pyani output folder:"
echo "  example_outputs/pyani"
