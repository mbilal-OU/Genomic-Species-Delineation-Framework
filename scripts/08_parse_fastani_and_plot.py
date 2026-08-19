#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FASTANI_COLUMNS = [
    "query",
    "reference",
    "ANI",
    "fragments_mapped",
    "total_fragments",
]


def read_fastani(path: Path) -> pd.DataFrame:
    """Read FastANI tabular output and calculate directional alignment fraction."""
    if not path.exists():
        raise FileNotFoundError(f"Missing FastANI output: {path}")

    df = pd.read_csv(path, sep="\t", header=None, names=FASTANI_COLUMNS)
    if df.empty:
        return pd.DataFrame(columns=FASTANI_COLUMNS + ["alignment_fraction"])

    for column in ["ANI", "fragments_mapped", "total_fragments"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["query"] = df["query"].map(lambda x: Path(str(x)).stem)
    df["reference"] = df["reference"].map(lambda x: Path(str(x)).stem)
    df["alignment_fraction"] = np.where(
        df["total_fragments"] > 0,
        df["fragments_mapped"] / df["total_fragments"],
        np.nan,
    )
    return df


def ani_context(value: float) -> str:
    """Return a descriptive ANI context label without making a species verdict."""
    if pd.isna(value):
        return "not_reported"
    if value >= 95:
        return "at_or_above_common_95pct_reference"
    if value >= 90:
        return "below_common_species_reference"
    return "distant_or_low_similarity"


def summarize_unordered_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize reciprocal FastANI directions for each unordered genome pair."""
    nonself = df[df["query"] != df["reference"]].copy()
    if nonself.empty:
        return pd.DataFrame(
            columns=[
                "genome_a",
                "genome_b",
                "ani_mean",
                "ani_min",
                "ani_max",
                "alignment_fraction_mean",
                "alignment_fraction_min",
                "alignment_fraction_max",
                "directions_reported",
                "ani_context",
                "alignment_review",
            ]
        )

    ordered = nonself.apply(
        lambda row: sorted([row["query"], row["reference"]]), axis=1, result_type="expand"
    )
    nonself[["genome_a", "genome_b"]] = ordered

    summary = (
        nonself.groupby(["genome_a", "genome_b"], as_index=False)
        .agg(
            ani_mean=("ANI", "mean"),
            ani_min=("ANI", "min"),
            ani_max=("ANI", "max"),
            alignment_fraction_mean=("alignment_fraction", "mean"),
            alignment_fraction_min=("alignment_fraction", "min"),
            alignment_fraction_max=("alignment_fraction", "max"),
            directions_reported=("ANI", "count"),
        )
        .sort_values(["ani_mean", "genome_a", "genome_b"], ascending=[False, True, True])
        .reset_index(drop=True)
    )

    summary["ani_context"] = summary["ani_mean"].apply(ani_context)
    summary["alignment_review"] = np.where(
        summary["alignment_fraction_min"].isna(),
        "missing_alignment_fraction",
        np.where(
            summary["alignment_fraction_min"] < 0.5,
            "below_0.5_reference_af_review",
            "no_low_af_flag",
        ),
    )
    return summary


def make_pair_matrices(df: pd.DataFrame, summary: pd.DataFrame):
    genomes = sorted(set(df.get("query", [])) | set(df.get("reference", [])))
    ani_matrix = pd.DataFrame(np.nan, index=genomes, columns=genomes, dtype=float)
    af_matrix = pd.DataFrame(np.nan, index=genomes, columns=genomes, dtype=float)

    for genome in genomes:
        ani_matrix.loc[genome, genome] = 100.0
        af_matrix.loc[genome, genome] = 1.0

    for _, row in summary.iterrows():
        a = row["genome_a"]
        b = row["genome_b"]
        ani_matrix.loc[a, b] = row["ani_mean"]
        ani_matrix.loc[b, a] = row["ani_mean"]
        af_matrix.loc[a, b] = row["alignment_fraction_min"]
        af_matrix.loc[b, a] = row["alignment_fraction_min"]

    return ani_matrix, af_matrix


def plot_heatmap(matrix: pd.DataFrame, out_file: Path, title: str, label: str):
    if matrix.empty:
        return
    plt.figure(figsize=(9, 7))
    masked = np.ma.masked_invalid(matrix.values.astype(float))
    im = plt.imshow(masked, vmin=80, vmax=100)
    plt.colorbar(im, label=label)
    plt.xticks(range(len(matrix.columns)), matrix.columns, rotation=45, ha="right", fontsize=8)
    plt.yticks(range(len(matrix.index)), matrix.index, fontsize=8)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix.iloc[i, j]
            if pd.notna(value):
                plt.text(j, i, f"{value:.1f}", ha="center", va="center", fontsize=7)

    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()


def plot_pairwise_ani(summary: pd.DataFrame, out_file: Path, reference_ani: float):
    if summary.empty:
        return
    plot_df = summary.copy()
    plot_df["pair"] = plot_df["genome_a"] + " vs " + plot_df["genome_b"]
    plot_df = plot_df.sort_values("ani_mean", ascending=True)

    plt.figure(figsize=(10, max(5, len(plot_df) * 0.35)))
    plt.barh(plot_df["pair"], plot_df["ani_mean"])
    plt.axvline(reference_ani, linestyle="--", label=f"{reference_ani:g}% reference ANI")
    plt.xlabel("Mean reciprocal FastANI (%)")
    plt.ylabel("Genome pair")
    plt.title("Pairwise FastANI summary")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()


def plot_ani_vs_af(summary: pd.DataFrame, out_file: Path, reference_ani: float):
    if summary.empty:
        return
    valid = summary.dropna(subset=["ani_mean", "alignment_fraction_min"])
    if valid.empty:
        return

    plt.figure(figsize=(8, 6))
    plt.scatter(valid["ani_mean"], valid["alignment_fraction_min"], alpha=0.8)
    plt.axvline(reference_ani, linestyle="--", label=f"{reference_ani:g}% reference ANI")
    plt.axhline(0.5, linestyle=":", label="0.5 reference AF line")
    plt.xlabel("Mean reciprocal FastANI (%)")
    plt.ylabel("Minimum reported alignment fraction")
    plt.title("ANI and genome overlap")
    plt.ylim(0, 1.03)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Parse FastANI output without forcing a binary species verdict."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("example_outputs/fastani/fastani_all_vs_all.tsv"),
        help="FastANI five-column output file.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("example_outputs/fastani"),
        help="Directory for parsed tables.",
    )
    parser.add_argument(
        "--fig-dir",
        type=Path,
        default=Path("figures"),
        help="Directory for figures.",
    )
    parser.add_argument(
        "--reference-ani",
        type=float,
        default=95.0,
        help="Reference ANI line used for plots only. It is not an automatic species verdict.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.fig_dir.mkdir(parents=True, exist_ok=True)

    directional = read_fastani(args.input)
    pairwise = summarize_unordered_pairs(directional)
    ani_matrix, af_matrix = make_pair_matrices(directional, pairwise)

    directional.to_csv(args.out_dir / "fastani_directional.tsv", sep="\t", index=False)
    pairwise.to_csv(args.out_dir / "fastani_pairwise_summary.csv", index=False)
    ani_matrix.to_csv(args.out_dir / "fastani_ani_matrix.csv")
    af_matrix.to_csv(args.out_dir / "fastani_alignment_fraction_matrix.csv")

    plot_heatmap(
        ani_matrix,
        args.fig_dir / "fastani_ani_heatmap.png",
        "FastANI mean reciprocal ANI",
        "ANI (%)",
    )
    plot_pairwise_ani(
        pairwise,
        args.fig_dir / "fastani_pairwise_ani.png",
        args.reference_ani,
    )
    plot_ani_vs_af(
        pairwise,
        args.fig_dir / "fastani_ani_vs_alignment_fraction.png",
        args.reference_ani,
    )

    print("Created:")
    print(args.out_dir / "fastani_directional.tsv")
    print(args.out_dir / "fastani_pairwise_summary.csv")
    print(args.out_dir / "fastani_ani_matrix.csv")
    print(args.out_dir / "fastani_alignment_fraction_matrix.csv")
    print(args.fig_dir / "fastani_ani_heatmap.png")
    print(args.fig_dir / "fastani_pairwise_ani.png")
    print(args.fig_dir / "fastani_ani_vs_alignment_fraction.png")


if __name__ == "__main__":
    main()
