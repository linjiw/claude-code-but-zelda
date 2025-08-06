#!/usr/bin/env python3
"""
Complete replacement of ALL sounds with custom Zelda tracks
Uses ONLY sounds from user-customized-sound folder
"""

import os
import subprocess
from pathlib import Path
import shutil

def convert_mp3_to_wav(mp3_path, wav_path):
    """Convert MP3 to WAV using ffmpeg or afconvert"""
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
    backup_dir = base_dir / 'sounds_backup_original'
    
    # Create backup of original sounds if not exists
    if not backup_dir.exists():
        print("Creating backup of original sounds...")
        shutil.copytree(sounds_dir, backup_dir)
        print(f"Backup created at: {backup_dir}")
    
    # Clear current sounds directory
    print("\nClearing current sounds directory...")
    for file in sounds_dir.glob('*.wav'):
        file.unlink()
    
    # Complete mapping - ALL sounds from custom folder
    sound_mapping = {
        # Core sounds
        '243. Cooking Success.mp3': 'success.wav',
        '741. GetLarge.mp3': 'item_get.wav',
        '237. Cooking Fail.mp3': 'error.wav',
        '744. GetSmall.mp3': 'rupee.wav',
        '740. GetHeart.mp3': 'todo_complete.wav',
        '743. GetMedium.mp3': 'puzzle_solved.wav',
        '363. Dm F S Y Game Over.mp3': 'damage.wav',
        '938. Location Open Main.mp3': 'secret.wav',
        
        # New sounds for remaining placeholders
        '167. ZonauBlockMaster BridgeA 1.mp3': 'menu_select.wav',
        '206. Assassin Appear.mp3': 'warning.wav',
        '010. ReadRiddle.mp3': 'default.wav'
    }
    
    # Process each file
    print("\n🎮 Converting all custom sounds...")
    print("=" * 50)
    converted_count = 0
    failed_count = 0
    
    for mp3_file, wav_name in sound_mapping.items():
        mp3_path = custom_dir / mp3_file
        wav_path = sounds_dir / wav_name
        
        if mp3_path.exists():
            print(f"\n📦 {mp3_file}")
            print(f"   → {wav_name}")
            if convert_mp3_to_wav(mp3_path, wav_path):
                converted_count += 1
                print(f"   ✅ Converted successfully")
            else:
                failed_count += 1
                print(f"   ❌ Conversion failed")
        else:
            failed_count += 1
            print(f"\n❌ File not found: {mp3_file}")
    
    print("\n" + "=" * 50)
    print(f"✅ Successfully converted: {converted_count} sounds")
    if failed_count > 0:
        print(f"❌ Failed conversions: {failed_count}")
    
    print("\n📋 Complete Sound Mapping:")
    print("-" * 40)
    print("SUCCESS/COMPLETION:")
    print("  • success.wav ← Cooking Success")
    print("  • item_get.wav ← GetLarge") 
    print("  • puzzle_solved.wav ← GetMedium")
    print("  • todo_complete.wav ← GetHeart")
    print("  • secret.wav ← Location Open Main")
    print("\nERROR/WARNING:")
    print("  • error.wav ← Cooking Fail")
    print("  • damage.wav ← Game Over")
    print("  • warning.wav ← Assassin Appear")
    print("\nNAVIGATION:")
    print("  • menu_select.wav ← ZonauBlockMaster Bridge")
    print("  • rupee.wav ← GetSmall (progress)")
    print("  • default.wav ← ReadRiddle")
    
    print("\n🎵 ALL sounds are now from your custom collection!")
    print("🔊 Test with: ./demo_sounds.sh")
    print("⚙️  Activate in Claude Code: ./setup_claude_hooks.sh")

if __name__ == "__main__":
    main()