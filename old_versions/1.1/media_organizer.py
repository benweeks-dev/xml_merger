#!/usr/bin/env python3
"""
Media Organizer - Reorganize and validate media files
Helps migrate between different media folder structures
"""

from pathlib import Path
import shutil
from collections import defaultdict
from typing import Dict, List, Set

class MediaOrganizer:
    """Organize and validate media files for emulation systems"""
    
    # Standard media types and their common names
    MEDIA_TYPES = {
        'box2dfront': ['box2dfront', 'boxfront', 'cover', 'covers'],
        'box2dback': ['box2dback', 'boxback', 'backcover'],
        'mix': ['mix', 'fanart', 'screenshot'],
        'wheel': ['wheel', 'marquee', 'logo', 'logos'],
        'screenshot': ['screenshot', 'screenshots', 'snap', 'snaps'],
        'video': ['video', 'videos', 'videosnaps'],
        'manual': ['manual', 'manuals'],
        'titleshot': ['titleshot', 'titles'],
    }
    
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.media_path = self.base_path / 'media'
        self.stats: Dict[str, int] = defaultdict(int)
    
    def scan_media_structure(self) -> Dict[str, List[Path]]:
        """Scan and categorize existing media files"""
        print(f"🔍 Scanning media in: {self.base_path}")
        
        media_files: Dict[str, List[Path]] = defaultdict(list)
        
        if not self.media_path.exists():
            print(f"⚠ Media directory not found: {self.media_path}")
            return media_files
        
        # Scan all subdirectories
        for item in self.media_path.rglob('*'):
            if item.is_file() and not item.name.startswith('.'):
                # Determine media type from parent folder name
                folder_name = item.parent.name.lower()
                
                # Find matching media type
                media_type = 'unknown'
                for standard_type, aliases in self.MEDIA_TYPES.items():
                    if folder_name in aliases:
                        media_type = standard_type
                        break
                
                media_files[media_type].append(item)
                self.stats[media_type] += 1
        
        # Print summary
        print(f"\n📊 Media Files Found:")
        for media_type in sorted(self.stats.keys()):
            count = self.stats[media_type]
            print(f"   {media_type:15s}: {count:4d} files")
        
        total = sum(self.stats.values())
        print(f"   {'TOTAL':15s}: {total:4d} files")
        
        return media_files
    
    def reorganize_to_standard(self, dry_run: bool = True) -> None:
        """
        Reorganize media files to standard structure
        
        Standard structure:
        media/
          ├── box2dfront/
          ├── box2dback/
          ├── mix/
          ├── wheel/
          ├── screenshot/
          ├── video/
          ├── manual/
          └── titleshot/
        """
        print(f"\n🔄 Reorganizing to standard structure...")
        if dry_run:
            print("   (DRY RUN - no files will be moved)")
        
        media_files = self.scan_media_structure()
        moves_needed: Dict[str, List[tuple]] = defaultdict(list)
        
        # Plan the reorganization
        for media_type, files in media_files.items():
            if media_type == 'unknown':
                continue
            
            target_dir = self.media_path / media_type
            
            for file_path in files:
                # Check if already in correct location
                if file_path.parent == target_dir:
                    continue
                
                target_path = target_dir / file_path.name
                
                # Handle name conflicts
                if target_path.exists() and target_path != file_path:
                    print(f"   ⚠ Conflict: {file_path.name} exists in both:")
                    print(f"      Source: {file_path.parent}")
                    print(f"      Target: {target_dir}")
                    continue
                
                moves_needed[media_type].append((file_path, target_path))
        
        # Execute or report moves
        total_moves = sum(len(moves) for moves in moves_needed.values())
        
        if total_moves == 0:
            print("\n✅ All files already in correct locations!")
            return
        
        print(f"\n📦 Moves needed: {total_moves}")
        
        for media_type, moves in sorted(moves_needed.items()):
            print(f"\n{media_type}:")
            
            for source, target in moves:
                if not dry_run:
                    # Create target directory
                    target.parent.mkdir(parents=True, exist_ok=True)
                    # Move file
                    shutil.move(str(source), str(target))
                    print(f"   ✓ Moved: {source.name}")
                else:
                    print(f"   Would move: {source.name}")
                    print(f"      From: {source.parent}")
                    print(f"      To:   {target.parent}")
        
        if dry_run:
            print(f"\n💡 Run with dry_run=False to actually move files")
        else:
            print(f"\n✅ Reorganization complete!")
            
            # Clean up empty directories
            self._cleanup_empty_dirs()
    
    def _cleanup_empty_dirs(self) -> None:
        """Remove empty directories after reorganization"""
        print("\n🧹 Cleaning up empty directories...")
        
        removed = 0
        for item in sorted(self.media_path.rglob('*'), reverse=True):
            if item.is_dir() and not any(item.iterdir()):
                item.rmdir()
                print(f"   Removed: {item.relative_to(self.media_path)}")
                removed += 1
        
        if removed == 0:
            print("   No empty directories found")
        else:
            print(f"   ✓ Removed {removed} empty directories")
    
    def find_duplicates(self) -> Dict[str, List[Path]]:
        """Find duplicate media files (same name, different locations)"""
        print(f"\n🔍 Checking for duplicate files...")
        
        file_locations: Dict[str, List[Path]] = defaultdict(list)
        
        for file_path in self.media_path.rglob('*'):
            if file_path.is_file():
                file_locations[file_path.name].append(file_path)
        
        duplicates = {name: paths for name, paths in file_locations.items() 
                     if len(paths) > 1}
        
        if duplicates:
            print(f"\n⚠ Found {len(duplicates)} duplicate file names:")
            for name, paths in sorted(duplicates.items()):
                print(f"\n{name}:")
                for path in paths:
                    print(f"   • {path.relative_to(self.base_path)}")
        else:
            print("   ✅ No duplicates found!")
        
        return duplicates
    
    def validate_file_extensions(self) -> Dict[str, List[Path]]:
        """Check for unexpected file extensions"""
        print(f"\n🔍 Validating file extensions...")
        
        EXPECTED_EXTENSIONS = {
            'box2dfront': {'.png', '.jpg', '.jpeg'},
            'box2dback': {'.png', '.jpg', '.jpeg'},
            'mix': {'.png', '.jpg', '.jpeg'},
            'wheel': {'.png', '.svg'},
            'screenshot': {'.png', '.jpg', '.jpeg'},
            'video': {'.mp4', '.avi', '.mkv', '.webm'},
            'manual': {'.pdf'},
            'titleshot': {'.png', '.jpg', '.jpeg'},
        }
        
        unexpected: Dict[str, List[Path]] = defaultdict(list)
        
        for media_type, expected_exts in EXPECTED_EXTENSIONS.items():
            media_dir = self.media_path / media_type
            
            if not media_dir.exists():
                continue
            
            for file_path in media_dir.iterdir():
                if file_path.is_file():
                    if file_path.suffix.lower() not in expected_exts:
                        unexpected[media_type].append(file_path)
        
        if unexpected:
            print("\n⚠ Unexpected file extensions found:")
            for media_type, files in sorted(unexpected.items()):
                print(f"\n{media_type}:")
                for file_path in files:
                    print(f"   • {file_path.name} ({file_path.suffix})")
        else:
            print("   ✅ All file extensions look correct!")
        
        return unexpected
    
    def generate_media_report(self, output_path: Path) -> None:
        """Generate comprehensive media report"""
        print(f"\n📋 Generating media report: {output_path}")
        
        media_files = self.scan_media_structure()
        duplicates = self.find_duplicates()
        unexpected = self.validate_file_extensions()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("MEDIA ORGANIZATION REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Base Path: {self.base_path}\n")
            f.write(f"Media Path: {self.media_path}\n\n")
            
            # Summary
            f.write("SUMMARY:\n")
            f.write("-" * 80 + "\n")
            total = sum(self.stats.values())
            f.write(f"Total Files: {total}\n\n")
            
            for media_type in sorted(self.stats.keys()):
                count = self.stats[media_type]
                f.write(f"  {media_type:15s}: {count:4d} files\n")
            
            # Duplicates
            if duplicates:
                f.write(f"\n\nDUPLICATE FILES: {len(duplicates)}\n")
                f.write("-" * 80 + "\n")
                for name, paths in sorted(duplicates.items()):
                    f.write(f"\n{name}:\n")
                    for path in paths:
                        f.write(f"  • {path.relative_to(self.base_path)}\n")
            
            # Unexpected extensions
            if unexpected:
                f.write(f"\n\nUNEXPECTED FILE EXTENSIONS:\n")
                f.write("-" * 80 + "\n")
                for media_type, files in sorted(unexpected.items()):
                    f.write(f"\n{media_type}:\n")
                    for file_path in files:
                        f.write(f"  • {file_path.name} ({file_path.suffix})\n")
        
        print(f"   ✓ Report saved")


def main():
    """Example usage"""
    print("=" * 80)
    print("MEDIA ORGANIZER")
    print("=" * 80)
    
    # Example: Organize NeoGeo Pocket media
    system_path = Path(r'C:\RetroBat\roms\ngp')
    
    if not system_path.exists():
        print(f"\n⚠ Example path not found: {system_path}")
        print("\nUpdate the path in this script and try again.")
        return
    
    organizer = MediaOrganizer(system_path)
    
    # Scan current structure
    organizer.scan_media_structure()
    
    # Find issues
    organizer.find_duplicates()
    organizer.validate_file_extensions()
    
    # Reorganize (dry run first)
    organizer.reorganize_to_standard(dry_run=True)
    
    # Generate report
    report_path = system_path / 'media_report.txt'
    organizer.generate_media_report(report_path)


if __name__ == "__main__":
    main()
