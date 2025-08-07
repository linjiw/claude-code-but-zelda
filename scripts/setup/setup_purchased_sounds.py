#!/usr/bin/env python3
"""
Setup purchased Zelda sounds for Claude Code
Converts MP3 to WAV and maps to appropriate filenames
"""

import os
import subprocess
from pathlib import Path
import shutil

# Define paths
SOURCE_DIR = Path("user-customized-sound")
TARGET_DIR = Path("sounds")
BACKUP_DIR = Path("sounds_backup/original")

# Create directories if needed
TARGET_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# Define sound mapping based on purchased files
# Map purchased sound IDs to Claude Code sound names
SOUND_MAPPING = {
    # Core success/error sounds (using 5-sec versions since 2-sec versions not purchased)
    "243. Cooking Success.mp3": "success.wav",           # Command success
    "237. Cooking Fail.mp3": "error.wav",               # Command error
    
    # Item/achievement sounds
    "744. GetSmall.mp3": "item_small.wav",              # Small success (2 sec)
    "743. GetMedium.mp3": "todo_complete.wav",          # Todo complete (5 sec)
    "741. GetLarge.mp3": "achievement.wav",             # Major achievement (6 sec)
    "740. GetHeart.mp3": "heart_get.wav",               # Health/milestone (6 sec)
    
    # Test/build sounds
    "952. Mercenary Clear.mp3": "test_pass.wav",        # All tests pass (4 sec)
    "363. Dm F S Y Game Over.mp3": "game_over.wav",     # Test fail (6 sec)
    "369. Dm F S Y Recycle Box Fail.mp3": "build_error.wav", # Build error (4 sec)
    
    # Notification/alert sounds
    "206. Assassin Appear.mp3": "warning.wav",          # Alert/warning (3 sec)
    "010. ReadRiddle.mp3": "notification.wav",          # Notification (2 sec)
    
    # File/search sounds
    "943. Location Open Small Dungeon Sub.mp3": "file_open.wav", # File opened (3 sec)
    "938. Location Open Main.mp3": "file_create.wav",   # File created (5 sec)
    "364. Dm F S Y Hide Chara Discovery.mp3": "search_found.wav", # Search success (4 sec)
    "250. Deep Hole Dive Blowing 0.mp3": "search_complete.wav", # Grep done (4 sec)
    
    # Session sounds
    "124. SmallDungeon Start.mp3": "session_start.wav", # Session begin (10 sec)
    "164. UotoriVillage Night Intro Fade.mp3": "session_night.wav", # Evening (9 sec)
    "167. ZonauBlockMaster BridgeA 1.mp3": "puzzle_solved.wav", # Extra: puzzle complete
}

# Additional copies for variety
ADDITIONAL_MAPPINGS = {
    "237. Cooking Fail.mp3": "damage.wav",              # Alternative error sound
    "740. GetHeart.mp3": "item_get.wav",                # Alternative item sound
    "744. GetSmall.mp3": "menu_select.wav",             # Menu navigation
    "952. Mercenary Clear.mp3": "shrine_complete.wav",  # Alternative success
}

def convert_mp3_to_wav(mp3_path, wav_path):
    """Convert MP3 to WAV using ffmpeg"""
    try:
        # Use ffmpeg to convert, normalizing audio
        cmd = [
            'ffmpeg', '-i', str(mp3_path),
            '-acodec', 'pcm_s16le',  # 16-bit PCM
            '-ar', '44100',           # 44.1kHz sample rate
            '-ac', '2',               # Stereo
            '-y',                     # Overwrite output
            str(wav_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"Error converting {mp3_path}: {result.stderr}")
            return False
    except FileNotFoundError:
        print("ffmpeg not found. Trying alternate method...")
        # Try using afconvert on macOS
        try:
            cmd = ['afconvert', '-f', 'WAVE', '-d', 'LEI16', str(mp3_path), str(wav_path)]
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except:
            print(f"Could not convert {mp3_path}. Please install ffmpeg: brew install ffmpeg")
            return False

def main():
    print("🎮 Setting up Zelda sounds for Claude Code\n")
    print("=" * 60)
    
    # Backup existing sounds
    print("\n📦 Backing up existing sounds...")
    if TARGET_DIR.exists():
        for wav_file in TARGET_DIR.glob("*.wav"):
            backup_path = BACKUP_DIR / wav_file.name
            if not backup_path.exists():
                shutil.copy2(wav_file, backup_path)
                print(f"  Backed up: {wav_file.name}")
    
    # Process main mappings
    print("\n🔄 Converting and mapping sounds...")
    converted_count = 0
    failed_count = 0
    
    for mp3_name, wav_name in SOUND_MAPPING.items():
        mp3_path = SOURCE_DIR / mp3_name
        wav_path = TARGET_DIR / wav_name
        
        if mp3_path.exists():
            print(f"\n  {mp3_name}")
            print(f"    → {wav_name}", end="")
            
            if convert_mp3_to_wav(mp3_path, wav_path):
                print(" ✅")
                converted_count += 1
            else:
                print(" ❌ (conversion failed)")
                failed_count += 1
        else:
            print(f"\n  ❌ Not found: {mp3_name}")
            failed_count += 1
    
    # Process additional mappings (copies)
    print("\n📋 Creating additional sound variants...")
    for mp3_name, wav_name in ADDITIONAL_MAPPINGS.items():
        mp3_path = SOURCE_DIR / mp3_name
        wav_path = TARGET_DIR / wav_name
        
        if mp3_path.exists():
            print(f"  {wav_name}", end="")
            
            if convert_mp3_to_wav(mp3_path, wav_path):
                print(" ✅")
                converted_count += 1
            else:
                print(" ❌")
    
    # Summary
    print("\n" + "=" * 60)
    print("\n📊 CONVERSION SUMMARY:")
    print(f"  ✅ Successfully converted: {converted_count} sounds")
    if failed_count > 0:
        print(f"  ❌ Failed conversions: {failed_count} sounds")
    
    # List all available sounds
    print("\n📂 Available sounds in sounds/ directory:")
    wav_files = sorted(TARGET_DIR.glob("*.wav"))
    for wav_file in wav_files:
        size = wav_file.stat().st_size / 1024  # KB
        print(f"  • {wav_file.name:<25} ({size:.1f} KB)")
    
    print(f"\n🎉 Setup complete! {len(wav_files)} sounds ready for Claude Code")
    
    # Create a reference file
    reference_file = Path("SOUND_REFERENCE.md")
    with open(reference_file, "w") as f:
        f.write("# Zelda Claude Code - Sound Reference\n\n")
        f.write("## Available Sounds\n\n")
        f.write("| Sound File | Source | Use Case |\n")
        f.write("|------------|--------|----------|\n")
        
        for mp3_name, wav_name in sorted(SOUND_MAPPING.items(), key=lambda x: x[1]):
            if (TARGET_DIR / wav_name).exists():
                source_name = mp3_name.replace(".mp3", "").split(". ", 1)[1]
                use_case = wav_name.replace(".wav", "").replace("_", " ").title()
                f.write(f"| {wav_name} | {source_name} | {use_case} |\n")
    
    print(f"\n📄 Created {reference_file} for your reference")

if __name__ == "__main__":
    main()