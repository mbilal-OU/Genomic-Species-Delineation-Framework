#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt

out = Path("figures/genomic_species_delineation_workflow.png")
steps = [
    "Genome assemblies",
    "Genome quality screening",
    "FastANI / pyani",
    "ANI matrix + visualization",
    "dRep genome comparison",
    "GTDB-Tk taxonomy",
    "Species-boundary interpretation"
]

plt.figure(figsize=(8, 10))
ax = plt.gca()
ax.axis("off")

for i, step in enumerate(steps):
    y = len(steps) - i
    ax.text(0.5, y, step, ha="center", va="center", fontsize=13,
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="black"))
    if i < len(steps) - 1:
        ax.annotate("", xy=(0.5, y - 0.65), xytext=(0.5, y - 0.25),
                    arrowprops=dict(arrowstyle="->", lw=1.8))

ax.set_xlim(0, 1)
ax.set_ylim(0, len(steps) + 1)
plt.title("Genomic Species Delineation Framework", fontsize=15, pad=20)
plt.tight_layout()
plt.savefig(out, dpi=300)
print(f"Saved: {out}")
