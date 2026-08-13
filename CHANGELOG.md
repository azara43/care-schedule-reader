# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-14

First public release.

### Added
- `care-schedule-reader` skill: reads photos of handwritten or printed care
  schedules and returns structured records.
- Deadline extraction from both cover notes and marked grid cells.
- Three-level confidence tagging on every row: Confirmed / Requested / Uncertain.
- Transport extraction from sticky-note blocks (outbound and return legs).
- Date/weekday mismatch detection.
- User-defined legend file (`legend.md`, `care-legend.md`, or
  `~/.claude/care-legend.md`) with a documented example.
- Privacy rules: no external transmission without a human in the loop; health
  details kept out of filenames and calendar titles.
- Fictional sample schedule and expected output for demos and testing.
