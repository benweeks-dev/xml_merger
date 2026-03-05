#!/usr/bin/env python3
"""
Batch process ALL systems across all platforms
Run this to unify gamelists for every system you have
"""

from pathlib import Path
from gamelist_unifier import GameListUnifier
import sys

def process_all_systems():
    """Process all systems found across all platforms"""
    
    # ========================================================================
    # CONFIGURE YOUR PATHS HERE
    # ========================================================================
    
    PLATFORMS = {
        'pc_backup': Path(r'D:\Backups\Emulation\roms'),
        'retrobat': Path(r'C:\RetroBat\roms'),
        'miyoo': Path(r'E:\Miyoo\roms'),
        # Add more as needed:
        # 'retrodeck': Path(r'/path/to/retrodeck/roms'),
    }
    
    OUTPUT_DIR = Path(r'D:\Unified_Gamelists')
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # ========================================================================
    # DISCOVER ALL SYSTEMS
    # ========================================================================
    
    print("=" * 80)
    print("BATCH GAMELIST UNIFIER")
    print("=" * 80)
    print("\n🔍 Discovering systems across platforms...")
    
    # Find all unique systems
    systems_found = set()
    
    for platform_name, platform_path in PLATFORMS.items():
        if not platform_path.exists():
            print(f"⚠ Warning: {platform_name} path not found: {platform_path}")
            continue
        
        # Look for directories containing gamelist.xml
        for item in platform_path.iterdir():
            if item.is_dir():
                gamelist = item / 'gamelist.xml'
                if gamelist.exists():
                    systems_found.add(item.name)
    
    systems_list = sorted(systems_found)
    
    if not systems_list:
        print("\n❌ No systems with gamelist.xml files found!")
        print("Check your platform paths.")
        return
    
    print(f"\n✓ Found {len(systems_list)} systems:")
    for i, system in enumerate(systems_list, 1):
        print(f"   {i:2d}. {system}")
    
    # ========================================================================
    # PROCESS EACH SYSTEM
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("PROCESSING SYSTEMS")
    print("=" * 80)
    
    results = {}
    
    for system_num, system in enumerate(systems_list, 1):
        print(f"\n[{system_num}/{len(systems_list)}] Processing: {system}")
        print("-" * 80)
        
        try:
            # Create unifier for this system
            unifier = GameListUnifier()
            sources_found = 0
            
            # Parse gamelists from all platforms
            for platform_name, platform_path in PLATFORMS.items():
                gamelist_path = platform_path / system / 'gamelist.xml'
                
                if gamelist_path.exists():
                    unifier.parse_gamelist(gamelist_path, source_name=platform_name)
                    sources_found += 1
            
            if sources_found == 0:
                print(f"   ⚠ No gamelists found for {system}")
                results[system] = {'status': 'skipped', 'reason': 'no gamelists'}
                continue
            
            # Standardize media paths
            unifier.standardize_media_paths(preferred_structure='retrobat')
            
            # Generate unified gamelist
            output_gamelist = OUTPUT_DIR / f'{system}_unified_gamelist.xml'
            unifier.generate_unified_gamelist(output_gamelist, format_style='retrobat')
            
            # Generate report
            report_path = OUTPUT_DIR / f'{system}_report.txt'
            unifier.generate_report(report_path)
            
            # Validate media (using first available platform path)
            validated = False
            for platform_name, platform_path in PLATFORMS.items():
                media_path = platform_path / system
                if media_path.exists():
                    missing_media = unifier.validate_media(media_path, report_missing=False)
                    
                    # Save missing media report if any
                    if any(missing_media.values()):
                        missing_report = OUTPUT_DIR / f'{system}_missing_media.txt'
                        with open(missing_report, 'w') as f:
                            f.write(f"Missing media report for: {system}\n")
                            f.write(f"Base path: {media_path}\n")
                            f.write("=" * 80 + "\n\n")
                            for media_type, files in missing_media.items():
                                if files:
                                    f.write(f"\n{media_type.upper()} - {len(files)} missing:\n")
                                    for filepath in sorted(files):
                                        f.write(f"  {filepath}\n")
                    
                    validated = True
                    break
            
            results[system] = {
                'status': 'success',
                'games': len(unifier.games),
                'sources': sources_found,
                'validated': validated
            }
            
            print(f"   ✅ Success: {len(unifier.games)} games from {sources_found} sources")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[system] = {'status': 'error', 'error': str(e)}
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 80)
    
    successful = [s for s, r in results.items() if r['status'] == 'success']
    failed = [s for s, r in results.items() if r['status'] == 'error']
    skipped = [s for s, r in results.items() if r['status'] == 'skipped']
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Successful: {len(successful)}")
    print(f"   ❌ Failed:     {len(failed)}")
    print(f"   ⚠  Skipped:    {len(skipped)}")
    
    if successful:
        print(f"\n✅ Successfully processed systems:")
        for system in successful:
            info = results[system]
            print(f"   • {system:20s} - {info['games']:3d} games, "
                  f"{info['sources']} sources")
    
    if failed:
        print(f"\n❌ Failed systems:")
        for system in failed:
            print(f"   • {system:20s} - {results[system]['error']}")
    
    print(f"\n💾 Output directory: {OUTPUT_DIR}")
    print(f"   📁 {len(successful)} unified gamelist.xml files")
    print(f"   📁 {len(successful)} reports")
    
    # ========================================================================
    # GENERATE MASTER INDEX
    # ========================================================================
    
    index_path = OUTPUT_DIR / '_INDEX.txt'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("GAMELIST UNIFICATION INDEX\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Systems: {len(systems_list)}\n")
        f.write(f"Successful:    {len(successful)}\n")
        f.write(f"Failed:        {len(failed)}\n")
        f.write(f"Skipped:       {len(skipped)}\n\n")
        
        f.write("SYSTEM DETAILS:\n")
        f.write("-" * 80 + "\n\n")
        
        for system in sorted(results.keys()):
            info = results[system]
            f.write(f"{system}:\n")
            f.write(f"  Status: {info['status']}\n")
            if info['status'] == 'success':
                f.write(f"  Games:  {info['games']}\n")
                f.write(f"  Sources: {info['sources']}\n")
                f.write(f"  Files:\n")
                f.write(f"    • {system}_unified_gamelist.xml\n")
                f.write(f"    • {system}_report.txt\n")
            elif info['status'] == 'error':
                f.write(f"  Error: {info['error']}\n")
            f.write("\n")
    
    print(f"\n📋 Index file created: {index_path}")
    
    print("\n💡 Next steps:")
    print("  1. Review the unified gamelists in the output directory")
    print("  2. Check individual system reports for data quality")
    print("  3. Deploy unified gamelists to each platform")
    print("  4. Consider scraping missing media for incomplete entries")


def deploy_gamelists():
    """
    Helper function to deploy unified gamelists back to platforms
    Run this after reviewing the unified gamelists
    """
    print("=" * 80)
    print("DEPLOY UNIFIED GAMELISTS")
    print("=" * 80)
    print("\n⚠ WARNING: This will overwrite existing gamelist.xml files!")
    print("Make sure you have backups!\n")
    
    response = input("Continue? (yes/no): ").lower().strip()
    if response != 'yes':
        print("Aborted.")
        return
    
    # TODO: Implement deployment logic
    print("\n💡 Deployment function not yet implemented.")
    print("For now, manually copy unified gamelists to:")
    print("  • RetroBat: C:\\RetroBat\\roms\\[system]\\gamelist.xml")
    print("  • Miyoo:    E:\\Miyoo\\roms\\[system]\\gamelist.xml")
    print("  • etc.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'deploy':
        deploy_gamelists()
    else:
        process_all_systems()
