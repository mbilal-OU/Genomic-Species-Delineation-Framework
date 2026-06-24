# Genomic Species Delineation Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20WSL2%20%7C%20HPC-blue)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![CI](https://github.com/mbilal-OU/Genomic-Species-Delineation-Framework/actions/workflows/ci.yml/badge.svg)](https://github.com/mbilal-OU/Genomic-Species-Delineation-Framework/actions)

> A reproducible framework for microbial species delineation using ANI,
> genome quality assessment, dereplication, taxonomy, and phylogenomic evidence.

---

## Table of Contents

- [What This Does](#what-this-does)
- [Background](#background)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Step-by-Step Guide](#step-by-step-guide)
  - [Step 1 - Prepare genome list](#step-1---prepare-genome-list)
  - [Step 2 - Run FastANI](#step-2---run-fastani)
  - [Step 3 - Visualize ANI results](#step-3---visualize-ani-results)
  - [Step 4 - Run pyani](#step-4---run-pyani-optional)
  - [Step 5 - Dereplicate with dRep](#step-5---dereplicate-with-drep)
  - [Step 6 - Classify with GTDB-Tk](#step-6---classify-with-gtdb-tk)
  - [Step 7 - Interpret species boundaries](#step-7---interpret-species-boundaries)
- [Scripts Reference](#scripts-reference)
- [Species Boundary Thresholds](#species-boundary-thresholds)
- [Example Results](#example-results)
- [Repository Structure](#repository-structure)
- [References](#references)

---

## What This Does

This framework takes a set of microbial genome assemblies and runs them through
a complete species delineation pipeline:

```
Genome assemblies (.fna)
        |
        v
FastANI - rapid all-vs-all ANI calculation
        |
        v
ANI matrix + heatmap + pairwise barplot
        |
        v
pyani   - detailed ANIb visualization (optional)
        |
        v
dRep    - genome comparison and dereplication
        |
        v
GTDB-Tk - taxonomy-aware classification
        |
        v
Species boundary assessment report
```

The result is a clear, evidence-based answer to: are these genomes the same species?

---

## Background

### Why ANI?

Traditional microbial species delineation used DNA-DNA Hybridization (DDH),
where strains sharing >=70% DDH were considered the same species (Goris et al., 2007).
DDH is labor-intensive and not scalable to large genomic datasets.

Average Nucleotide Identity (ANI) measures the mean nucleotide similarity between
shared genomic regions of two genomes. Studies have shown that ANI values of
approximately **95-96%** correspond closely to the traditional 70% DDH threshold,
making ANI the standard genomic metric for species delineation (Richter and Rossello-Mora, 2009).

### Why ANI alone is not enough

ANI should never be the only criterion. Always consider:

- Genome completeness and contamination
- Assembly quality (N50, contig count)
- Horizontal gene transfer and recombination
- Phylogenetic placement
- Ecological divergence
- GTDB taxonomy assignment

This framework integrates all these layers into one reproducible workflow.

---

## Installation

### Option 1 - conda (recommended)

```bash
# Create environment with all tools
conda create -n species_delineation python=3.10 -y
conda activate species_delineation

# Install bioinformatics tools
conda install -c bioconda -c conda-forge fastani drep -y

# Install Python dependencies
pip install -r requirements.txt
```

### Option 2 - install tools separately

```bash
# FastANI
conda install -c bioconda fastani -y
fastANI --version

# dRep
conda install -c bioconda drep -y
dRep -h

# pyani (optional)
pip install pyani

# GTDB-Tk (large database required)
conda install -c bioconda gtdbtk -y
download-db.sh
```

### Verify installation

```bash
fastANI --version
dRep -h | head -5
python3 -c "import pandas, matplotlib, numpy; print('Python deps OK')"
```

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/mbilal-OU/Genomic-Species-Delineation-Framework.git
cd Genomic-Species-Delineation-Framework

# Run FastANI on toy genomes
bash scripts/01_make_fastani_lists.sh
bash scripts/02_run_fastani_all_vs_all.sh

# Visualize results
python3 scripts/08_parse_fastani_and_plot.py

# View outputs
ls example_outputs/fastani/
ls figures/
```

---

## Step-by-Step Guide

### Step 1 - Prepare genome list

Put all your genome FASTA files in one directory and create a genome list:

```bash
# If using your own genomes
ls /path/to/genomes/*.fna > genome_list.txt
wc -l genome_list.txt

# If using toy genomes included in this repo
bash scripts/01_make_fastani_lists.sh
```

The script creates:
- `fastani_query_list.txt` - query genomes
- `fastani_reference_list.txt` - reference genomes (same list for all-vs-all)

---

### Step 2 - Run FastANI

```bash
bash scripts/02_run_fastani_all_vs_all.sh
```

Or run manually:

```bash
fastANI \
    --ql fastani_query_list.txt \
    --rl fastani_reference_list.txt \
    --output example_outputs/fastani/fastani_results.txt \
    --threads 8 \
    --matrix
```

Output:
```
example_outputs/fastani/fastani_results.txt        - pairwise ANI table
example_outputs/fastani/fastani_results.txt.matrix - square matrix
```

Each line: `query_genome  ref_genome  ANI  fragments_mapped  total_fragments`

---

### Step 3 - Visualize ANI results

```bash
python3 scripts/08_parse_fastani_and_plot.py
```

Generates:
- `figures/fastani_real_heatmap.png` - clustered ANI heatmap
- `figures/fastani_real_barplot.png` - pairwise comparison barplot

---

### Step 4 - Run pyani (optional)

pyani provides more detailed ANIb-based analysis with statistical output.
Useful when you need precise ANI values for borderline cases near the 95-96% threshold.

```bash
bash scripts/03_run_pyani.sh
```

Output saved to `example_outputs/pyani/`

---

### Step 5 - Dereplicate with dRep

dRep clusters genomes by ANI and selects the best representative from each cluster.
Use this when you have many closely related genomes and want to reduce redundancy.

```bash
bash scripts/04_run_drep_compare.sh
```

Key dRep parameters:
```
-pa 0.90    Primary clustering ANI threshold (genus level)
-sa 0.95    Secondary clustering ANI threshold (species level)
-nc 0.30    Minimum genome overlap required
-comp 50    Minimum genome completeness (requires CheckM)
-con 10     Maximum genome contamination (requires CheckM)
```

Output in `example_outputs/drep/`

---

### Step 6 - Classify with GTDB-Tk

GTDB-Tk places genomes in the GTDB taxonomy tree using marker genes
and phylogenetic placement. This gives you the most accurate, up-to-date
taxonomic classification.

```bash
bash scripts/06_run_gtdbtk_classify_example.sh
```

Or directly:

```bash
gtdbtk classify_wf \
    --genome_dir /path/to/genomes/ \
    --out_dir gtdbtk_results/ \
    --extension fna \
    --cpus 16
```

Key output: `gtdbtk_results/gtdbtk.bac120.summary.tsv`

---

### Step 7 - Interpret species boundaries

After running all tools, use this decision framework:

```
ANI >= 96%   + same GTDB species    = same species (high confidence)
ANI >= 96%   + different GTDB       = check phylogeny, possible misclassification
ANI 95-96%   + any taxonomy         = borderline - need more evidence
ANI 94-95%   + any taxonomy         = likely different species
ANI < 94%    + any taxonomy         = different species
```

Always cross-check with:
- CheckM2 completeness and contamination values
- dRep clustering results
- GTDB phylogenetic placement
- Published literature for the genus

---

## Scripts Reference

| Script | Tool | Description |
|---|---|---|
| `01_make_fastani_lists.sh` | - | Generate genome path lists for FastANI |
| `02_run_fastani_all_vs_all.sh` | FastANI | All-vs-all ANI comparison |
| `03_run_pyani.sh` | pyani | ANIb-based detailed comparison |
| `04_run_drep_compare.sh` | dRep | Genome comparison and dereplication |
| `05_run_drep_dereplicate.sh` | dRep | Dereplication with quality filtering |
| `06_run_gtdbtk_classify_example.sh` | GTDB-Tk | Taxonomy assignment |
| `07_run_fastani_matrix.sh` | FastANI | Matrix output format |
| `08_parse_fastani_and_plot.py` | Python | Heatmap and barplot generation |

---

## Species Boundary Thresholds

| ANI (%) | Classification | Confidence |
|---|---|---|
| 99-100 | Nearly identical strains | High |
| 96-99 | Same species | High |
| 95-96 | Species boundary zone | Borderline - use additional evidence |
| 94-95 | Likely different species | Moderate |
| < 94 | Different species | High |

These thresholds apply to bacteria and archaea. Always interpret ANI together
with genome quality, phylogenetic placement, and ecological context.

**Comparison with DDH:**
The 95-96% ANI threshold corresponds to approximately 70% DDH (Goris et al., 2007),
the traditional species boundary in prokaryotic taxonomy.

---

## Example Results

The included toy dataset spans multiple levels of genomic relatedness
to demonstrate the full range of ANI interpretation.

| Genome pair | FastANI (%) | Interpretation |
|---|---|---|
| A_reference vs B_same_species_98ANI | 97.85 | Same species |
| A_reference vs C_boundary_95ANI | 95.04 | Near species boundary |
| A_reference vs D_related_below_species_92ANI | 92.29 | Different species |
| A_reference vs E_distant_85ANI | 81.82 | Distant lineage |

### ANI Heatmap

![FastANI Heatmap](figures/fastani_real_heatmap.png)

### Pairwise ANI Comparison

![FastANI Barplot](figures/fastani_real_barplot.png)

---

## Repository Structure

```
Genomic-Species-Delineation-Framework/
|
|- scripts/
|   |- 01_make_fastani_lists.sh
|   |- 02_run_fastani_all_vs_all.sh
|   |- 03_run_pyani.sh
|   |- 04_run_drep_compare.sh
|   |- 05_run_drep_dereplicate.sh
|   |- 06_run_gtdbtk_classify_example.sh
|   |- 07_run_fastani_matrix.sh
|   |- 08_parse_fastani_and_plot.py
|
|- toy_genomes/              - synthetic genomes for testing
|- example_outputs/          - pre-generated output files
|   |- fastani/
|   |- pyani/
|   |- drep/
|
|- figures/                  - output plots
|- docs/                     - additional documentation
|- requirements.txt
|- LICENSE
|- README.md
```

---

## References

1. Konstantinidis KT, Tiedje JM. 2005. Genomic insights that advance the species
   definition for prokaryotes. PNAS 102:2567-2572.

2. Goris J et al. 2007. DNA-DNA hybridization values and their relationship to
   whole-genome sequence similarities. IJSEM 57:81-91.

3. Richter M, Rossello-Mora R. 2009. Shifting the genomic gold standard for the
   prokaryotic species definition. PNAS 106:19126-19131.

4. Jain C et al. 2018. High throughput ANI analysis of 90K prokaryotic genomes
   reveals clear species boundaries. Nature Communications 9:5114.

5. Olm MR et al. 2017. dRep: a tool for fast and accurate genomic comparisons.
   ISME Journal 11:2864-2868.

6. Parks DH et al. 2020. A complete domain-to-species taxonomy for Bacteria and
   Archaea. Nature Biotechnology 38:1079-1086.

---

## Author

**Muhammad Bilal**
Department of Biological Sciences, Oakland University
Rochester, Michigan, USA

---

## License

MIT License - free to use, modify, and distribute with attribution.
