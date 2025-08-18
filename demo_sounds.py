#!/usr/bin/env python3
"""Demo script to play all Zelda sounds - Windows compatible version"""

import os
import sys
import time
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from play_sound import play_sound

def demo_sounds():
    """Play all sounds in sequence with descriptions"""
    
    sounds = [
        ("success", "✅ Success - Task completed!"),
        ("error", "❌ Error - Something went wrong"),
        ("warning", "⚠️ Warning - Pay attention"),
        ("achievement", "🏆 Achievement - You unlocked something!"),
        ("todo_complete", "✔️ Todo Complete - Task checked off"),
        ("puzzle_solved", "🧩 Puzzle Solved - Major breakthrough!"),
        ("item_get", "💎 Item Get - New discovery!"),
        ("damage", "💔 Damage - Test failed"),
        ("secret", "🗝️ Secret - Hidden feature found!")
    ]
    
    print("\n🎮 ZELDA CLAUDE CODE - SOUND DEMO 🎮\n")
    print("Playing all sounds...\n")
    
    for sound_name, description in sounds:
        print(f"  {description}")
        play_sound(sound_name)
        time.sleep(1.5)  # Wait between sounds
    
    print("\n✨ Demo complete! Happy coding!\n")

if __name__ == "__main__":
    demo_sounds()