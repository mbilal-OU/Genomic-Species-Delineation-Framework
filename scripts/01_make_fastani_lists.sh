#!/usr/bin/env bash
set -euo pipefail

# Create query and reference lists for all-vs-all FastANI screening.
# Run from the repository root.

mkdir -p example_outputs/fastani
find toy_genomes -name "*.fna" | sort > example_outputs/fastani/query_list.txt
cp example_outputs/fastani/query_list.txt example_outputs/fastani/reference_list.txt

echo "Created:"
echo "  example_outputs/fastani/query_list.txt"
echo "  example_outputs/fastani/reference_list.txt"
