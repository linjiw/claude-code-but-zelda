#!/usr/bin/env python3
"""
Configure Claude Code hooks properly according to official documentation
"""

import json
from pathlib import Path
import os

def configure_hooks():
    """Set up Claude Code hooks with the correct format"""
    
    # Claude uses ~/.claude/settings.json
    settings_path = Path.home() / '.claude' / 'settings.json'
    hook_script = Path(__file__).parent / 'hooks' / 'play_sound_hook.py'
    
    # Make sure hook script is executable
    os.chmod(hook_script, 0o755)
    
    # Read existing settings
    if settings_path.exists():
        with open(settings_path) as f:
            settings = json.load(f)
        # Backup
        backup_path = settings_path.with_suffix('.json.backup_proper_hooks')
        with open(backup_path, 'w') as f:
            json.dump(settings, f, indent=2)
        print(f"Backed up to: {backup_path}")
    else:
        settings = {}
    
    # Configure hooks according to official documentation
    settings["hooks"] = {
        # PostToolUse - Runs after tools complete successfully
        "PostToolUse": [
            {
                "matcher": "*",  # Match all tools
                "hooks": [
                    {
                        "type": "command",
                        "command": f"python3 {hook_script}"
                    }
                ]
            }
        ],
        
        # Notification - When Claude needs input or permission
        "Notification": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": f"python3 {hook_script}"
                    }
                ]
            }
        ],
        
        # Stop - When Claude finishes responding
        "Stop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": f"python3 {hook_script}"
                    }
                ]
            }
        ]
    }
    
    # Write the settings
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print("✅ Claude Code hooks configured properly!")
    print(f"📍 Settings location: {settings_path}")
    print(f"🎵 Hook script: {hook_script}")
    
    print("\n📋 Configured hooks:")
    print("  • PostToolUse → Plays success/error sounds after tool execution")
    print("  • Notification → Plays warning sound when Claude needs input")
    print("  • Stop → Plays completion sound when Claude finishes")
    
    print("\n🎮 What will happen:")
    print("  • Successful commands → Cooking Success sound")
    print("  • Failed commands → Cooking Fail sound")
    print("  • Todo completion → GetHeart sound")
    print("  • Test pass → Puzzle Solved sound")
    print("  • Test fail → Game Over sound")
    print("  • Claude needs input → Assassin Appear sound")
    print("  • Claude finishes → GetLarge sound")
    
    return settings_path

if __name__ == "__main__":
    settings_path = configure_hooks()
    
    print("\n⚠️  IMPORTANT:")
    print("  1. Restart Claude Code for changes to take effect")
    print("  2. You can also use /hooks command in Claude Code to verify")
    print("\n🧪 Test with:")
    print("  claude")
    print("  > ls          # Should play success sound")
    print("  > cat /fake   # Should play error sound")
    print("  > Create a todo list and mark items complete")