#!/usr/bin/env python3
"""
Claude Code Hook - Play Zelda sounds based on tool execution results
Receives JSON via stdin and plays appropriate sound
"""

import json
import sys
import subprocess
from pathlib import Path

# Get the sounds directory
SOUNDS_DIR = Path(__file__).parent.parent / "sounds"

def play_sound_async(sound_file):
    """Play a sound file asynchronously without blocking"""
    sound_path = SOUNDS_DIR / sound_file
    if sound_path.exists():
        # Use subprocess.Popen for non-blocking playback
        subprocess.Popen(
            ["afplay", str(sound_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def main():
    try:
        # Read JSON input from stdin (provided by Claude Code)
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        # Silent failure - don't interrupt Claude Code
        sys.exit(0)
    
    # Extract relevant information
    hook_event = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")
    tool_response = input_data.get("tool_response", {})
    
    # For PostToolUse events
    if hook_event == "PostToolUse":
        # Check if the tool execution was successful
        success = tool_response.get("success", True)
        
        # Special handling for different tools
        if tool_name == "TodoWrite":
            # Check if any todos were marked complete
            todos = tool_response.get("todos", [])
            if any(todo.get("status") == "completed" for todo in todos):
                play_sound_async("todo_complete.wav")  # GetHeart sound
            else:
                play_sound_async("success.wav")  # Regular success
        
        elif tool_name in ["Test", "TestRun"]:
            # Test execution results
            if success:
                play_sound_async("puzzle_solved.wav")  # Test pass
            else:
                play_sound_async("damage.wav")  # Test fail
        
        elif success:
            # General success sound for all other tools
            play_sound_async("success.wav")  # Cooking Success
        
        else:
            # Error sound for failed operations
            play_sound_async("error.wav")  # Cooking Fail
    
    # For PreToolUse events (could add warning sounds here)
    elif hook_event == "PreToolUse":
        # Could play a "starting" sound
        if tool_name in ["Bash", "Shell", "Execute"]:
            play_sound_async("menu_select.wav")  # Starting action
    
    # For Notification events
    elif hook_event == "Notification":
        play_sound_async("warning.wav")  # Assassin Appear
    
    # For Stop events (Claude finished)
    elif hook_event == "Stop":
        play_sound_async("item_get.wav")  # Major completion
    
    # Exit successfully - don't block Claude Code
    sys.exit(0)

if __name__ == "__main__":
    main()