# FastANI input lists

FastANI query and reference lists should contain one genome file path per line. When building a list from a directory, restrict `find` to regular files so a directory whose name ends in `.fna` is not passed to FastANI accidentally.

```bash
find /path/to/genomes -type f -name '*.fna' | sort > genome_list.txt
```

Before running an all-vs-all comparison, verify the list and count the inputs:

```bash
sed -n '1,5p' genome_list.txt
wc -l genome_list.txt
```

The repository helper `scripts/01_make_fastani_lists.sh` applies the same `-type f` filter and requires at least two matching genomes before creating the query and reference lists.
