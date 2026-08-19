# Contributing to SpeciesResolve

Contributions are welcome when they improve reproducibility, species-boundary interpretation, test coverage, current tool compatibility, or documentation.

## Keep the evidence model explicit

Changes should preserve the distinction between:

- genome-quality evidence;
- ANI and alignment fraction;
- taxonomic/reference context;
- threshold-dependent clustering;
- alternative ANI methods;
- phylogenomic context.

Do not add rules that convert one ANI cutoff into an automatic taxonomic verdict.

## Before opening a pull request

Run:

```bash
python -m py_compile scripts/*.py
for script in scripts/*.sh; do bash -n "$script"; done
pytest -q
```

## Software changes

When updating commands for FastANI, dRep, pyANI-plus, GTDB-Tk, or other external tools:

1. check the current primary project documentation;
2. state any version-dependent behavior;
3. avoid silently changing biological interpretation when only software syntax changed.

## Scientific changes

Changes to ANI reference values, alignment-fraction handling, quality thresholds, or taxonomic interpretation should explain the scientific rationale and retain missing or discordant evidence rather than replacing it with invented values.
