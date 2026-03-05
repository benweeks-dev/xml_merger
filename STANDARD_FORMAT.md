# Updated GameList Structure

## ✨ New Standard Format

All gamelists now follow the exact EmulationStation standard structure:

```xml
<?xml version="1.0"?>
<gameList>
  <game>
    <path>./Super Mario 64.z64</path>
    <name>Super Mario 64</name>
    <desc>A long description of the game...</desc>
    <rating>0.8</rating>
    <releasedate>19960623T000000</releasedate>
    <developer>Nintendo</developer>
    <publisher>Nintendo</publisher>
    <genre>Platform</genre>
    <players>1</players>
    <image>./media/mix/Super Mario 64.png</image>
    <thumbnail>./media/box2dfront/Super Mario 64.png</thumbnail>
    <marquee>./media/wheel/Super Mario 64.png</marquee>
    <video>./media/video/Super Mario 64.mp4</video>
    <fanart>./media/fanart/Super Mario 64.png</fanart>
    <boxback>./media/box2dback/Super Mario 64.png</boxback>
    <map>./media/maps/Super Mario 64.png</map>
    <manual>./media/manuals/Super Mario 64.pdf</manual>
    <favorite>false</favorite>
    <hidden>false</hidden>
    <kidgame>false</kidgame>
    <lastplayed>20240101T120000</lastplayed>
    <playcount>5</playcount>
    <lang>en</lang>
    <region>us</region>
  </game>
</gameList>
```

## 📋 Field Order (Exact)

1. **path** - ROM file path (required)
2. **name** - Game display name
3. **desc** - Description
4. **rating** - 0.0 to 1.0
5. **releasedate** - YYYYMMDDTHHMMSS format
6. **developer** - Developer name
7. **publisher** - Publisher name
8. **genre** - Genre/category
9. **players** - Player count
10. **image** - Main image (fanart/mix)
11. **thumbnail** - Box front art
12. **marquee** - Wheel/logo
13. **video** - Video preview
14. **fanart** - Background fanart
15. **boxback** - Box back art
16. **map** - Game map image
17. **manual** - PDF manual
18. **favorite** - true/false
19. **hidden** - true/false
20. **kidgame** - true/false
21. **lastplayed** - Last played timestamp
22. **playcount** - Number of times played
23. **lang** - Language code
24. **region** - Region code

## 🎨 Media Folder Structure

```
media/
├── mix/           # Main images (fanart blend)
├── box2dfront/    # Box front covers
├── wheel/         # Logos/marquees
├── video/         # Video previews (.mp4)
├── fanart/        # Background fanart
├── box2dback/     # Box back covers
├── maps/          # Game maps
├── manuals/       # PDF manuals
├── screenshot/    # In-game screenshots
└── titleshot/     # Title screens
```

## ✅ All Fields Always Present

Every game entry will have **all** these fields, even if empty:
- Empty strings: `<desc></desc>` or `<desc />`
- Default values: `<favorite>false</favorite>`, `<playcount>0</playcount>`

This ensures:
- ✅ Consistent XML structure
- ✅ Easy manual editing
- ✅ No frontend compatibility issues
- ✅ Clean diffs/comparisons

## 🚀 Your NGP Example Output

After running `test_ngp.py`, a Baseball Stars entry will look like:

```xml
<game source="ScreenScraper.fr">
  <path>./Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).zip</path>
  <name>Baseball Stars - Pocket Sports Series</name>
  <desc>Baseball Stars is sports game about baseball. Game is similar to Baseball Stars from NES but has less realistic characters and gameplay's style. You manage own baseball team and play in series of matches. Game has typical baseball rules - one player throws the ball, second hits the ball, someone else grabs it etc. Each character has own statistics, like stamina.</desc>
  <rating>0</rating>
  <releasedate>19981028T000000</releasedate>
  <developer>SNK</developer>
  <publisher>SNK</publisher>
  <genre>Sports</genre>
  <players>2</players>
  <image>./media/mix/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).png</image>
  <thumbnail>./media/box2dfront/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).png</thumbnail>
  <marquee>./media/wheel/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).png</marquee>
  <video></video>
  <fanart></fanart>
  <boxback>./media/box2dback/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).png</boxback>
  <map></map>
  <manual>./media/manuals/Baseball Stars - Pocket Sports Series (Japan, Europe) (En,Ja).pdf</manual>
  <favorite>false</favorite>
  <hidden>false</hidden>
  <kidgame>false</kidgame>
  <lastplayed></lastplayed>
  <playcount>0</playcount>
  <lang>jp,en</lang>
  <region>eu</region>
</game>
```

## 🎯 Key Features

1. **Clean name** - Removes "(Japan, Europe) (En,Ja)"
2. **Standard order** - Matches EmulationStation exactly
3. **All fields present** - Even empty ones
4. **Consistent media paths** - Uses proper folder structure
5. **Merged data** - Best info from all sources

Ready to run!
