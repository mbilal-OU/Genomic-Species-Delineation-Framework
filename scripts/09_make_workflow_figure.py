#!/usr/bin/env python3

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

OUT = Path("figures/speciesresolve_evidence_map.png")
OUT.parent.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")

ax.text(6, 7.55, "SpeciesResolve", ha="center", va="center", fontsize=24, fontweight="bold")
ax.text(
    6,
    7.12,
    "Species delineation by evidence concordance, not one cutoff",
    ha="center",
    va="center",
    fontsize=12,
)

center = Circle((6, 4.0), 1.15, fill=False, linewidth=2.2)
ax.add_patch(center)
ax.text(6, 4.18, "Species", ha="center", va="center", fontsize=16, fontweight="bold")
ax.text(6, 3.82, "hypothesis", ha="center", va="center", fontsize=16, fontweight="bold")

nodes = [
    (1.25, 5.4, 2.7, 1.3, "Genome quality", "completeness\ncontamination\nassembly continuity"),
    (4.65, 5.55, 2.7, 1.3, "ANI + AF", "identity\nalignment fraction\nmissing comparisons"),
    (8.05, 5.4, 2.7, 1.3, "GTDB context", "representative radius\nAF criterion\nphylogenomic placement"),
    (2.35, 1.25, 2.7, 1.3, "dRep clustering", "operational groups\nrepresentative selection\nthreshold dependent"),
    (6.95, 1.25, 2.7, 1.3, "Method cross-check", "pyANI-plus\nselected pairs\nmethod sensitivity"),
]

for x, y, w, h, title, body in nodes:
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.03,rounding_size=0.08",
        fill=False,
        linewidth=1.7,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h * 0.69, title, ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(x + w / 2, y + h * 0.34, body, ha="center", va="center", fontsize=9)

links = [
    ((3.95, 5.4), (5.15, 4.6)),
    ((6.0, 5.55), (6.0, 5.15)),
    ((8.05, 5.4), (6.85, 4.6)),
    ((5.05, 2.55), (5.45, 3.0)),
    ((8.0, 2.55), (6.65, 3.0)),
]
for start, end in links:
    ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", linewidth=1.5))

ax.text(6, 0.55, "Interpretation states: concordant support | discordant evidence | unresolved", ha="center", fontsize=11)
ax.text(6, 0.18, "No automatic taxonomic act", ha="center", fontsize=9)

plt.tight_layout()
plt.savefig(OUT, dpi=300, bbox_inches="tight")
print(f"Saved: {OUT}")
