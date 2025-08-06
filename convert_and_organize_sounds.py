#!/usr/bin/env python3
"""
Convert MP3 files to WAV and organize them for Claude Code hooks
"""

import os
import subprocess
from pathlib import Path
import shutil

def convert_mp3_to_wav(mp3_path, wav_path):
    """Convert MP3 to WAV using ffmpeg"""
    try:
        # Try ffmpeg first
        subprocess.run(['ffmpeg', '-i', str(mp3_path), '-acodec', 'pcm_s16le', 
                       '-ar', '44100', str(wav_path), '-y'], 
                      check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Try afconvert on macOS
            subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16', 
                          str(mp3_path), str(wav_path)], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"Could not convert {mp3_path.name} - ffmpeg or afconvert not found")
            return False

def main():
    # Paths
    base_dir = Path(__file__).parent
    custom_dir = base_dir / 'user-customized-sound'
    sounds_dir = base_dir / 'sounds'
    backup_dir = base_dir / 'sounds_backup'
    
    # Create backup of original sounds
    if not backup_dir.exists():
        print("Creating backup of original sounds...")
        shutil.copytree(sounds_dir, backup_dir)
        print(f"Backup created at: {backup_dir}")
    
    # Mapping of custom files to our sound system
    sound_mapping = {
        '237. Cooking Fail.mp3': 'error.wav',
        '243. Cooking Success.mp3': 'success.wav',
        '363. Dm F S Y Game Over.mp3': 'damage.wav',
        '740. GetHeart.mp3': 'todo_complete.wav',
        '741. GetLarge.mp3': 'item_get.wav',
        '743. GetMedium.mp3': 'puzzle_solved.wav',
        '744. GetSmall.mp3': 'rupee.wav',
        '938. Location Open Main.mp3': 'secret.wav'
    }
    
    # Process each file
    converted_count = 0
    for mp3_file, wav_name in sound_mapping.items():
        mp3_path = custom_dir / mp3_file
        wav_path = sounds_dir / wav_name
        
        if mp3_path.exists():
            print(f"Converting {mp3_file} -> {wav_name}")
            if convert_mp3_to_wav(mp3_path, wav_path):
                converted_count += 1
                print(f"  ✓ Converted successfully")
            else:
                print(f"  ✗ Conversion failed")
        else:
            print(f"  ✗ File not found: {mp3_file}")
    
    # Keep menu_select and warning from original
    print("\nKeeping original sounds for:")
    print("  • menu_select.wav")
    print("  • warning.wav")
    print("  • default.wav")
    
    if backup_dir.exists():
        for keep_file in ['menu_select.wav', 'warning.wav', 'default.wav']:
            backup_file = backup_dir / keep_file
            target_file = sounds_dir / keep_file
            if backup_file.exists() and not target_file.exists():
                shutil.copy2(backup_file, target_file)
    
    print(f"\n✅ Converted {converted_count} custom sounds!")
    print("\nSound mappings:")
    print("  • Cooking Fail → error.wav")
    print("  • Cooking Success → success.wav")
    print("  • Game Over → damage.wav (test fail)")
    print("  • GetHeart → todo_complete.wav")
    print("  • GetLarge → item_get.wav")
    print("  • GetMedium → puzzle_solved.wav")
    print("  • GetSmall → rupee.wav (progress)")
    print("  • Location Open → secret.wav")
    
    print("\nTest with: ./demo_sounds.sh")

if __name__ == "__main__":
    main()