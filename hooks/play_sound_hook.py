#!/usr/bin/env python3
"""
Claude Code Hook - Play Zelda sounds based on tool execution results
Receives JSON via stdin and plays appropriate sound
Fixed version that handles actual Claude Code JSON format
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
    
    # Debug: Log the input to understand the format
    # with open("/tmp/claude_hook_debug.log", "a") as f:
    #     f.write(json.dumps(input_data, indent=2) + "\n\n")
    
    # Extract relevant information
    hook_event = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})
    
    # Handle different response formats
    # Sometimes tool_response is a string, sometimes a dict
    if isinstance(tool_response, str):
        # For string responses, check if it contains error indicators
        is_error = "error" in tool_response.lower() or "failed" in tool_response.lower()
        success = not is_error
    elif isinstance(tool_response, dict):
        # For dict responses, check for success field
        success = tool_response.get("success", True)
        # Also check for error field
        if "error" in tool_response:
            success = False
    else:
        # Default to success if we can't determine
        success = True
    
    # For PostToolUse events
    if hook_event == "PostToolUse":
        # Special handling for different tools
        if tool_name == "TodoWrite":
            # Check if any todos were marked complete
            if isinstance(tool_response, dict):
                todos = tool_response.get("todos", [])
                if any(todo.get("status") == "completed" for todo in todos):
                    play_sound_async("todo_complete.wav")  # GetHeart sound
                    sys.exit(0)
            play_sound_async("success.wav")  # Regular success
        
        elif tool_name in ["Test", "TestRun"]:
            # Test execution results
            if success:
                play_sound_async("puzzle_solved.wav")  # Test pass
            else:
                play_sound_async("damage.wav")  # Test fail
        
        elif tool_name in ["Read", "LS", "List"] and not success:
            # File/directory operations that failed
            play_sound_async("error.wav")  # Cooking Fail
        
        elif tool_name in ["Bash", "Shell", "Execute"]:
            # Command execution - check exit code if available
            if isinstance(tool_response, dict) and "exitCode" in tool_response:
                if tool_response["exitCode"] == 0:
                    play_sound_async("success.wav")
                else:
                    play_sound_async("error.wav")
            elif success:
                play_sound_async("success.wav")
            else:
                play_sound_async("error.wav")
        
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