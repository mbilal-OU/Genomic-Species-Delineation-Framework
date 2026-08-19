from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "08_parse_fastani_and_plot.py"
spec = importlib.util.spec_from_file_location("speciesresolve_fastani", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def write_fastani(tmp_path: Path) -> Path:
    path = tmp_path / "fastani.tsv"
    path.write_text(
        "A.fna\tA.fna\t100\t100\t100\n"
        "B.fna\tB.fna\t100\t100\t100\n"
        "C.fna\tC.fna\t100\t100\t100\n"
        "A.fna\tB.fna\t97\t80\t100\n"
        "B.fna\tA.fna\t96\t70\t100\n"
        "B.fna\tC.fna\t94\t20\t100\n"
    )
    return path


def test_alignment_fraction_and_reciprocal_summary(tmp_path):
    df = module.read_fastani(write_fastani(tmp_path))
    ab = df[(df["query"] == "A") & (df["reference"] == "B")].iloc[0]
    assert np.isclose(ab["alignment_fraction"], 0.80)

    summary = module.summarize_unordered_pairs(df)
    pair = summary[(summary["genome_a"] == "A") & (summary["genome_b"] == "B")].iloc[0]

    assert np.isclose(pair["ani_mean"], 96.5)
    assert np.isclose(pair["ani_min"], 96.0)
    assert np.isclose(pair["ani_max"], 97.0)
    assert np.isclose(pair["alignment_fraction_min"], 0.70)
    assert pair["directions_reported"] == 2
    assert pair["ani_context"] == "at_or_above_common_95pct_reference"
    assert pair["alignment_review"] == "no_low_af_flag"


def test_low_alignment_fraction_is_flagged(tmp_path):
    df = module.read_fastani(write_fastani(tmp_path))
    summary = module.summarize_unordered_pairs(df)
    pair = summary[(summary["genome_a"] == "B") & (summary["genome_b"] == "C")].iloc[0]

    assert np.isclose(pair["ani_mean"], 94.0)
    assert np.isclose(pair["alignment_fraction_min"], 0.20)
    assert pair["directions_reported"] == 1
    assert pair["ani_context"] == "below_common_species_reference"
    assert pair["alignment_review"] == "below_0.5_reference_af_review"


def test_unreported_pair_stays_missing(tmp_path):
    df = module.read_fastani(write_fastani(tmp_path))
    summary = module.summarize_unordered_pairs(df)
    ani_matrix, af_matrix = module.make_pair_matrices(df, summary)

    assert np.isnan(ani_matrix.loc["A", "C"])
    assert np.isnan(af_matrix.loc["A", "C"])
    assert ani_matrix.loc["A", "A"] == 100.0
    assert af_matrix.loc["A", "A"] == 1.0


def test_empty_file_is_supported(tmp_path):
    empty = tmp_path / "empty.tsv"
    empty.write_text("")
    df = module.read_fastani(empty)
    summary = module.summarize_unordered_pairs(df)
    assert df.empty
    assert summary.empty
