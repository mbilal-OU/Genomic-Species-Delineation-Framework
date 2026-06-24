#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fastani_file = Path("example_outputs/fastani/fastani_all_vs_all.tsv")
out_dir = Path("example_outputs/fastani")
fig_dir = Path("figures")

out_dir.mkdir(parents=True, exist_ok=True)
fig_dir.mkdir(parents=True, exist_ok=True)

if not fastani_file.exists():
    raise FileNotFoundError(f"Missing FastANI output: {fastani_file}")

df = pd.read_csv(
    fastani_file,
    sep="\t",
    header=None,
    names=["query", "reference", "ANI", "fragments_mapped", "total_fragments"]
)

df["query"] = df["query"].map(lambda x: Path(x).stem)
df["reference"] = df["reference"].map(lambda x: Path(x).stem)

genomes = sorted(set(df["query"]) | set(df["reference"]))

matrix = pd.DataFrame(np.nan, index=genomes, columns=genomes)

for _, row in df.iterrows():
    matrix.loc[row["query"], row["reference"]] = row["ANI"]

# Fill diagonal if needed
for g in genomes:
    matrix.loc[g, g] = 100.0 if pd.isna(matrix.loc[g, g]) else matrix.loc[g, g]

matrix.to_csv(out_dir / "fastani_matrix.csv")

pairwise = df[df["query"] != df["reference"]].copy()
pairwise["pair"] = pairwise["query"] + " vs " + pairwise["reference"]
pairwise["classification"] = pairwise["ANI"].apply(
    lambda x: "Likely same species" if x >= 95 else "Likely different species"
)
pairwise.to_csv(out_dir / "fastani_pairwise_interpreted.csv", index=False)

# Heatmap
plt.figure(figsize=(9, 7))
im = plt.imshow(matrix.values, vmin=80, vmax=100)
plt.colorbar(im, label="FastANI (%)")
plt.xticks(range(len(matrix.columns)), matrix.columns, rotation=45, ha="right", fontsize=8)
plt.yticks(range(len(matrix.index)), matrix.index, fontsize=8)

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        val = matrix.iloc[i, j]
        if pd.notna(val):
            plt.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=7)

plt.title("FastANI All-vs-All Heatmap")
plt.tight_layout()
plt.savefig(fig_dir / "fastani_real_heatmap.png", dpi=300)
plt.close()

# Barplot, remove reciprocal duplicates by sorted pair
tmp = pairwise.copy()
tmp["pair_key"] = tmp.apply(lambda r: " -- ".join(sorted([r["query"], r["reference"]])), axis=1)
tmp = tmp.sort_values("ANI", ascending=False).drop_duplicates("pair_key")
tmp = tmp.sort_values("ANI", ascending=True)

plt.figure(figsize=(9, 6))
plt.barh(tmp["pair_key"], tmp["ANI"])
plt.axvline(95, linestyle="--", label="95% ANI boundary")
plt.xlabel("FastANI (%)")
plt.ylabel("Genome pair")
plt.title("FastANI Pairwise Genome Similarity")
plt.legend()
plt.tight_layout()
plt.savefig(fig_dir / "fastani_real_barplot.png", dpi=300)
plt.close()

print("Created:")
print(out_dir / "fastani_matrix.csv")
print(out_dir / "fastani_pairwise_interpreted.csv")
print(fig_dir / "fastani_real_heatmap.png")
print(fig_dir / "fastani_real_barplot.png")
