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

def deploy_unified_gamelists():
    """Change RetroBat xml file names"""
    
    # ========================================================================
    # CONFIGURE YOUR PATHS
    # ========================================================================
    
    RETROBAT_BASE = Path(r'D:\RetroBat\roms')
    UNIFIED_DIR = Path(r'D:\Unified_Gamelists')
    
    print("=" * 80)
    print("RENAME GAMELISTS")
    print("=" * 80)
    print(f"\nSource:      {UNIFIED_DIR}")
    print(f"RetroBat:    {RETROBAT_BASE}")
    
    # ========================================================================
    # VERIFY PATHS
    # ========================================================================
    
    if not UNIFIED_DIR.exists():
        print(f"\n❌ ERROR: Unified gamelists directory not found: {UNIFIED_DIR}")
        return
    
    if not RETROBAT_BASE.exists():
        print(f"\n⚠ WARNING: RetroBat path not found: {RETROBAT_BASE}")
        print("Will skip RetroBat deployment")
        retrobat_available = False
    else:
        retrobat_available = True
    
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
   
    deployment_plan = []
    
    for file in unified_files:
        system = file.stem.replace('_unified_gamelist', '')
        print(f"\n📦 {system}")
        
        new_file = RETROBAT_BASE / system / f'{system}_unified_gamelist.xml'
        old_file = RETROBAT_BASE / system / 'gamelist.xml'
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
        
        if destinations:
            deployment_plan.append({
                'system': system,
                'new': new_file,
                'old': old_file,
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
    
    print("\nThis will rename gamelists as '[system]_unified_gamelist.xml'")
    print("Your original 'gamelist.xml' files will be modified to 'gamelist_BACKUP'")
    
    response = input("\n📋 Proceed with deployment? (yes/no): ").lower().strip()
    if response != 'yes':
        print("\n❌ Deployment cancelled.")
        return
    
    # ========================================================================
    # DEPLOY TO EACH SYSTEM
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("RENAMING GAMELISTS")
    print("=" * 80)
    
    deployment_log = []
    
    for plan in deployment_plan:
        system = plan['system']
        new_file = plan['new']
        old_file = plan['old']
        
        print(f"\n📦 Deploying: {system}")
        print("-" * 80)
        
        for dest in plan['destinations']:
            dest_file = dest['path']
            location = dest['location']
            
            try:
                # Create destination directory if needed
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Change file names
                old_file.rename(RETROBAT_BASE / system / 'gamelist_BACKUP.xml')
                new_file.rename(RETROBAT_BASE / system / 'gamelist.xml')

                print(f"   ✓ {location}: {dest_file}")
                deployment_log.append(f"✓ {system} → {location}: {dest_file}")
            except Exception as e:
                print(f"   ❌ {location}: Error - {e}")
                deployment_log.append(f"❌ {system} → {location}: {e}")
    
    # ========================================================================
    # SAVE DEPLOYMENT LOG
    # ========================================================================
    
    log_file = RETROBAT_BASE / '_RENAME_LOG.txt'
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("RENAME GAMELIST DEPLOYMENT LOG\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Source:      {UNIFIED_DIR}\n")
        f.write(f"RetroBat:    {RETROBAT_BASE}\n\n")
        f.write("RENAME:\n")
        f.write("-" * 80 + "\n\n")
        for entry in deployment_log:
            f.write(entry + "\n")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("✅ RENAMING COMPLETE!")
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
    print("\nYour gamelists have been renamed.")

if __name__ == "__main__":
    deploy_unified_gamelists()
