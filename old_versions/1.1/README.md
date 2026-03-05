# GameList Unifier Toolkit

Complete toolkit for managing and standardizing gamelist.xml files across multiple emulation platforms (RetroBat, RetroDECK, Miyoo Mini Plus, etc.)

## 📦 What's Included

### Core Tools

1. **gamelist_unifier.py** - Main library for merging and standardizing gamelists
2. **example_usage.py** - Single system processing example
3. **batch_process.py** - Process all systems at once
4. **media_organizer.py** - Reorganize and validate media files

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Your ROM collections with gamelist.xml files

### Basic Usage

#### Option 1: Process One System at a Time

```python
python example_usage.py
```

Edit the script to configure:
- Your platform paths (PC backup, RetroBat, Miyoo, etc.)
- Which system to process (ngp, n64, psx, etc.)
- Output directory

#### Option 2: Batch Process Everything

```python
python batch_process.py
```

This will:
- Automatically discover all systems across all platforms
- Merge gamelists for each system
- Generate unified gamelists and reports
- Create a master index

## 📋 Detailed Workflow

### Step 1: Configure Your Paths

Edit `batch_process.py` or `example_usage.py`:

```python
PLATFORMS = {
    'pc_backup': Path(r'D:\Backups\Emulation\roms'),
    'retrobat': Path(r'C:\RetroBat\roms'),
    'miyoo': Path(r'E:\Miyoo\roms'),
}
```

### Step 2: Run the Batch Processor

```bash
python batch_process.py
```

This will generate:
- `{system}_unified_gamelist.xml` - Merged gamelist for each system
- `{system}_report.txt` - Data quality report
- `{system}_missing_media.txt` - Missing media files (if any)
- `_INDEX.txt` - Master summary

### Step 3: Review the Results

Check the output directory for:
- ✅ Complete metadata coverage
- ⚠️ Missing descriptions, developers, dates
- 🖼️ Missing media files

### Step 4: Deploy Unified Gamelists

Copy the unified gamelists back to your platforms:

```
retrobat:  C:\RetroBat\roms\{system}\gamelist.xml
miyoo:     E:\Miyoo\roms\{system}\gamelist.xml
retrodeck: /path/to/retrodeck/roms/{system}/gamelist.xml
```

## 🎨 Media Organization

### Current Recommended Structure

```
roms/{system}/
├── gamelist.xml
├── media/
│   ├── box2dfront/    # Box/cover art (front)
│   ├── box2dback/     # Box art (back)
│   ├── mix/           # Screenshots/fanart
│   ├── wheel/         # Logos/marquees
│   ├── screenshot/    # In-game screenshots
│   ├── video/         # Video previews
│   ├── manual/        # PDF manuals
│   └── titleshot/     # Title screens
└── [ROM files]
```

### Reorganize Media Files

If your media is scattered across different folder names:

```python
from media_organizer import MediaOrganizer

organizer = MediaOrganizer(Path(r'C:\RetroBat\roms\ngp'))

# Scan current structure
organizer.scan_media_structure()

# Find issues
organizer.find_duplicates()
organizer.validate_file_extensions()

# Reorganize (dry run first!)
organizer.reorganize_to_standard(dry_run=True)

# Actually move files
organizer.reorganize_to_standard(dry_run=False)
```

## 🔧 Advanced Features

### Field Standardization

The unifier handles various field name inconsistencies:

- `<n>` vs `<name>` (Skraper vs EmulationStation)
- `<image>` paths (different media types)
- `<thumbnail>` meanings (varies by scraper)

### Smart Merging

When multiple gamelists exist for the same game:
- Prefers longer/more complete descriptions
- Keeps all unique media file references
- Preserves technical metadata (hash, genreid, etc.)

### Media Path Mapping

Automatically maps common variations:
```
box2dfront ← boxfront, cover, covers
wheel ← marquee, logo, logos
mix ← fanart, screenshot
```

## 📊 Understanding Reports

### Unification Report

Shows:
- Total games processed
- Media coverage by source
- Games with incomplete metadata
- Data source attribution

### Missing Media Report

Lists files referenced in gamelist but not found on disk:
```
BOX2DFRONT - 5 missing:
  ./media/box2dfront/game1.png
  ./media/box2dfront/game2.png
  ...
```

### Media Organization Report

Shows:
- Current file counts by type
- Duplicate files (same name, different locations)
- Unexpected file extensions

## 🎯 Best Practices

### Before You Start

1. **Backup everything** - Copy your ROM folders first
2. **Pick a master** - Choose your most complete collection as the base
3. **Test on one system** - Run on a single system before batch processing

### Media Organization

✅ **DO:**
- Keep separate folders for each media type
- Use relative paths (`./media/...`)
- Standardize on one file extension per type (PNG for images, MP4 for videos)

❌ **DON'T:**
- Mix media types in one folder
- Use absolute paths
- Have duplicate filenames in different folders

### Gamelist Quality

1. Always review the generated reports
2. Re-scrape games with missing metadata
3. Validate media file existence before deploying
4. Keep backups of working gamelists

## 🐛 Troubleshooting

### "No gamelist.xml files found"
- Check your platform paths in the configuration
- Ensure gamelist.xml files exist in `{path}/{system}/gamelist.xml`

### "Media validation shows 0% found"
- Check if media paths in gamelist match your actual folder structure
- Run media_organizer to fix folder naming issues

### "Duplicate entries with different data"
- This is normal - the merger keeps the most complete version
- Check the report to see which source was used for each field

## 📝 Example Output

After running batch_process.py:

```
✅ COMPLETE!

Output files in: D:\Unified_Gamelists
  📄 ngp_unified_gamelist.xml
  📄 n64_unified_gamelist.xml
  📄 psx_unified_gamelist.xml
  📋 ngp_report.txt
  📋 n64_report.txt
  📋 psx_report.txt
  📋 _INDEX.txt
```

## 🤝 Contributing

Found a bug or have a suggestion? Feel free to modify these scripts for your needs!

## 📄 License

Free to use and modify for personal use.

---

**Happy Gaming! 🎮**
