# ANI Interpretation Guide

Average Nucleotide Identity (ANI) summarizes nucleotide identity across homologous regions shared by two genomes. It is a powerful species-level genomic measure for bacteria and archaea, but it should not be interpreted as a single universal cutoff detached from genome overlap, reference context, and genome quality.

## A better way to read ANI

Use ANI together with at least four questions:

1. **How much of the genomes aligned?**
2. **Are both assemblies of sufficient quality?**
3. **Which reference or representative genome defines the species comparison?**
4. **Do taxonomy and phylogenomic context agree with the ANI result?**

## The common 95% reference point

ANI near 95% is widely used as a practical species-level reference value in prokaryotic genomics. Treat it as a useful reference point rather than a universal biological law.

A simple evidence vocabulary is:

| ANI context | Suggested wording |
|---|---|
| clearly above the applicable species radius | ANI supports close species-level genomic relatedness |
| close to the applicable radius | boundary case; inspect alignment fraction and reference context |
| below the common species range | ANI provides evidence against membership in the same conventional species cluster |
| FastANI not reported | unresolved by FastANI; preserve as missing |

Avoid statements such as `ANI < 95 therefore different species` when the lineage, alignment fraction, genome quality, and relevant species radius have not been examined.

## Alignment fraction

FastANI reports the number of mapped query fragments and the total number of query fragments. SpeciesResolve calculates:

```text
alignment_fraction = mapped_fragments / total_query_fragments
```

A high ANI value over limited genome overlap should be reviewed carefully. ANI and alignment fraction answer different questions and should be retained together.

GTDB currently uses both ANI and alignment fraction when assigning genomes to species clusters. The usual GTDB species radius is 95% ANI, with some representative-specific radii reaching 97% in order to preserve named species clusters. Current GTDB species assignment uses a minimum alignment-fraction criterion of 0.5.

## Directionality

FastANI can report query-to-reference and reference-to-query comparisons separately. Because fragmentation and query coverage can make these values slightly asymmetric, SpeciesResolve preserves the directional results and also summarizes each unordered pair using mean/minimum/maximum ANI plus alignment-fraction statistics.

Do not silently keep only the higher reciprocal value.

## Missing FastANI output

FastANI documents that genome pairs much below roughly 80% ANI may not receive an ANI estimate. A missing result is therefore not equivalent to 0%, 70%, 79%, or any other invented value.

If a pair is too divergent for FastANI, use a method appropriate to deeper evolutionary distances instead of forcing an ANI number.

## ANI and dDDH

ANI and digital DNA-DNA hybridization (dDDH) are related but distinct genome-based measures. ANI around 95-96% is often broadly associated with the historical 70% DDH species criterion, but exact correspondence varies.

For formal taxonomic descriptions or especially difficult boundary cases, dDDH and nomenclatural/type-strain evidence may be appropriate additions.

## What ANI cannot prove by itself

ANI alone does not establish:

- ecological equivalence;
- phenotype;
- adaptation;
- pathogenicity;
- nomenclatural validity;
- absence of contamination;
- a universal species boundary for every lineage.

Use ANI as one strong genomic evidence layer inside a broader species hypothesis.
