# GameList Unifier - Updates Summary

## ✨ New Features Added

### 1. Automatic Name Cleaning
**What it does:** Removes region and language tags from game names

**Examples:**
- `"Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja)"` 
  → `"Baseball Stars - Pocket Sports Series"`
- `"King of Fighters R-1 - Pocket Fighting Series (Japan, Europe) (En,Ja)"` 
  → `"King of Fighters R-1 - Pocket Fighting Series"`

**How to use:**
```python
# Name cleaning is enabled by default
unifier = GameListUnifier(clean_names=True)

# To disable:
unifier = GameListUnifier(clean_names=False)
```

**Patterns removed:**
- Single regions: `(USA)`, `(Japan)`, `(Europe)`, `(World)`, etc.
- Multiple regions: `(Japan, Europe)`, `(USA, Europe)`, etc.
- Language codes: `(En)`, `(En,Ja)`, `(En,Fr,De)`, etc.
- Keeps revision info: `(Rev 1)`, `(Beta)`, etc.

---

### 2. Always Include All Standard Tags
**What it does:** Every game entry now has all standard XML tags, even if empty

**Why this is good:**
- ✅ Consistent XML structure across all games
- ✅ Easier to manually edit (fields are already there)
- ✅ No issues with frontends expecting certain tags
- ✅ Cleaner diffs when comparing files

**Example output:**
```xml
<game>
  <path>./game.zip</path>
  <name>Game Name</name>
  <desc>Description here</desc>
  <rating>0.85</rating>
  <releasedate>19981028T000000</releasedate>
  <developer>SNK</developer>
  <publisher>SNK</publisher>
  <genre>Action</genre>
  <players>1-2</players>
  <hash>ABCD1234</hash>
  <md5></md5>  <!-- Empty but present -->
  <genreid>262</genreid>
  <lang></lang>  <!-- Empty but present -->
  <region></region>  <!-- Empty but present -->
  <image>./media/mix/game.png</image>
  <thumbnail>./media/box2dfront/game.png</thumbnail>
  <marquee>./media/wheel/game.png</marquee>
  <video></video>  <!-- Empty but present -->
  <boxback>./media/box2dback/game.png</boxback>
  <manual></manual>  <!-- Empty but present -->
  <screenshot></screenshot>  <!-- Empty but present -->
</game>
```

---

### 3. Force <image> to Use Mix Folder
**What it does:** The `<image>` tag **always** uses `./media/mix/` regardless of source

**Why:**
- Your RetroBat gamelists use mix (fanart/screenshot blend)
- Your PC backup uses box2dfront for image
- Standardizing on mix gives you the better visual experience

**Result:**
```xml
<image>./media/mix/GameName.png</image>
```

**Other media paths still respect source data:**
- `<thumbnail>` → box2dfront (if exists)
- `<marquee>` → wheel (if exists)
- `<boxback>` → box2dback (if exists)

---

## 📋 Standard Tags Always Included

### Core Metadata (always included):
- `<path>` - ROM file path (required)
- `<name>` - Game name (cleaned)
- `<desc>` - Description
- `<rating>` - Rating (0.0-1.0)
- `<releasedate>` - Release date (YYYYMMDDTHHMMSS)
- `<developer>` - Developer name
- `<publisher>` - Publisher name
- `<genre>` - Genre/category
- `<players>` - Player count (e.g., "1-2")

### Technical Metadata (always included):
- `<hash>` - ROM hash
- `<md5>` - MD5 checksum
- `<genreid>` - Numeric genre ID
- `<lang>` - Language codes
- `<region>` - Region codes

### Media Paths (always included):
- `<image>` - Main image (mix folder)
- `<thumbnail>` - Box front art
- `<marquee>` - Wheel/logo
- `<video>` - Video preview
- `<boxback>` - Box back art
- `<manual>` - PDF manual
- `<screenshot>` - Screenshot

---

## 🎯 Usage

### test_ngp.py (Your Custom Script)

Just update the paths and run:

```bash
python test_ngp.py
```

**What it does:**
1. ✅ Parses both PC backup and RetroBat gamelists
2. ✅ Cleans game names (removes regions/languages)
3. ✅ Merges data (prefers more complete info)
4. ✅ Forces `<image>` to use mix folder
5. ✅ Includes all standard tags (even if empty)
6. ✅ Validates media files
7. ✅ Generates unified gamelist + reports

**Output files:**
- `ngp_unified_gamelist.xml` - Your clean, standardized gamelist
- `ngp_unification_report.txt` - Data quality report
- `ngp_source_comparison.txt` - Shows which source provided what data
- `ngp_*_missing_media.txt` - Missing media reports (if any)

---

## 💡 Before/After Example

### Before (PC Backup):
```xml
<game id="0" source="ScreenScraper.fr">
  <path>./Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).zip</path>
  <n>Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja)</n>
  <desc />
  <releasedate />
  <developer />
  <publisher />
  <genre />
  <players />
</game>
```

### Before (RetroBat):
```xml
<game source="ScreenScraper.fr">
  <path>./Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).zip</path>
  <n>Baseball Stars - Pocket Sports Series</n>
  <desc>Baseball Stars is sports game about baseball...</desc>
  <genre>Sports</genre>
  <image>./media/mix/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).png</image>
  <marquee>./media/wheel/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).png</marquee>
  <thumbnail>./media/box2dfront/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).png</thumbnail>
  <rating>0</rating>
  <releasedate>19981028T000000</releasedate>
  <developer>SNK</developer>
  <publisher>SNK</publisher>
  <players>2</players>
</game>
```

### After (Unified):
```xml
<game source="ScreenScraper.fr">
  <path>./Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).zip</path>
  <name>Baseball Stars - Pocket Sports Series</name>
  <desc>Baseball Stars is sports game about baseball...</desc>
  <rating>0</rating>
  <releasedate>19981028T000000</releasedate>
  <developer>SNK</developer>
  <publisher>SNK</publisher>
  <genre>Sports</genre>
  <players>2</players>
  <hash></hash>
  <md5></md5>
  <genreid></genreid>
  <lang></lang>
  <region></region>
  <image>./media/mix/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).png</image>
  <thumbnail>./media/box2dfront/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).png</thumbnail>
  <marquee>./media/wheel/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).png</marquee>
  <video></video>
  <boxback></boxback>
  <manual></manual>
  <screenshot></screenshot>
</game>
```

**Key improvements:**
✅ Name cleaned (no region tags)
✅ Complete description (from RetroBat)
✅ All metadata fields present
✅ All media tags present (even if empty)
✅ Consistent structure
✅ Uses `<name>` instead of `<n>`

---

## 🚀 Ready to Run!

Your files are updated and ready to go. Just:

1. Open `test_ngp.py`
2. Update the RetroBat path (line 23)
3. Run: `python test_ngp.py`
4. Review the output files
5. Copy the unified gamelist to both locations (with backups!)

Questions? Let me know!
