#!/usr/bin/env python3
"""
Enhanced Claude Code Hook - Play Zelda sounds with comprehensive mapping
Maps all Claude Code tools to appropriate Zelda sounds
"""

import json
import sys
import subprocess
from pathlib import Path

# Get the sounds directory
SOUNDS_DIR = Path(__file__).parent.parent / "sounds"

# Comprehensive sound mapping for all Claude Code tools
TOOL_SOUND_MAP = {
    # File Operations
    "Read": {
        "success": "file_open.wav",
        "error": "error.wav"
    },
    "Write": {
        "success": "file_create.wav",
        "error": "build_error.wav"
    },
    "Edit": {
        "success": "item_small.wav",
        "error": "error.wav"
    },
    "MultiEdit": {
        "success": "achievement.wav",
        "error": "build_error.wav"
    },
    "NotebookEdit": {
        "success": "puzzle_solved.wav",
        "error": "error.wav"
    },
    
    # Search Tools
    "Grep": {
        "success": "search_found.wav",
        "no_results": "search_complete.wav",
        "error": "error.wav"
    },
    "Glob": {
        "success": "search_found.wav",
        "error": "error.wav"
    },
    "LS": {
        "success": "menu_select.wav",
        "error": "error.wav"
    },
    
    # Execution
    "Bash": {
        "start": "item_small.wav",  # Quick sound for command start
        "success": "success.wav",
        "error": "damage.wav"
    },
    "Task": {
        "start": "session_start.wav",
        "success": "shrine_complete.wav",
        "error": "game_over.wav"
    },
    
    # Web Tools
    "WebFetch": {
        "success": "search_found.wav",
        "error": "error.wav"
    },
    "WebSearch": {
        "success": "search_complete.wav",
        "error": "error.wav"
    },
    
    # Todo Management
    "TodoWrite": {
        "success": "todo_complete.wav",
        "completed": "heart_get.wav",  # When marking todos complete
        "all_complete": "achievement.wav"
    },
    "ExitPlanMode": {
        "success": "menu_select.wav"
    },
    
    # MCP Tools
    "mcp__ide__executeCode": {
        "success": "test_pass.wav",
        "error": "build_error.wav"
    },
    "mcp__ide__getDiagnostics": {
        "success": "search_complete.wav",
        "error": "warning.wav"
    }
}

# Hook event sounds
HOOK_EVENT_SOUNDS = {
    "Notification": "warning.wav",
    "UserPromptSubmit": "notification.wav",
    "Stop": "session_night.wav",
    "SubagentStop": "shrine_complete.wav",
    "SessionStart": "session_start.wav",
    "PreCompact": "menu_select.wav"
}

def play_sound_async(sound_file):
    """Play a sound file asynchronously without blocking"""
    sound_path = SOUNDS_DIR / sound_file
    if sound_path.exists():
        subprocess.Popen(
            ["afplay", str(sound_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def get_tool_sound(tool_name, response):
    """Determine which sound to play based on tool and response"""
    # Check if tool has specific mapping
    if tool_name in TOOL_SOUND_MAP:
        tool_sounds = TOOL_SOUND_MAP[tool_name]
        
        # Determine success/error state
        if isinstance(response, dict):
            # Check for explicit success field
            if response.get("success") is False:
                return tool_sounds.get("error", "error.wav")
            
            # Check for error field
            if "error" in response:
                return tool_sounds.get("error", "error.wav")
            
            # Check for exit code (Bash commands)
            if "exitCode" in response:
                if response["exitCode"] == 0:
                    return tool_sounds.get("success", "success.wav")
                else:
                    return tool_sounds.get("error", "damage.wav")
            
            # Check for empty results (search tools)
            if tool_name in ["Grep", "Glob"] and "results" in response:
                if not response["results"]:
                    return tool_sounds.get("no_results", "search_complete.wav")
            
            # Check for TodoWrite specific cases
            if tool_name == "TodoWrite" and "todos" in response:
                todos = response["todos"]
                completed_count = sum(1 for t in todos if t.get("status") == "completed")
                if completed_count == len(todos) and completed_count > 0:
                    return tool_sounds.get("all_complete", "achievement.wav")
                elif completed_count > 0:
                    return tool_sounds.get("completed", "heart_get.wav")
            
            # Default to success
            return tool_sounds.get("success", "success.wav")
        
        elif isinstance(response, str):
            # String responses - check for error indicators
            response_lower = response.lower()
            if any(word in response_lower for word in ["error", "failed", "fail", "exception"]):
                return tool_sounds.get("error", "error.wav")
            return tool_sounds.get("success", "success.wav")
        
        else:
            # Default to success sound for this tool
            return tool_sounds.get("success", "success.wav")
    
    # Check for MCP tools with pattern matching
    if tool_name.startswith("mcp__"):
        # Use generic MCP sounds
        if isinstance(response, dict) and (response.get("success") is False or "error" in response):
            return "warning.wav"
        return "puzzle_solved.wav"
    
    # Default fallback
    return "success.wav" if not _is_error_response(response) else "error.wav"

def _is_error_response(response):
    """Helper to determine if response indicates an error"""
    if isinstance(response, dict):
        return response.get("success") is False or "error" in response
    elif isinstance(response, str):
        return any(word in response.lower() for word in ["error", "failed", "exception"])
    return False

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Silent failure
        sys.exit(0)
    
    # Extract relevant information
    hook_event = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")
    tool_response = input_data.get("tool_response", {})
    
    # Handle different hook events
    if hook_event == "PostToolUse" and tool_name:
        # Tool-specific sound
        sound = get_tool_sound(tool_name, tool_response)
        play_sound_async(sound)
    
    elif hook_event == "PreToolUse" and tool_name:
        # Play start sound for certain tools
        if tool_name == "Bash":
            play_sound_async("item_small.wav")  # Quick prep sound
        elif tool_name == "Task":
            play_sound_async("notification.wav")  # Starting subagent
    
    elif hook_event in HOOK_EVENT_SOUNDS:
        # Hook event specific sounds
        play_sound_async(HOOK_EVENT_SOUNDS[hook_event])
    
    # Exit successfully
    sys.exit(0)

if __name__ == "__main__":
    main()