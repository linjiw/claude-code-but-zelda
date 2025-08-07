#!/usr/bin/env python3
"""
Zelda CLI - Interactive commands for Claude Code Zelda integration
Usage: python3 zelda_cli.py [command]
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.stats_tracker import get_tracker
from src.features.combo_system import get_combo_tracker  
from src.features.achievement_system import get_achievement_manager

def format_time(minutes: float) -> str:
    """Format minutes into human-readable time"""
    if minutes < 60:
        return f"{minutes:.1f} minutes"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.1f} hours"
    days = hours / 24
    return f"{days:.1f} days"

def show_stats():
    """Display coding statistics"""
    tracker = get_tracker()
    stats = tracker.get_stats_summary()
    
    print("\n" + "="*60)
    print("🎮 ZELDA CODING STATISTICS")
    print("="*60)
    
    # All-time stats
    all_time = stats["all_time"]
    print("\n📊 All-Time Stats:")
    print(f"  Total Sessions: {all_time['total_sessions']}")
    print(f"  Total Commands: {all_time['total_commands']}")
    print(f"  Success Rate: {all_time['success_rate']}")
    print(f"  Longest Streak: {all_time['longest_streak']} 🔥")
    print(f"  Total Coding Time: {format_time(all_time['total_time'])}")
    print(f"  Favorite Tool: {all_time['favorite_tool'] or 'None yet'}")
    print(f"  Achievements: {all_time['achievements']}/{all_time['milestones']} milestones")
    
    # Current session stats
    if "current_session" in stats:
        session = stats["current_session"]
        print("\n⚡ Current Session:")
        print(f"  Commands: {session['commands']}")
        print(f"  Success Rate: {session['success_rate']}")
        print(f"  Current Streak: {session['current_streak']}")
        print(f"  Max Streak: {session['max_streak']}")
        
        if session['top_tools']:
            print("  Top Tools:")
            for tool, count in session['top_tools'][:3]:
                print(f"    • {tool}: {count} uses")
    
    print("\n" + "="*60)

def show_achievements():
    """Display achievement progress"""
    manager = get_achievement_manager()
    summary = manager.get_achievement_summary()
    
    print("\n" + "="*60)
    print("🏆 ACHIEVEMENTS")
    print("="*60)
    
    print(f"\nTotal Progress: {summary['unlocked']}/{summary['total_achievements']} ({summary['percentage']:.1f}%)")
    
    # Progress bar
    bar_length = 40
    filled = int(bar_length * summary['percentage'] / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"[{bar}]")
    
    # By category
    print("\n📂 By Category:")
    for category, data in summary['by_category'].items():
        print(f"  {category.value.title()}: {data['unlocked']}/{data['total']}")
    
    # Recent unlocks
    if summary['recent_unlocks']:
        print("\n🎖️ Recent Achievements:")
        for unlock in summary['recent_unlocks'][:5]:
            date = datetime.fromisoformat(unlock['date']).strftime("%Y-%m-%d")
            print(f"  {unlock['icon']} {unlock['name']} - {date}")
    
    # Next closest
    if summary['next_closest']:
        print(f"\n📍 Next Closest: {summary['next_closest']}")
    
    # List all achievements (grouped by unlocked status)
    print("\n📜 All Achievements:")
    
    unlocked = []
    locked = []
    
    for aid, achievement in manager.achievements.items():
        progress = manager.progress[aid]
        if progress.unlocked:
            unlocked.append((achievement, progress))
        else:
            locked.append((achievement, progress))
    
    if unlocked:
        print("\n✅ Unlocked:")
        for achievement, progress in unlocked:
            print(f"  {achievement.icon} {achievement.name} - {achievement.description}")
    
    if locked:
        print("\n🔒 Locked:")
        for achievement, progress in locked[:10]:  # Show first 10 locked
            if not achievement.hidden or progress.current_progress > 0:
                percent = progress.progress_percent
                print(f"  {achievement.icon} {achievement.name} ({percent:.0f}%)")
                print(f"     {achievement.description}")
                print(f"     Progress: {progress.current_progress}/{progress.requirement}")
    
    print("\n" + "="*60)

def show_combo():
    """Display current combo status"""
    tracker = get_combo_tracker()
    status = tracker.get_combo_status()
    
    print("\n" + "="*60)
    print("⚡ COMBO STATUS")
    print("="*60)
    
    print(f"\n🔥 Current Streak: {status['current_streak']}")
    print(f"🏆 Highest Streak: {status['highest_streak']}")
    print(f"🎯 Current Level: {status['current_level']}")
    print(f"💎 Total Combos: {status['total_combos']}")
    
    if "next_milestone" in status:
        print(f"\n📊 Progress to Next Level:")
        print(f"   {status['progress_to_next']}")
        
        # Visual progress bar
        current = status['current_streak']
        next_level = status['next_milestone']
        percent = (current / next_level) * 100
        bar_length = 30
        filled = int(bar_length * percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   [{bar}] {percent:.0f}%")
    
    # Combo levels guide
    print("\n📈 Combo Levels:")
    print("  🥉 Bronze: 3 commands")
    print("  🥈 Silver: 5 commands")
    print("  🥇 Gold: 10 commands")
    print("  💎 Platinum: 20 commands")
    print("  🔥 Master: 50 commands")
    
    print("\n" + "="*60)

def test_sounds():
    """Test all sound files"""
    import subprocess
    from pathlib import Path
    
    sounds_dir = Path(__file__).parent / "sounds"
    
    print("\n" + "="*60)
    print("🔊 SOUND TEST")
    print("="*60)
    
    wav_files = sorted(sounds_dir.glob("*.wav"))
    
    if not wav_files:
        print("\n❌ No sound files found in sounds/ directory")
        return
    
    print(f"\nFound {len(wav_files)} sound files")
    print("Playing each sound with 1 second delay...\n")
    
    for i, wav_file in enumerate(wav_files, 1):
        print(f"  {i:2d}. {wav_file.name:<30}", end="", flush=True)
        
        # Play sound
        try:
            subprocess.run(["afplay", str(wav_file)], 
                         capture_output=True, timeout=10)
            print(" ✅")
        except subprocess.TimeoutExpired:
            print(" ⏱️ (timeout)")
        except Exception as e:
            print(f" ❌ ({e})")
        
        # Small delay between sounds
        if i < len(wav_files):
            subprocess.run(["sleep", "0.5"])
    
    print("\n" + "="*60)

def show_help():
    """Display help information"""
    print("""
🎮 ZELDA CLAUDE CODE - Command Reference
========================================

Usage: python3 zelda_cli.py [command]

Commands:
  stats        Show coding statistics and progress
  achievements Display achievement progress
  combo        Show current combo status
  test         Test all sound files
  help         Show this help message

Examples:
  python3 zelda_cli.py stats
  python3 zelda_cli.py achievements
  python3 zelda_cli.py combo

For Claude Code integration:
  1. Sounds play automatically via hooks
  2. Stats track in background
  3. Achievements unlock as you code
  4. Combos build with consecutive successes

Happy coding, Hero of Hyrule! 🗡️✨
""")

def main():
    parser = argparse.ArgumentParser(
        description="Zelda Claude Code CLI",
        add_help=False
    )
    parser.add_argument("command", nargs="?", default="help",
                       choices=["stats", "achievements", "combo", "test", "help"])
    
    args = parser.parse_args()
    
    commands = {
        "stats": show_stats,
        "achievements": show_achievements,
        "combo": show_combo,
        "test": test_sounds,
        "help": show_help
    }
    
    command_func = commands.get(args.command, show_help)
    command_func()

if __name__ == "__main__":
    main()