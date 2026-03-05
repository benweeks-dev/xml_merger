#!/usr/bin/env python3
"""
Custom GameList Unifier for Ben's Setup
Handles PC backup's non-standard structure where gamelist.xml is inside media folder
"""

from pathlib import Path
from gamelist_unifier import GameListUnifier

def main():
    print("=" * 80)
    print("GAMELIST UNIFIER - NGP TEST RUN")
    print("=" * 80)
    
    # ========================================================================
    # YOUR SPECIFIC PATHS
    # ========================================================================
    
    # PC Backup - gamelist.xml is INSIDE the media folder
    PC_BACKUP_BASE = Path(r'D:\ROMs BackUp\ROMs - 1G1R\SNK\NeoGeo Pocket')
    PC_BACKUP_GAMELIST = PC_BACKUP_BASE / 'media' / 'gamelist.xml'
    
    # RetroBat - normal structure
    RETROBAT_BASE = Path(r'D:\RetroBat\roms\ngp')  # Update this to your actual path
    RETROBAT_GAMELIST = RETROBAT_BASE / 'gamelist.xml'
    
    # Output directory
    OUTPUT_DIR = Path(r'D:\Unified_Gamelists')
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # ========================================================================
    # VERIFY PATHS
    # ========================================================================
    
    print("\n🔍 Verifying paths...")
    print(f"\nPC Backup:")
    print(f"  Base:     {PC_BACKUP_BASE}")
    print(f"  Gamelist: {PC_BACKUP_GAMELIST}")
    print(f"  Exists:   {'✓' if PC_BACKUP_GAMELIST.exists() else '❌ NOT FOUND'}")
    
    print(f"\nRetroBat:")
    print(f"  Base:     {RETROBAT_BASE}")
    print(f"  Gamelist: {RETROBAT_GAMELIST}")
    print(f"  Exists:   {'✓' if RETROBAT_GAMELIST.exists() else '❌ NOT FOUND'}")
    
    # Check if we found any gamelists
    sources_to_parse = []
    
    if PC_BACKUP_GAMELIST.exists():
        sources_to_parse.append(('PC Backup', PC_BACKUP_GAMELIST, PC_BACKUP_BASE))
    else:
        print(f"\n⚠ Warning: PC backup gamelist not found at:")
        print(f"   {PC_BACKUP_GAMELIST}")
    
    if RETROBAT_GAMELIST.exists():
        sources_to_parse.append(('RetroBat', RETROBAT_GAMELIST, RETROBAT_BASE))
    else:
        print(f"\n⚠ Warning: RetroBat gamelist not found at:")
        print(f"   {RETROBAT_GAMELIST}")
    
    if not sources_to_parse:
        print("\n❌ No gamelist.xml files found! Please update the paths in this script.")
        print("\nExpected locations:")
        print(f"  PC Backup: {PC_BACKUP_GAMELIST}")
        print(f"  RetroBat:  {RETROBAT_GAMELIST}")
        return
    
    # ========================================================================
    # PARSE GAMELISTS
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("PARSING GAMELISTS")
    print("=" * 80)
    
    # Create unifier with name cleaning enabled
    unifier = GameListUnifier(clean_names=True)
    print("✓ Name cleaning enabled (will remove region/language tags)")
    
    for source_name, gamelist_path, base_path in sources_to_parse:
        print(f"\n📖 Parsing: {source_name}")
        print(f"   Path: {gamelist_path}")
        unifier.parse_gamelist(gamelist_path, source_name=source_name)
    
    print(f"\n✅ Total unique games found: {len(unifier.games)}")
    
    # ========================================================================
    # SHOW SAMPLE DATA
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("SAMPLE DATA (First 3 games)")
    print("=" * 80)
    
    for i, (rom_path, entry) in enumerate(list(unifier.games.items())[:3], 1):
        print(f"\n{i}. {entry.name or rom_path}")
        print(f"   ROM Path:     {entry.path}")
        print(f"   Description:  {entry.desc[:80] + '...' if len(entry.desc) > 80 else entry.desc}")
        print(f"   Developer:    {entry.developer}")
        print(f"   Release Date: {entry.releasedate}")
        print(f"   Media:")
        if entry.image:
            print(f"     • Image:     {entry.image}")
        if entry.thumbnail:
            print(f"     • Thumbnail: {entry.thumbnail}")
        if entry.marquee:
            print(f"     • Marquee:   {entry.marquee}")
        if entry.boxback:
            print(f"     • Boxback:   {entry.boxback}")
        if entry.manual:
            print(f"     • Manual:    {entry.manual}")
    
    # ========================================================================
    # STANDARDIZE MEDIA PATHS
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("STANDARDIZING MEDIA PATHS")
    print("=" * 80)
    
    unifier.standardize_media_paths(preferred_structure='retrobat')
    print("✓ Media paths standardized to RetroBat structure")
    
    # ========================================================================
    # VALIDATE MEDIA (Check both locations)
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("VALIDATING MEDIA FILES")
    print("=" * 80)
    
    # Check PC Backup media
    if PC_BACKUP_BASE.exists():
        print(f"\n📂 Checking PC Backup: {PC_BACKUP_BASE}")
        pc_missing = unifier.validate_media(PC_BACKUP_BASE, report_missing=False)
        
        if any(pc_missing.values()):
            pc_missing_report = OUTPUT_DIR / 'ngp_pc_backup_missing_media.txt'
            with open(pc_missing_report, 'w') as f:
                f.write(f"Missing Media Report - PC Backup\n")
                f.write(f"Base Path: {PC_BACKUP_BASE}\n")
                f.write("=" * 80 + "\n\n")
                for media_type, files in pc_missing.items():
                    if files:
                        f.write(f"\n{media_type.upper()} - {len(files)} missing:\n")
                        for filepath in sorted(files):
                            f.write(f"  {filepath}\n")
    
    # Check RetroBat media
    if RETROBAT_BASE.exists():
        print(f"\n📂 Checking RetroBat: {RETROBAT_BASE}")
        rb_missing = unifier.validate_media(RETROBAT_BASE, report_missing=False)
        
        if any(rb_missing.values()):
            rb_missing_report = OUTPUT_DIR / 'ngp_retrobat_missing_media.txt'
            with open(rb_missing_report, 'w') as f:
                f.write(f"Missing Media Report - RetroBat\n")
                f.write(f"Base Path: {RETROBAT_BASE}\n")
                f.write("=" * 80 + "\n\n")
                for media_type, files in rb_missing.items():
                    if files:
                        f.write(f"\n{media_type.upper()} - {len(files)} missing:\n")
                        for filepath in sorted(files):
                            f.write(f"  {filepath}\n")
    
    # ========================================================================
    # GENERATE UNIFIED GAMELIST
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("GENERATING UNIFIED GAMELIST")
    print("=" * 80)
    
    output_gamelist = OUTPUT_DIR / 'ngp_unified_gamelist.xml'
    unifier.generate_unified_gamelist(output_gamelist, format_style='retrobat')
    
    # ========================================================================
    # GENERATE REPORT
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("GENERATING REPORT")
    print("=" * 80)
    
    report_path = OUTPUT_DIR / 'ngp_unification_report.txt'
    unifier.generate_report(report_path)
    
    # ========================================================================
    # COMPARISON REPORT
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("GENERATING COMPARISON REPORT")
    print("=" * 80)
    
    comparison_path = OUTPUT_DIR / 'ngp_source_comparison.txt'
    
    with open(comparison_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("PC BACKUP vs RETROBAT COMPARISON\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Total Games: {len(unifier.games)}\n\n")
        
        # Which source had better data for each game
        f.write("DATA SOURCE ATTRIBUTION:\n")
        f.write("-" * 80 + "\n\n")
        
        for rom_path, entry in sorted(unifier.games.items()):
            f.write(f"\n{entry.name or rom_path}:\n")
            
            if entry.data_sources:
                for field, source in sorted(entry.data_sources.items()):
                    f.write(f"  {field:12s}: {source}\n")
            else:
                f.write("  No source tracking available\n")
    
    print(f"✓ Comparison report saved: {comparison_path}")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    print(f"\n📄 Generated files:")
    print(f"   • ngp_unified_gamelist.xml      - Merged gamelist")
    print(f"   • ngp_unification_report.txt    - Data quality report")
    print(f"   • ngp_source_comparison.txt     - Which source provided what data")
    
    if any(pc_missing.values() if PC_BACKUP_BASE.exists() else False):
        print(f"   • ngp_pc_backup_missing_media.txt  - Missing media in PC backup")
    if any(rb_missing.values() if RETROBAT_BASE.exists() else False):
        print(f"   • ngp_retrobat_missing_media.txt   - Missing media in RetroBat")
    
    print("\n💡 Next Steps:")
    print("   1. Review the unified gamelist.xml")
    print("   2. Check the comparison report to see which source had better data")
    print("   3. Review missing media reports")
    print("   4. If satisfied, copy unified gamelist to:")
    print(f"      • PC Backup: {PC_BACKUP_BASE / 'media' / 'gamelist.xml'}")
    print(f"      • RetroBat:  {RETROBAT_BASE / 'gamelist.xml'}")
    print("\n⚠  Make backups before overwriting!")

if __name__ == "__main__":
    main()
