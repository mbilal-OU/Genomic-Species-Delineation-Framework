# Software Roles in SpeciesResolve

SpeciesResolve uses several tools, but they do not represent independent votes of equal weight. Each tool answers a different computational question.

| Tool | Main role | What it contributes | What it should not be called |
|---|---|---|---|
| FastANI | scalable pairwise ANI screening | ANI plus mapped/total fragments for alignment-fraction context | a universal species oracle |
| pyANI-plus | optional alternative ANI methods | ANIb, ANIm, dnadiff, FastANI and related method comparisons | automatically more accurate than FastANI |
| dRep | genome clustering and representative selection | operational dereplication under explicit similarity settings | independent confirmation of species identity |
| GTDB-Tk | reference taxonomy and phylogenomic placement | ANI screening against GTDB representatives plus marker-gene placement/classification | a substitute for inspecting ANI, AF, quality, and reference relationships |

## FastANI

Use FastANI for efficient pairwise or all-vs-all comparisons among sufficiently related genomes.

Important outputs include:

```text
ANI
mapped fragments
total query fragments
alignment fraction
```

FastANI can leave divergent comparisons unreported. SpeciesResolve preserves those as missing.

## pyANI-plus

The original `pyani` project is deprecated upstream. SpeciesResolve therefore points new analyses to **pyANI-plus**.

Use pyANI-plus when you want to compare selected genomes with alternative ANI algorithms or inspect method sensitivity. For example, ANIb and ANIm use different alignment strategies and can be informative in a near-boundary case.

Method agreement is useful, but two ANI implementations do not become two independent biological criteria.

## dRep

dRep is useful when many genomes must be clustered and representative genomes selected. Its primary and secondary ANI thresholds are analysis parameters, so changing them can change the clusters.

Use dRep to answer operational questions such as:

```text
Which genomes group under this clustering rule?
Which representative should be retained from each cluster?
```

Do not write:

```text
dRep independently proved that these are one species.
```

## GTDB-Tk

GTDB-Tk provides a standardized bacterial and archaeal taxonomic context. Current workflows combine an ANI screen against GTDB representative genomes with marker-gene based phylogenetic placement for genomes that require placement.

Species assignment depends on the GTDB reference release, representative genome, applicable ANI radius, and alignment fraction. Record the GTDB-Tk version and database release in reproducible analyses.

## Genome quality tools

SpeciesResolve does not prescribe a single completeness/contamination program. CheckM2 or another justified quality method can be used before species interpretation.

The key requirement is to retain the quality evidence and not interpret poor assemblies as if they were complete, uncontaminated genomes.
