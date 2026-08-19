# SpeciesResolve Evidence Model

SpeciesResolve treats microbial species delineation as a hypothesis evaluated with multiple, partly dependent genomic evidence layers.

The goal is not to add up a fixed number of votes. The goal is to understand which observations are concordant, which are methodologically related, and which conflicts need investigation.

## 1. Genome quality gate

Before pairwise species interpretation, ask whether each assembly is suitable for comparison.

Useful fields include:

```text
completeness
contamination
assembly size
contig count
N50 or another continuity measure
```

A fragmented or contaminated assembly can reduce apparent genome overlap, alter genome size, disturb taxonomic placement, and introduce misleading sequence content.

Quality evidence comes first because later metrics assume the input genomes are meaningful representations of the organisms being compared.

## 2. ANI and alignment fraction

ANI asks:

```text
How similar are the homologous nucleotide regions that could be compared?
```

Alignment fraction asks:

```text
How much of the genome participated in that comparison?
```

These quantities should be retained together.

A high ANI over extensive overlap is a different evidence pattern from high ANI over limited overlap.

## 3. Reference and type context

Species assignment is relative to a taxonomic framework and, for named taxa, ideally to appropriate type-derived or accepted representative material.

Questions to record include:

```text
Which representative genome was used?
Is it type-derived or otherwise authoritative for the comparison?
Which database release supplied the assignment?
What ANI radius applies to that representative?
```

This is especially important for near-boundary or nomenclaturally complex groups.

## 4. GTDB taxonomic context

GTDB-Tk supplies standardized bacterial and archaeal taxonomic context using GTDB representatives, ANI screening, marker genes, and phylogenetic placement.

A concordant GTDB assignment can strengthen interpretation, but it is not independent of ANI because GTDB species assignment itself uses ANI and alignment-fraction criteria.

For reproducibility, retain:

```text
GTDB-Tk version
GTDB release
summary TSV
closest representative
ANI / AF fields when reported
classification method or note
```

## 5. dRep clustering

dRep is useful for clustering many genomes and choosing representatives under explicit similarity settings.

It is an operational layer, not an independent species criterion.

When reporting dRep, record at least:

```text
primary ANI threshold
secondary ANI threshold
secondary comparison algorithm
coverage setting when used
genome-quality settings
representative-selection settings
```

## 6. Alternative ANI methods

pyANI-plus can run multiple ANI-related algorithms. Comparing methods can reveal sensitivity to alignment strategy, fragmentation, and algorithmic details.

This is a methodological robustness check.

Do not count FastANI and ANIb as two independent biological votes simply because two programs produced similar numbers.

## 7. Phylogenomic context

Phylogenomic placement or a core/marker-gene tree can help determine whether a proposed species group is compatible with broader evolutionary relationships.

Tree evidence is especially useful when:

- ANI is near a species radius;
- GTDB and existing labels disagree;
- multiple close named species occur in the same lineage;
- a genome appears as an outlier;
- the reference relationship is uncertain.

Phylogenomics and ANI answer different questions, so disagreement should be investigated rather than averaged away.

## Interpretation states

### Concordant support

Use when the available quality, ANI/AF, reference, taxonomy, and phylogenomic context are mutually compatible.

### Discordant evidence

Use when important evidence layers point in different directions.

Examples:

```text
high ANI but low genome overlap
high ANI but conflicting GTDB species assignment
one genome has poor quality or unexpected genome size
dRep grouping changes under modest parameter changes
phylogenomic placement conflicts with the assumed label
```

### Unresolved

Use when the data do not support a defensible conclusion.

Examples:

```text
FastANI does not report the pair
one genome is too incomplete or contaminated
only a distant reference is available
ANI is near the applicable radius and other evidence is missing
```

Leaving a case unresolved is scientifically preferable to manufacturing certainty.

## Formal taxonomy is a separate step

SpeciesResolve supports genomic species hypotheses. It does not itself perform a formal nomenclatural act.

Formal descriptions can require additional evidence, type material, nomenclatural checks, and accepted taxonomic procedures. Depending on the project, dDDH and other evidence may also be appropriate.
