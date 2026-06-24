#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

matrix_file = Path("example_outputs/example_ani_matrix.csv")
out_file = Path("figures/example_ani_heatmap_from_script.png")

ani = pd.read_csv(matrix_file, index_col=0)

plt.figure(figsize=(8, 6))
im = plt.imshow(ani.values, vmin=80, vmax=100)
plt.colorbar(im, label="ANI (%)")
plt.xticks(range(len(ani.columns)), ani.columns, rotation=45, ha="right", fontsize=8)
plt.yticks(range(len(ani.index)), ani.index, fontsize=8)

for i in range(ani.shape[0]):
    for j in range(ani.shape[1]):
        plt.text(j, i, f"{ani.iloc[i, j]:.1f}", ha="center", va="center", fontsize=7)

plt.title("Example ANI Heatmap")
plt.tight_layout()
plt.savefig(out_file, dpi=300)
print(f"Saved: {out_file}")
