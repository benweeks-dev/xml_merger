#!/usr/bin/env python3
"""
Example usage script for GameList Unifier
Customize the paths below for your setup
"""

from pathlib import Path
from gamelist_unifier import GameListUnifier

def main():
    # Initialize the unifier
    unifier = GameListUnifier()
    
    # ========================================================================
    # STEP 1: Configure your paths
    # ========================================================================
    
    # Where are your ROM collections? Update these paths:
    PATHS = {
        'pc_backup': Path(r'D:\ROMs BackUp\ROMs - 1G1R'),   # Your PC backup
        'retrobat': Path(r'D:\RetroBat\roms'),              # RetroBat installation
        'retrodeck': Path(r''),                             # RetroDECK (if applicable)
        'miyoo': Path(r''),                                 # Miyoo Mini Plus SD card
    }
    
    # Which system are we processing? (e.g., 'ngp', 'n64', 'psx', 'snes')
    SYSTEM = 'ngp'  # NeoGeo Pocket example
    
    # Output location for unified gamelist
    OUTPUT_DIR = Path(r'D:\Unified_Gamelists')
    
    # ========================================================================
    # STEP 2: Parse all available gamelist.xml files for this system
    # ========================================================================
    
    print(f"\n🎮 Processing system: {SYSTEM}")
    print("=" * 80)
    
    # Try to find and parse gamelists from each source
    sources_found = 0
    
    for source_name, base_path in PATHS.items():
        gamelist_path = base_path / SYSTEM / 'gamelist.xml'
        
        if gamelist_path.exists():
            unifier.parse_gamelist(gamelist_path, source_name=source_name)
            sources_found += 1
        else:
            print(f"⚠ Skipping {source_name}: {gamelist_path} not found")
    
    if sources_found == 0:
        print("\n❌ No gamelist.xml files found! Check your paths.")
        return
    
    print(f"\n✓ Parsed {sources_found} gamelist files")
    print(f"✓ Found {len(unifier.games)} unique games")
    
    # ========================================================================
    # STEP 3: Standardize media paths
    # ========================================================================
    
    # Choose your preferred structure:
    # - 'retrobat': Separate folders (mix, wheel, box2dfront, etc.)
    # - 'simple': Unified structure (images, thumbnails, etc.)
    
    unifier.standardize_media_paths(preferred_structure='retrobat')
    
    # ========================================================================
    # STEP 4: Validate media files (optional but recommended)
    # ========================================================================
    
    # Which path should we check for media? Usually your main/master collection
    media_base_path = PATHS['retrobat'] / SYSTEM
    
    if media_base_path.exists():
        missing_media = unifier.validate_media(media_base_path, report_missing=True)
        
        # Optionally save missing media report
        if any(missing_media.values()):
            missing_report = OUTPUT_DIR / f'{SYSTEM}_missing_media.txt'
            with open(missing_report, 'w') as f:
                for media_type, files in missing_media.items():
                    if files:
                        f.write(f"\n{media_type.upper()} - {len(files)} missing:\n")
                        for filepath in sorted(files)[:10]:  # Show first 10
                            f.write(f"  {filepath}\n")
                        if len(files) > 10:
                            f.write(f"  ... and {len(files) - 10} more\n")
            print(f"\n💾 Missing media report: {missing_report}")
    
    # ========================================================================
    # STEP 5: Generate unified gamelist files
    # ========================================================================
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate the unified gamelist
    output_gamelist = OUTPUT_DIR / f'{SYSTEM}_unified_gamelist.xml'
    unifier.generate_unified_gamelist(output_gamelist, format_style='retrobat')
    
    # ========================================================================
    # STEP 6: Generate detailed report
    # ========================================================================
    
    report_path = OUTPUT_DIR / f'{SYSTEM}_unification_report.txt'
    unifier.generate_report(report_path)
    
    # ========================================================================
    # DONE!
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    print(f"\nOutput files in: {OUTPUT_DIR}")
    print(f"  📄 {output_gamelist.name}")
    print(f"  📋 {report_path.name}")
    if any(missing_media.values()):
        print(f"  ⚠ {SYSTEM}_missing_media.txt")
    
    print("\n💡 Next steps:")
    print("  1. Review the unified gamelist.xml")
    print("  2. Check the report for any data quality issues")
    print("  3. Copy the unified gamelist to each platform:")
    print(f"     - RetroBat:  {PATHS['retrobat'] / SYSTEM / 'gamelist.xml'}")
    print(f"     - Miyoo:     {PATHS['miyoo'] / SYSTEM / 'gamelist.xml'}")
    print("  4. Optional: Scrape missing media for incomplete entries")

if __name__ == "__main__":
    main()
