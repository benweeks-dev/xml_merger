# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

A Python toolkit for merging and standardizing `gamelist.xml` files across emulation platforms (RetroBat, PC backup collections). The core workflow: parse multiple `gamelist.xml` sources → merge intelligently → standardize media paths → deploy unified gamelists.

## Running the Scripts

```bash
# Single system test (NGP example - edit paths inside first)
python test_ngp.py

# Batch process all systems (edit PC_BACKUP_BASE/RETROBAT_BASE/OUTPUT_DIR inside)
python batch_process_custom.py

# Deploy unified gamelists to RetroBat/PC backup folders
python deploy_unified_gamelists.py

# Rename gamelists in RetroBat (backs up old, activates new)
python gamelist_to_backup.py
```

No build step, no dependencies beyond the Python standard library (Python 3.7+).

## Architecture

**`gamelist_unifier.py`** — Core library. Contains:
- `GameEntry` dataclass: holds all fields for a single game (metadata + media paths + user data)
- `GameListUnifier` class: the main engine
  - `parse_gamelist()`: reads a `gamelist.xml`, merges into internal `self.games` dict keyed by ROM path. Handles both `<n>` (Skraper) and `<name>` (EmulationStation) tags.
  - `_merge_field()`: prefer-longer merge strategy — non-empty values win; longer strings win over shorter ones
  - `standardize_media_paths()`: rewrites all media paths to `./media/{type}/{subfolder}{romname}.ext` format, always using `mix/` for `<image>`
  - `validate_media()`: checks that referenced files actually exist on disk
  - `generate_unified_gamelist()`: writes output XML with all standard tags present (even empty ones), pretty-printed with explicit closing tags (no self-closing `<tag/>`)
  - `clean_game_name()`: strips region/language parentheticals like `(USA)`, `(Japan, Europe)`, `(En,Ja)` but preserves `(Rev 1)`, `(Beta)`

**`batch_process_custom.py`** — Ben's setup-specific batch processor. Hardcoded paths: `D:\ROMs BackUp\ROMs - 1G1R`, `D:\RetroBat\roms`, `D:\Unified_Gamelists`. Contains `SYSTEM_MAPPING` dict that maps RetroBat system names (e.g., `ngp`) to PC backup manufacturer folder paths (e.g., `SNK\NeoGeo Pocket`). PC backup gamelists are expected at `{system_path}/media/gamelist.xml`. Outputs `_MASTER_INDEX.txt` that `deploy_unified_gamelists.py` reads to find PC backup paths.

**`deploy_unified_gamelists.py`** — Copies `*_unified_gamelist.xml` files to RetroBat and PC backup destinations. Reads `_MASTER_INDEX.txt` from the unified output dir to find PC backup paths. Does NOT activate them (originals kept as `gamelist.xml`).

**`gamelist_to_backup.py`** — Activates unified gamelists in RetroBat only: renames `gamelist.xml` → `gamelist_BACKUP.xml` and `{system}_unified_gamelist.xml` → `gamelist.xml`.

**`test_ngp.py`** — Single-system test script for NGP. Paths hardcoded inside.

## Key Conventions

- ROM path (the `<path>` element) is the merge key — games are deduplicated by exact ROM path string
- `<image>` always maps to `./media/mix/` regardless of source data (RetroBat standard)
- `<thumbnail>` → `box2dfront/`, `<marquee>` → `wheel/`, `<video>` → `video/`
- All 24 standard tags are always written, even if empty — no self-closing tags in output
- Game names are cleaned by default (`clean_names=True`); pass `False` to disable
- Subfolders in ROM paths (e.g., `./JAPAN/game.zip`) are preserved in generated media paths

## Paths to Configure

All scripts have hardcoded paths near the top of their `main()`/processing function — edit before running:
- `PC_BACKUP_BASE`: root of the `ROMs - 1G1R` folder (manufacturer subdirectory structure)
- `RETROBAT_BASE`: root of RetroBat `roms/` folder (flat system subdirectory structure)
- `OUTPUT_DIR` / `UNIFIED_DIR`: where unified gamelists and reports are written
