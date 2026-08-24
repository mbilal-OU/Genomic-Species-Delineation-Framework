# FastANI input checks

Before running an all-vs-all comparison, verify the genome list rather than assuming every path is usable.

```bash
# Build a deterministic list of assemblies.
find /path/to/genomes -type f -name '*.fna' | sort > genome_list.txt

# Confirm that the list is non-empty.
test -s genome_list.txt || { echo 'ERROR: genome_list.txt is empty' >&2; exit 1; }

# Report any paths that no longer exist or are not regular files.
while IFS= read -r genome; do
  [ -f "$genome" ] || printf 'Missing genome: %s\n' "$genome" >&2
done < genome_list.txt
```

FastANI reads paths from the query and reference list files. Moving assemblies after creating `genome_list.txt`, using the wrong filename extension in `find`, or generating an empty list can therefore cause a run to fail before any biological comparison is made.

For an all-vs-all analysis, use the same validated list for both `--ql` and `--rl`. Keep the list with the analysis outputs so the exact input set can be reconstructed later.
