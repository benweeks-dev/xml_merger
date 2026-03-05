#!/usr/bin/env python3
"""
Deploy Unified Gamelists
Copies *_unified_gamelist.xml files to their respective folders
Keeps original gamelist.xml files intact (you can rename/remove them later)
"""

from pathlib import Path
import shutil

# Same system mapping as batch processor
SYSTEM_MAPPING = {
    # SNK Systems
    'ngp': 'SNK\\NeoGeo Pocket',
    'ngpc': 'SNK\\NeoGeo Pocket Color',
    'neogeo': 'NeoGeo',
    
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
    
    # Arcade
    'arcade': 'Arcade',
    'mame': 'Arcade\\MAME',
    'fbneo': 'Arcade\\FBNeo',
    'naomi': 'Arcade\\Naomi',
    
    # Other
    '3do': '3DO\\3DO',
    'colecovision': 'Coleco\\ColecoVision',
    'intellivision': 'Mattel\\Intellivision',
    'wonderswan': 'Bandai\\WonderSwan',
    'wonderswancolor': 'Bandai\\WonderSwan Color',
}

def find_pc_backup_path(system_name: str, pc_backup_base: Path) -> Path:
    """Find the PC backup folder for a given system"""
    if system_name in SYSTEM_MAPPING:
        relative_path = SYSTEM_MAPPING[system_name]
        full_path = pc_backup_base / relative_path
        if full_path.exists():
            return full_path
    
    # Try direct folder
    direct_path = pc_backup_base / system_name.title()
    if direct_path.exists():
        return direct_path
    
    # Search manufacturer folders
    for manufacturer_folder in pc_backup_base.iterdir():
        if manufacturer_folder.is_dir() and not manufacturer_folder.name.startswith('.'):
            for system_folder in manufacturer_folder.iterdir():
                if system_folder.is_dir() and system_folder.name.lower().replace(' ', '') == system_name.lower():
                    return system_folder
    
    return None

def load_paths_from_master_index(unified_dir: Path) -> dict:
    """
    Load PC backup paths from the master index file
    Returns dict: {system_name: pc_backup_path}
    """
    master_index = unified_dir / '_MASTER_INDEX.txt'
    paths = {}
    
    if not master_index.exists():
        return paths
    
    try:
        with open(master_index, 'r', encoding='utf-8') as f:
            current_system = None
            for line in f:
                line = line.rstrip()

                # Look for system headers (e.g., "NGP:")
                if line and line.endswith(':') and not line.startswith(' '):
                    current_system = line[:-1].lower()
                
                # Look for PC Backup path lines
                if current_system and 'PC Backup:' in line and 'Not configured' not in line:
                    # Extract path after "PC Backup:"
                    parts = line.split('PC Backup:', 1)
                    if len(parts) == 2:
                        path_str = parts[1].strip()
                        if path_str and path_str != 'Not configured':
                            paths[current_system] = Path(path_str)
                    current_system = None
        
        print(f"\n📋 Loaded {len(paths)} PC backup paths from master index")
        for system, path in paths.items():
            print(f"   • {system}: {path}")
    
    except Exception as e:
        print(f"\n⚠ Warning: Could not read master index: {e}")
    
    return paths

def deploy_unified_gamelists():
    """Deploy unified gamelists to PC backup and RetroBat folders"""
    
    # ========================================================================
    # CONFIGURE YOUR PATHS
    # ========================================================================
    
    PC_BACKUP_BASE = Path(r'D:\ROMs BackUp\ROMs - 1G1R')
    RETROBAT_BASE = Path(r'D:\RetroBat\roms')
    UNIFIED_DIR = Path(r'D:\Unified_Gamelists')
    
    print("=" * 80)
    print("DEPLOY UNIFIED GAMELISTS")
    print("=" * 80)
    print(f"\nSource:      {UNIFIED_DIR}")
    print(f"PC Backup:   {PC_BACKUP_BASE}")
    print(f"RetroBat:    {RETROBAT_BASE}")
    
    # ========================================================================
    # VERIFY PATHS
    # ========================================================================
    
    if not UNIFIED_DIR.exists():
        print(f"\n❌ ERROR: Unified gamelists directory not found: {UNIFIED_DIR}")
        return
    
    if not PC_BACKUP_BASE.exists():
        print(f"\n⚠ WARNING: PC backup path not found: {PC_BACKUP_BASE}")
        print("Will skip PC backup deployment")
        pc_backup_available = False
    else:
        pc_backup_available = True
    
    if not RETROBAT_BASE.exists():
        print(f"\n⚠ WARNING: RetroBat path not found: {RETROBAT_BASE}")
        print("Will skip RetroBat deployment")
        retrobat_available = False
    else:
        retrobat_available = True
    
    if not pc_backup_available and not retrobat_available:
        print("\n❌ ERROR: Neither PC backup nor RetroBat paths are available!")
        return
    
    # ========================================================================
    # FIND UNIFIED GAMELISTS & MATCH TO DESTINATIONS
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("DISCOVERING UNIFIED GAMELISTS")
    print("=" * 80)
    
    unified_files = list(UNIFIED_DIR.glob('*_unified_gamelist.xml'))
    
    if not unified_files:
        print(f"\n❌ No unified gamelist files found in {UNIFIED_DIR}")
        print("Expected files like: ngp_unified_gamelist.xml, n64_unified_gamelist.xml, etc.")
        return
    
    print(f"\n✓ Found {len(unified_files)} unified gamelists")
    
    # Load PC backup paths from master index
    master_index_paths = load_paths_from_master_index(UNIFIED_DIR)
    
    deployment_plan = []
    
    for file in unified_files:
        system = file.stem.replace('_unified_gamelist', '')
        print(f"\n📦 {system}")
        
        source_file = file
        destinations = []
        
        # Find RetroBat destination
        if retrobat_available:
            retrobat_dest = RETROBAT_BASE / system
            if retrobat_dest.exists():
                destinations.append({
                    'location': 'RetroBat',
                    'path': retrobat_dest / f'{system}_unified_gamelist.xml'
                })
                print(f"   ✓ RetroBat: {retrobat_dest}")
            else:
                print(f"   ⚠ RetroBat: System folder not found")
        
        # Find PC Backup destination
        if pc_backup_available:
            pc_backup_path = None
            
            # 1. First check master index
            if system in master_index_paths:
                pc_backup_path = master_index_paths[system]
                if pc_backup_path.exists():
                    print(f"   ✓ PC Backup: {pc_backup_path} (from master index)")
                else:
                    print(f"   ⚠ PC Backup: Path from master index not found: {pc_backup_path}")
                    pc_backup_path = None
            
            # 2. Try auto-detection if not in master index
            if not pc_backup_path:
                pc_backup_path = find_pc_backup_path(system, PC_BACKUP_BASE)
                if pc_backup_path:
                    print(f"   ✓ PC Backup: {pc_backup_path} (auto-detected)")
            
            # 3. If still not found, prompt user
            if pc_backup_path:
                pc_dest = pc_backup_path / 'media' / f'{system}_unified_gamelist.xml'
                destinations.append({
                    'location': 'PC Backup',
                    'path': pc_dest
                })
            else:
                # Couldn't find, prompt user
                print(f"   ❓ PC Backup: Not found in master index or auto-detection")
                response = input(f"      Enter PC backup path for {system} (or press Enter to skip): ").strip()
                
                if response:
                    manual_path = Path(response)
                    
                    if manual_path.exists():
                        # Determine where to put the gamelist
                        if (manual_path / 'media').exists():
                            # System folder provided
                            pc_dest = manual_path / 'media' / f'{system}_unified_gamelist.xml'
                        elif manual_path.name == 'media':
                            # Media folder provided
                            pc_dest = manual_path / f'{system}_unified_gamelist.xml'
                        else:
                            # Assume system folder, create media if needed
                            pc_dest = manual_path / 'media' / f'{system}_unified_gamelist.xml'
                        
                        destinations.append({
                            'location': 'PC Backup',
                            'path': pc_dest
                        })
                        print(f"      ✓ Will deploy to: {pc_dest}")
                    else:
                        print(f"      ⚠ Path does not exist, skipping PC backup for {system}")
                else:
                    print(f"      → Skipping PC backup for {system}")
        
        if destinations:
            deployment_plan.append({
                'system': system,
                'source': source_file,
                'destinations': destinations
            })
        else:
            print(f"   ⚠ No valid destinations found for {system}")
    
    if not deployment_plan:
        print("\n❌ No systems have valid deployment destinations!")
        return
    
    # ========================================================================
    # CONFIRM DEPLOYMENT
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("⚠  DEPLOYMENT PLAN")
    print("=" * 80)
    
    print(f"\nReady to deploy {len(deployment_plan)} systems:")
    for plan in deployment_plan:
        print(f"\n  {plan['system']}:")
        for dest in plan['destinations']:
            print(f"    → {dest['location']}: {dest['path'].parent}")
    
    print("\nThis will copy unified gamelists as '[system]_unified_gamelist.xml'")
    print("Your original 'gamelist.xml' files will NOT be modified or deleted.")
    print("\nYou can manually rename them later:")
    print("  1. Backup: Rename 'gamelist.xml' → 'gamelist_original.xml'")
    print("  2. Deploy: Rename '[system]_unified_gamelist.xml' → 'gamelist.xml'")
    
    response = input("\n📋 Proceed with deployment? (yes/no): ").lower().strip()
    if response != 'yes':
        print("\n❌ Deployment cancelled.")
        return
    
    # ========================================================================
    # DEPLOY TO EACH SYSTEM
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("DEPLOYING UNIFIED GAMELISTS")
    print("=" * 80)
    
    deployment_log = []
    
    for plan in deployment_plan:
        system = plan['system']
        source_file = plan['source']
        
        print(f"\n📦 Deploying: {system}")
        print("-" * 80)
        
        for dest in plan['destinations']:
            dest_file = dest['path']
            location = dest['location']
            
            try:
                # Create destination directory if needed
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy the file
                shutil.copy2(source_file, dest_file)
                print(f"   ✓ {location}: {dest_file}")
                deployment_log.append(f"✓ {system} → {location}: {dest_file}")
            except Exception as e:
                print(f"   ❌ {location}: Error - {e}")
                deployment_log.append(f"❌ {system} → {location}: {e}")
    
    # ========================================================================
    # SAVE DEPLOYMENT LOG
    # ========================================================================
    
    log_file = UNIFIED_DIR / '_DEPLOYMENT_LOG.txt'
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("UNIFIED GAMELIST DEPLOYMENT LOG\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Source:      {UNIFIED_DIR}\n")
        f.write(f"PC Backup:   {PC_BACKUP_BASE}\n")
        f.write(f"RetroBat:    {RETROBAT_BASE}\n\n")
        f.write("DEPLOYMENTS:\n")
        f.write("-" * 80 + "\n\n")
        for entry in deployment_log:
            f.write(entry + "\n")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("✅ DEPLOYMENT COMPLETE!")
    print("=" * 80)
    
    successful = [line for line in deployment_log if line.startswith('✓')]
    failed = [line for line in deployment_log if line.startswith('❌')]
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Successful: {len(successful)}")
    print(f"   ❌ Failed:     {len(failed)}")
    
    print(f"\n📋 Deployment log: {log_file}")
    
    print("\n" + "=" * 80)
    print("⚠  NEXT STEPS - MANUAL ACTIVATION")
    print("=" * 80)
    print("\nYour unified gamelists have been copied but NOT activated yet.")
    print("The original 'gamelist.xml' files are still in use.")
    print("\nTo activate the unified gamelists, for each system:")
    print("\n  1. BACKUP (rename):")
    print("     gamelist.xml → gamelist_original.xml")
    print("\n  2. ACTIVATE (rename):")
    print("     [system]_unified_gamelist.xml → gamelist.xml")
    print("\nExample for NGP in RetroBat:")
    print("  D:\\RetroBat\\roms\\ngp\\")
    print("    gamelist.xml → gamelist_original.xml")
    print("    ngp_unified_gamelist.xml → gamelist.xml")
    print("\nExample for NGP in PC Backup:")
    print("  D:\\ROMs BackUp\\ROMs - 1G1R\\SNK\\NeoGeo Pocket\\media\\")
    print("    gamelist.xml → gamelist_original.xml")
    print("    ngp_unified_gamelist.xml → gamelist.xml")
    print("\n💡 TIP: Test with one system (like NGP) before activating all!")

if __name__ == "__main__":
    deploy_unified_gamelists()
