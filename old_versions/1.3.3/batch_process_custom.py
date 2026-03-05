#!/usr/bin/env python3
"""
Custom Batch Processor for Ben's Setup
Handles PC backup's manufacturer structure with Arcade/NeoGeo exceptions
Auto-discovers RetroBat systems and matches them to PC backup
"""

from pathlib import Path
from gamelist_unifier import GameListUnifier
import sys

# Mapping of RetroBat system names to PC backup folder paths
# This handles the manufacturer folder structure
SYSTEM_MAPPING = {
    # SNK Systems
    'ngp': 'SNK\\NeoGeo Pocket',
    'ngpc': 'SNK\\NeoGeo Pocket Color',
    'neogeo': 'NeoGeo',  # Exception: no manufacturer folder
    
    # Nintendo Systems
    'n64': 'Nintendo\\Nintendo 64',
    'snes': 'Nintendo\\Super Nintendo',
    'nes': 'Nintendo\\Nintendo Entertainment System',
    'gb': 'Nintendo\\Game Boy',
    'gbc': 'Nintendo\\Game Boy Color',
    'gba': 'Nintendo\\Game Boy Advance',
    'nds': 'Nintendo\\Nintendo DS',
    'gamecube': 'Nintendo\\GameCube',
    'wii': 'Nintendo\\Wii',
    'wiiu': 'Nintendo\\Wii U',
    'switch': 'Nintendo\\Switch',
    
    # Sony Systems
    'psx': 'Sony\\PlayStation',
    'ps2': 'Sony\\PlayStation 2',
    'psp': 'Sony\\PlayStation Portable',
    
    # Sega Systems
    'genesis': 'Sega\\Genesis',
    'megadrive': 'Sega\\Mega Drive',
    'mastersystem': 'Sega\\Master System',
    'gamegear': 'Sega\\Game Gear',
    'saturn': 'Sega\\Saturn',
    'dreamcast': 'Sega\\Dreamcast',
    'segacd': 'Sega\\Sega CD',
    'sega32x': 'Sega\\32X',
    
    # Atari Systems
    'atari2600': 'Atari\\Atari 2600',
    'atari5200': 'Atari\\Atari 5200',
    'atari7800': 'Atari\\Atari 7800',
    'atarijaguar': 'Atari\\Jaguar',
    'atarilynx': 'Atari\\Lynx',
    
    # NEC Systems
    'pcengine': 'NEC\\PC Engine',
    'pcenginecd': 'NEC\\PC Engine CD',
    'tg16': 'NEC\\TurboGrafx-16',
    
    # Arcade - Exception: no manufacturer folder
    'arcade': 'Arcade',
    'mame': 'Arcade\\MAME',
    'fbneo': 'Arcade\\FBNeo',
    'naomi': 'Arcade\\Naomi',
    
    # Other manufacturers
    '3do': '3DO\\3DO',
    'colecovision': 'Coleco\\ColecoVision',
    'intellivision': 'Mattel\\Intellivision',
    'wonderswan': 'Bandai\\WonderSwan',
    'wonderswancolor': 'Bandai\\WonderSwan Color',
}

def find_pc_backup_path(system_name: str, pc_backup_base: Path) -> Path:
    """
    Find the PC backup folder for a given RetroBat system
    Handles manufacturer folder structure and exceptions
    """
    # Check if we have a known mapping
    if system_name in SYSTEM_MAPPING:
        relative_path = SYSTEM_MAPPING[system_name]
        full_path = pc_backup_base / relative_path
        if full_path.exists():
            return full_path
    
    # Try to find it by searching
    # Check direct folders (for exceptions like Arcade, NeoGeo)
    direct_path = pc_backup_base / system_name.title()
    if direct_path.exists():
        return direct_path
    
    # Search manufacturer folders
    for manufacturer_folder in pc_backup_base.iterdir():
        if manufacturer_folder.is_dir() and not manufacturer_folder.name.startswith('.'):
            # Look for system folder inside
            for system_folder in manufacturer_folder.iterdir():
                if system_folder.is_dir() and system_folder.name.lower().replace(' ', '') == system_name.lower():
                    return system_folder
    
    return None

def process_all_systems():
    """Process all systems found in RetroBat"""
    
    # ========================================================================
    # CONFIGURE YOUR PATHS
    # ========================================================================
    
    PC_BACKUP_BASE = Path(r'D:\ROMs BackUp\ROMs - 1G1R')
    RETROBAT_BASE = Path(r'D:\RetroBat\roms')
    OUTPUT_DIR = Path(r'D:\Unified_Gamelists')
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("BATCH GAMELIST UNIFIER - BEN'S CUSTOM VERSION")
    print("=" * 80)
    print(f"\nPC Backup Base: {PC_BACKUP_BASE}")
    print(f"RetroBat Base:  {RETROBAT_BASE}")
    print(f"Output Dir:     {OUTPUT_DIR}")
    
    # ========================================================================
    # VERIFY BASE PATHS
    # ========================================================================
    
    if not PC_BACKUP_BASE.exists():
        print(f"\n❌ ERROR: PC backup path not found: {PC_BACKUP_BASE}")
        return
    
    if not RETROBAT_BASE.exists():
        print(f"\n❌ ERROR: RetroBat path not found: {RETROBAT_BASE}")
        return
    
    # ========================================================================
    # DISCOVER RETROBAT SYSTEMS
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("DISCOVERING RETROBAT SYSTEMS")
    print("=" * 80)
    
    retrobat_systems = []
    for item in RETROBAT_BASE.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            gamelist = item / 'gamelist.xml'
            if gamelist.exists():
                retrobat_systems.append(item.name)
    
    retrobat_systems.sort()
    
    if not retrobat_systems:
        print("\n❌ No systems with gamelist.xml found in RetroBat!")
        return
    
    print(f"\n✓ Found {len(retrobat_systems)} RetroBat systems with gamelists:")
    for i, system in enumerate(retrobat_systems, 1):
        print(f"   {i:2d}. {system}")
    
    # ========================================================================
    # MATCH WITH PC BACKUP
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("MATCHING WITH PC BACKUP")
    print("=" * 80)
    
    systems_to_process = []
    
    for system in retrobat_systems:
        retrobat_gamelist = RETROBAT_BASE / system / 'gamelist.xml'
        pc_backup_path = find_pc_backup_path(system, PC_BACKUP_BASE)
        
        if pc_backup_path:
            pc_backup_gamelist = pc_backup_path / 'media' / 'gamelist.xml'
            
            if pc_backup_gamelist.exists():
                print(f"\n✓ {system}")
                print(f"  RetroBat: {retrobat_gamelist}")
                print(f"  PC Backup: {pc_backup_gamelist}")
                
                systems_to_process.append({
                    'system': system,
                    'retrobat_gamelist': retrobat_gamelist,
                    'retrobat_base': RETROBAT_BASE / system,
                    'pc_backup_gamelist': pc_backup_gamelist,
                    'pc_backup_base': pc_backup_path,
                })
            else:
                print(f"\n⚠ {system}: PC backup path found but no gamelist.xml")
                print(f"  Expected: {pc_backup_gamelist}")
                # Still process RetroBat only
                systems_to_process.append({
                    'system': system,
                    'retrobat_gamelist': retrobat_gamelist,
                    'retrobat_base': RETROBAT_BASE / system,
                    'pc_backup_gamelist': None,
                    'pc_backup_base': None,
                })
        else:
            # Couldn't find PC backup folder automatically
            print(f"\n❓ {system}: PC backup folder not found automatically")
            print(f"  RetroBat: {retrobat_gamelist}")
            
            # Prompt user for manual path
            response = input(f"  Enter PC backup path for {system} (or press Enter to skip): ").strip()
            
            if response:
                # User provided a path
                manual_path = Path(response)
                
                if manual_path.exists():
                    # Check if gamelist.xml is in the path provided
                    if (manual_path / 'gamelist.xml').exists():
                        # User gave us the direct folder with gamelist.xml
                        pc_backup_gamelist = manual_path / 'gamelist.xml'
                        pc_backup_base = manual_path.parent if manual_path.name == 'media' else manual_path
                    elif (manual_path / 'media' / 'gamelist.xml').exists():
                        # User gave us the system folder, gamelist is in media subfolder
                        pc_backup_gamelist = manual_path / 'media' / 'gamelist.xml'
                        pc_backup_base = manual_path
                    else:
                        print(f"  ⚠ No gamelist.xml found at provided path, using RetroBat only")
                        pc_backup_gamelist = None
                        pc_backup_base = None
                    
                    if pc_backup_gamelist:
                        print(f"  ✓ Found: {pc_backup_gamelist}")
                        systems_to_process.append({
                            'system': system,
                            'retrobat_gamelist': retrobat_gamelist,
                            'retrobat_base': RETROBAT_BASE / system,
                            'pc_backup_gamelist': pc_backup_gamelist,
                            'pc_backup_base': pc_backup_base,
                        })
                    else:
                        systems_to_process.append({
                            'system': system,
                            'retrobat_gamelist': retrobat_gamelist,
                            'retrobat_base': RETROBAT_BASE / system,
                            'pc_backup_gamelist': None,
                            'pc_backup_base': None,
                        })
                else:
                    print(f"  ⚠ Path does not exist: {manual_path}")
                    print(f"  Using RetroBat only")
                    systems_to_process.append({
                        'system': system,
                        'retrobat_gamelist': retrobat_gamelist,
                        'retrobat_base': RETROBAT_BASE / system,
                        'pc_backup_gamelist': None,
                        'pc_backup_base': None,
                    })
            else:
                # User pressed Enter to skip
                print(f"  → Using RetroBat only")
                systems_to_process.append({
                    'system': system,
                    'retrobat_gamelist': retrobat_gamelist,
                    'retrobat_base': RETROBAT_BASE / system,
                    'pc_backup_gamelist': None,
                    'pc_backup_base': None,
                })
    
    if not systems_to_process:
        print("\n❌ No systems to process!")
        return
    
    # ========================================================================
    # PROCESS EACH SYSTEM
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("PROCESSING SYSTEMS")
    print("=" * 80)
    
    results = {}
    
    for idx, system_info in enumerate(systems_to_process, 1):
        system = system_info['system']
        
        print(f"\n[{idx}/{len(systems_to_process)}] Processing: {system}")
        print("-" * 80)
        
        try:
            # Create unifier with name cleaning enabled
            unifier = GameListUnifier(clean_names=True)
            sources_found = 0
            
            # Parse RetroBat gamelist
            print(f"   📖 Parsing RetroBat gamelist...")
            unifier.parse_gamelist(system_info['retrobat_gamelist'], source_name='RetroBat')
            sources_found += 1
            
            # Parse PC backup gamelist if it exists
            if system_info['pc_backup_gamelist']:
                print(f"   📖 Parsing PC backup gamelist...")
                unifier.parse_gamelist(system_info['pc_backup_gamelist'], source_name='PC Backup')
                sources_found += 1
            
            if len(unifier.games) == 0:
                print(f"   ⚠ No games found")
                results[system] = {'status': 'skipped', 'reason': 'no games'}
                continue
            
            print(f"   ✓ Found {len(unifier.games)} unique games from {sources_found} source(s)")
            
            # Standardize media paths
            print(f"   🎨 Standardizing media paths...")
            unifier.standardize_media_paths(preferred_structure='retrobat')
            
            # Generate unified gamelist
            output_gamelist = OUTPUT_DIR / f'{system}_unified_gamelist.xml'
            print(f"   💾 Generating unified gamelist...")
            unifier.generate_unified_gamelist(output_gamelist, format_style='retrobat', include_empty_tags=True)
            
            # Generate report
            report_path = OUTPUT_DIR / f'{system}_report.txt'
            unifier.generate_report(report_path)
            
            # Generate comparison report
            comparison_path = OUTPUT_DIR / f'{system}_source_comparison.txt'
            with open(comparison_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"SOURCE COMPARISON - {system.upper()}\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Total Games: {len(unifier.games)}\n")
                f.write(f"Sources: {sources_found}\n\n")
                
                f.write("DATA SOURCE ATTRIBUTION:\n")
                f.write("-" * 80 + "\n\n")
                
                for rom_path, entry in sorted(unifier.games.items())[:20]:  # First 20
                    f.write(f"\n{entry.name or rom_path}:\n")
                    if entry.data_sources:
                        for field, source in sorted(entry.data_sources.items()):
                            f.write(f"  {field:12s}: {source}\n")
                
                if len(unifier.games) > 20:
                    f.write(f"\n... and {len(unifier.games) - 20} more games\n")
            
            # Validate media (using RetroBat as primary)
            print(f"   🔍 Validating media files...")
            missing_media = unifier.validate_media(system_info['retrobat_base'], report_missing=False)
            
            if any(missing_media.values()):
                missing_report = OUTPUT_DIR / f'{system}_missing_media.txt'
                with open(missing_report, 'w') as f:
                    f.write(f"Missing Media Report - {system}\n")
                    f.write(f"Base Path: {system_info['retrobat_base']}\n")
                    f.write("=" * 80 + "\n\n")
                    for media_type, files in missing_media.items():
                        if files:
                            f.write(f"\n{media_type.upper()} - {len(files)} missing:\n")
                            for filepath in sorted(files):
                                f.write(f"  {filepath}\n")
            
            results[system] = {
                'status': 'success',
                'games': len(unifier.games),
                'sources': sources_found
            }
            
            print(f"   ✅ Complete!")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
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
            print(f"   • {system:20s} - {info['games']:3d} games, {info['sources']} source(s)")
    
    if failed:
        print(f"\n❌ Failed systems:")
        for system in failed:
            print(f"   • {system:20s} - {results[system]['error']}")
    
    print(f"\n💾 Output directory: {OUTPUT_DIR}")
    print(f"   📁 {len(successful)} unified gamelist.xml files")
    print(f"   📁 {len(successful)} reports")
    print(f"   📁 {len(successful)} source comparisons")
    
    # ========================================================================
    # GENERATE MASTER INDEX
    # ========================================================================
    
    index_path = OUTPUT_DIR / '_MASTER_INDEX.txt'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("GAMELIST UNIFICATION - MASTER INDEX\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"PC Backup Base: {PC_BACKUP_BASE}\n")
        f.write(f"RetroBat Base:  {RETROBAT_BASE}\n")
        f.write(f"Output Dir:     {OUTPUT_DIR}\n\n")
        f.write(f"Total Systems:  {len(systems_to_process)}\n")
        f.write(f"Successful:     {len(successful)}\n")
        f.write(f"Failed:         {len(failed)}\n")
        f.write(f"Skipped:        {len(skipped)}\n\n")
        
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
                f.write(f"    • {system}_source_comparison.txt\n")
            elif info['status'] == 'error':
                f.write(f"  Error: {info['error']}\n")
            f.write("\n")
    
    print(f"\n📋 Master index: {index_path}")
    
    print("\n" + "=" * 80)
    print("✅ ALL DONE!")
    print("=" * 80)
    print("\n💡 Next steps:")
    print("  1. Review the unified gamelists in the output directory")
    print("  2. Check individual system reports for data quality")
    print("  3. Review source comparisons to see which data came from where")
    print("  4. Back up your current gamelists!")
    print("  5. Deploy unified gamelists to RetroBat/PC backup")
    print("\n⚠  IMPORTANT: Make backups before overwriting production gamelists!")

if __name__ == "__main__":
    process_all_systems()
