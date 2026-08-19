# Synthetic toy genomes

The FASTA files in this directory are **synthetic teaching and software-test genomes**.

They were designed to span several approximate similarity regimes so the repository can demonstrate FastANI behavior without downloading biological data.

The filenames are descriptive labels for the simulation design:

```text
A_reference.fna
B_same_species_98ANI.fna
C_boundary_95ANI.fna
D_related_below_species_92ANI.fna
E_distant_85ANI.fna
```

These labels are not taxonomic assignments, and the files should not be cited as biological examples of real species boundaries.

Use them to test:

- FastANI input-list generation;
- pairwise ANI parsing;
- reciprocal summaries;
- alignment-fraction calculation;
- preservation of missing comparisons;
- plotting and CI behavior.

For biological conclusions, replace these files with quality-assessed real genomes and record the reference/type context, software versions, and database releases used in the analysis.
