# Changelog

## Unreleased

### Changed
- Reframed the project as **SpeciesResolve**, an evidence-aware microbial species delineation framework.
- Replaced binary ANI species calls with descriptive ANI context plus alignment-fraction reporting.
- Added reciprocal FastANI pair summaries instead of retaining only one direction.
- Added explicit preservation of missing FastANI comparisons.
- Clarified that dRep clustering is threshold-dependent operational clustering, not independent species evidence.
- Replaced deprecated pyani guidance with pyANI-plus.
- Generalized FastANI, dRep, and GTDB-Tk wrapper scripts for user-supplied genome sets.
- Added an evidence-concordance interpretation model for concordant, discordant, and unresolved cases.

### Added
- `environment.yml` for the core FastANI/dRep/Python environment.
- `docs/EVIDENCE_MODEL.md`.
- SpeciesResolve evidence-map SVG.
- FastANI parser unit tests.
- `CITATION.cff` and contribution guidance.

### Fixed
- Restored the complete MIT License text.
- Updated CI actions and expanded CI from syntax checks to parser unit tests.
