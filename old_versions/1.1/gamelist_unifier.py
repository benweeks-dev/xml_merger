#!/usr/bin/env python3
"""
GameList Unifier - Merge and standardize gamelist.xml files across emulation platforms
Supports: RetroBat, RetroDECK, Miyoo Mini Plus, and other EmulationStation-based systems
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
import sys
from collections import defaultdict

@dataclass
class GameEntry:
    """Represents a unified game entry with all possible metadata"""
    path: str
    name: str = ""
    desc: str = ""
    rating: str = ""
    releasedate: str = ""
    developer: str = ""
    publisher: str = ""
    genre: str = ""
    players: str = ""
    hash: str = ""
    md5: str = ""
    genreid: str = ""
    lang: str = ""
    region: str = ""
    
    # Media paths
    image: str = ""  # Main image (mix/fanart)
    thumbnail: str = ""  # Box front
    marquee: str = ""  # Wheel/logo
    video: str = ""
    boxback: str = ""
    manual: str = ""
    screenshot: str = ""
    titleshot: str = ""
    
    # Metadata
    source: str = ""
    game_id: str = ""
    
    # Track which fields came from which source
    data_sources: Dict[str, str] = field(default_factory=dict)

class GameListUnifier:
    """Main class for merging and standardizing gamelist.xml files"""
    
    # Standard media field mappings
    MEDIA_FIELDS = {
        'image', 'thumbnail', 'marquee', 'video', 'boxback', 
        'manual', 'screenshot', 'titleshot'
    }
    
    # All metadata fields to track
    METADATA_FIELDS = {
        'name', 'desc', 'rating', 'releasedate', 'developer', 'publisher',
        'genre', 'players', 'hash', 'md5', 'genreid', 'lang', 'region'
    }
    
    def __init__(self):
        self.games: Dict[str, GameEntry] = {}  # keyed by ROM path
        self.provider_info: Dict[str, str] = {}
        self.media_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        
    def parse_gamelist(self, xml_path: Path, source_name: str = None) -> None:
        """Parse a gamelist.xml file and merge into unified database"""
        if source_name is None:
            source_name = xml_path.parent.name
            
        print(f"\n📖 Parsing: {xml_path}")
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
        except Exception as e:
            print(f"❌ Error parsing {xml_path}: {e}")
            return
        
        # Extract provider info
        provider = root.find('provider')
        if provider is not None and not self.provider_info:
            for child in provider:
                self.provider_info[child.tag] = child.text or ""
        
        # Process each game
        games_found = 0
        for game in root.findall('game'):
            path_elem = game.find('path')
            if path_elem is None or not path_elem.text:
                continue
                
            rom_path = path_elem.text.strip()
            games_found += 1
            
            # Get or create game entry
            if rom_path not in self.games:
                self.games[rom_path] = GameEntry(path=rom_path)
            
            entry = self.games[rom_path]
            
            # Merge metadata (prefer non-empty values)
            self._merge_field(entry, game, 'n', 'name', source_name)  # Skraper uses <n>
            self._merge_field(entry, game, 'name', 'name', source_name)  # EmulationStation uses <name>
            
            for field in ['desc', 'rating', 'releasedate', 'developer', 'publisher',
                         'genre', 'players', 'hash', 'md5', 'genreid', 'lang', 'region']:
                self._merge_field(entry, game, field, field, source_name)
            
            # Merge media paths
            for media_field in self.MEDIA_FIELDS:
                self._merge_field(entry, game, media_field, media_field, source_name)
            
            # Store source info
            if not entry.source:
                entry.source = game.get('source', '')
            if not entry.game_id:
                entry.game_id = game.get('id', '')
        
        print(f"   ✓ Found {games_found} games")
    
    def _merge_field(self, entry: GameEntry, game_elem: ET.Element, 
                    xml_tag: str, field_name: str, source_name: str) -> None:
        """Merge a single field, preferring non-empty values"""
        elem = game_elem.find(xml_tag)
        if elem is not None and elem.text and elem.text.strip():
            current_value = getattr(entry, field_name)
            new_value = elem.text.strip()
            
            # Only update if current is empty or new value is longer/better
            if not current_value or len(new_value) > len(current_value):
                setattr(entry, field_name, new_value)
                entry.data_sources[field_name] = source_name
                
                # Track media stats
                if field_name in self.MEDIA_FIELDS:
                    self.media_stats[source_name][field_name] += 1
    
    def standardize_media_paths(self, preferred_structure: str = 'retrobat') -> None:
        """
        Standardize media paths across all entries
        
        Args:
            preferred_structure: 'retrobat' (separate folders) or 'simple' (all in media/)
        """
        print(f"\n🎨 Standardizing media paths ({preferred_structure} structure)...")
        
        for rom_path, entry in self.games.items():
            rom_name = Path(rom_path).stem.replace('./', '')
            
            if preferred_structure == 'retrobat':
                # RetroBat style: separate folders for each media type
                if not entry.image:
                    entry.image = f"./media/mix/{rom_name}.png"
                if not entry.thumbnail:
                    entry.thumbnail = f"./media/box2dfront/{rom_name}.png"
                if not entry.marquee:
                    entry.marquee = f"./media/wheel/{rom_name}.png"
                if not entry.boxback:
                    entry.boxback = f"./media/box2dback/{rom_name}.png"
                if not entry.manual:
                    entry.manual = f"./media/manuals/{rom_name}.pdf"
                if not entry.video:
                    entry.video = f"./media/video/{rom_name}.mp4"
                if not entry.screenshot:
                    entry.screenshot = f"./media/screenshot/{rom_name}.png"
            else:
                # Simple structure: all media in subfolders
                if not entry.image:
                    entry.image = f"./media/images/{rom_name}.png"
                if not entry.thumbnail:
                    entry.thumbnail = f"./media/thumbnails/{rom_name}.png"
    
    def validate_media(self, base_path: Path, report_missing: bool = True) -> Dict[str, List[str]]:
        """
        Validate that media files actually exist
        
        Returns:
            Dictionary of missing files by media type
        """
        print(f"\n🔍 Validating media files in: {base_path}")
        
        missing = defaultdict(list)
        found_count = defaultdict(int)
        
        for rom_path, entry in self.games.items():
            for media_field in self.MEDIA_FIELDS:
                media_path = getattr(entry, media_field)
                if not media_path:
                    continue
                
                # Convert relative path to absolute
                full_path = base_path / media_path.lstrip('./')
                
                if full_path.exists():
                    found_count[media_field] += 1
                else:
                    missing[media_field].append(str(media_path))
        
        # Print summary
        print("\n📊 Media Validation Summary:")
        for media_type in sorted(self.MEDIA_FIELDS):
            total = sum(1 for e in self.games.values() if getattr(e, media_type))
            found = found_count[media_type]
            missing_count = len(missing[media_type])
            
            if total > 0:
                percent = (found / total) * 100
                status = "✓" if percent == 100 else "⚠" if percent > 50 else "❌"
                print(f"   {status} {media_type:12s}: {found:3d}/{total:3d} found ({percent:5.1f}%)")
        
        return dict(missing)
    
    def generate_unified_gamelist(self, output_path: Path, format_style: str = 'retrobat') -> None:
        """
        Generate a unified gamelist.xml file
        
        Args:
            output_path: Where to save the unified gamelist
            format_style: 'retrobat' (detailed) or 'simple' (minimal)
        """
        print(f"\n💾 Generating unified gamelist: {output_path}")
        
        root = ET.Element('gameList')
        
        # Add provider info if available
        if self.provider_info:
            provider = ET.SubElement(root, 'provider')
            for key, value in self.provider_info.items():
                elem = ET.SubElement(provider, key)
                elem.text = value
        
        # Add games in sorted order
        for rom_path in sorted(self.games.keys()):
            entry = self.games[rom_path]
            game = ET.SubElement(root, 'game')
            
            # Add ID and source attributes if available
            if entry.game_id:
                game.set('id', entry.game_id)
            if entry.source:
                game.set('source', entry.source)
            
            # Path (required)
            ET.SubElement(game, 'path').text = entry.path
            
            # Name (use <name> for standard ES compatibility, not <n>)
            if entry.name:
                ET.SubElement(game, 'name').text = entry.name
            
            # Metadata
            for field in ['desc', 'rating', 'releasedate', 'developer', 'publisher',
                         'genre', 'players']:
                value = getattr(entry, field)
                if value:
                    ET.SubElement(game, field).text = value
            
            # Technical metadata
            for field in ['hash', 'md5', 'genreid', 'lang', 'region']:
                value = getattr(entry, field)
                if value:
                    ET.SubElement(game, field).text = value
            
            # Media paths
            for media_field in sorted(self.MEDIA_FIELDS):
                value = getattr(entry, media_field)
                if value:
                    ET.SubElement(game, media_field).text = value
        
        # Write XML with pretty formatting
        self._prettify_and_save(root, output_path)
        print(f"   ✓ Saved {len(self.games)} games")
    
    def _prettify_and_save(self, elem: ET.Element, filepath: Path) -> None:
        """Save XML with proper indentation"""
        from xml.dom import minidom
        
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="\t")
        
        # Remove extra blank lines
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def generate_report(self, output_path: Path) -> None:
        """Generate a detailed report of the merge operation"""
        print(f"\n📋 Generating report: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("GAMELIST UNIFICATION REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Total Games: {len(self.games)}\n\n")
            
            # Media statistics by source
            f.write("MEDIA COVERAGE BY SOURCE:\n")
            f.write("-" * 80 + "\n")
            for source, stats in sorted(self.media_stats.items()):
                f.write(f"\n{source}:\n")
                for media_type, count in sorted(stats.items()):
                    f.write(f"  {media_type:12s}: {count:3d} files\n")
            
            # Games with incomplete data
            f.write("\n\nGAMES WITH INCOMPLETE METADATA:\n")
            f.write("-" * 80 + "\n")
            
            incomplete = []
            for rom_path, entry in sorted(self.games.items()):
                missing_fields = []
                if not entry.desc:
                    missing_fields.append('description')
                if not entry.developer:
                    missing_fields.append('developer')
                if not entry.releasedate:
                    missing_fields.append('release date')
                
                if missing_fields:
                    incomplete.append((entry.name or rom_path, missing_fields))
            
            if incomplete:
                for game_name, missing in incomplete[:20]:  # Show first 20
                    f.write(f"\n{game_name}:\n")
                    f.write(f"  Missing: {', '.join(missing)}\n")
                
                if len(incomplete) > 20:
                    f.write(f"\n... and {len(incomplete) - 20} more\n")
            else:
                f.write("All games have complete metadata!\n")
        
        print(f"   ✓ Report saved")

def main():
    """Main CLI interface"""
    print("=" * 80)
    print("GAMELIST UNIFIER - Merge and Standardize Your Emulation Gamelists")
    print("=" * 80)
    
    unifier = GameListUnifier()
    
    # Example usage - you'll customize this
    print("\nThis tool will:")
    print("  1. Parse multiple gamelist.xml files")
    print("  2. Merge data intelligently (prefer complete metadata)")
    print("  3. Standardize media paths")
    print("  4. Validate media file existence")
    print("  5. Generate unified gamelist.xml files")
    print("  6. Create a detailed report")
    
    print("\n" + "=" * 80)
    print("READY TO USE!")
    print("=" * 80)
    print("\nSee the example code at the bottom of this script to customize for your setup.")

if __name__ == "__main__":
    main()
