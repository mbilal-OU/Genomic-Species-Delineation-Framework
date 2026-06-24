# ANI Software Comparison

| Tool | Best use | Notes |
|---|---|---|
| FastANI | fast all-vs-all ANI for many genomes | scalable and commonly used |
| pyani | detailed ANI methods and heatmaps | includes ANIb, ANIm, TETRA depending on setup |
| dRep | dereplication and representative genome selection | useful for large genome collections/MAGs |
| GTDB-Tk | taxonomy and species placement | integrates genome classification with reference taxonomy |

## Recommended Use

- Use **FastANI** for rapid pairwise or all-vs-all ANI screening.
- Use **pyani** when you want a teaching-friendly ANI matrix workflow and graphical summaries.
- Use **dRep** when you have many genomes and need representative genomes.
- Use **GTDB-Tk** when you need standardized bacterial/archaeal taxonomy.
