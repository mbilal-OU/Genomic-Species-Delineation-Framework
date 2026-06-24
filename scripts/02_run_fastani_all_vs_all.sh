#!/usr/bin/env bash
set -euo pipefail

# FastANI all-vs-all example.
# Requires fastANI installed and available in PATH.
# Run from the repository root.

mkdir -p example_outputs/fastani

fastANI \
  --ql example_outputs/fastani/query_list.txt \
  --rl example_outputs/fastani/reference_list.txt \
  -o example_outputs/fastani/fastani_all_vs_all.tsv \
  -t 4

echo "FastANI output:"
echo "  example_outputs/fastani/fastani_all_vs_all.tsv"
