#!/usr/bin/env python3
"""
Ultimate Claude Code Hook - Complete Zelda Experience
Integrates sounds, statistics, combos, and achievements
"""

import json
import sys
import subprocess
from pathlib import Path
import os

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.stats_tracker import get_tracker
from src.features.combo_system import get_combo_tracker
from src.features.achievement_system import get_achievement_manager

# Get the sounds directory
SOUNDS_DIR = Path(__file__).parent.parent / "sounds"

# Comprehensive sound mapping for all Claude Code tools
TOOL_SOUND_MAP = {
    # File Operations
    "Read": {"success": "file_open.wav", "error": "error.wav"},
    "Write": {"success": "file_create.wav", "error": "build_error.wav"},
    "Edit": {"success": "item_small.wav", "error": "error.wav"},
    "MultiEdit": {"success": "achievement.wav", "error": "build_error.wav"},
    "NotebookEdit": {"success": "puzzle_solved.wav", "error": "error.wav"},
    
    # Search Tools
    "Grep": {"success": "search_found.wav", "no_results": "search_complete.wav", "error": "error.wav"},
    "Glob": {"success": "search_found.wav", "error": "error.wav"},
    "LS": {"success": "menu_select.wav", "error": "error.wav"},
    
    # Execution
    "Bash": {"start": "item_small.wav", "success": "success.wav", "error": "damage.wav"},
    "Task": {"start": "session_start.wav", "success": "shrine_complete.wav", "error": "game_over.wav"},
    
    # Web Tools
    "WebFetch": {"success": "search_found.wav", "error": "error.wav"},
    "WebSearch": {"success": "search_complete.wav", "error": "error.wav"},
    
    # Todo Management
    "TodoWrite": {"success": "todo_complete.wav", "completed": "heart_get.wav", "all_complete": "achievement.wav"},
    "ExitPlanMode": {"success": "menu_select.wav"},
    
    # MCP Tools
    "mcp__ide__executeCode": {"success": "test_pass.wav", "error": "build_error.wav"},
    "mcp__ide__getDiagnostics": {"success": "search_complete.wav", "error": "warning.wav"}
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

# Initialize systems
stats_tracker = get_tracker()
combo_tracker = get_combo_tracker()
achievement_manager = get_achievement_manager()

# Track error-free commands for perfectionist achievements
error_free_count = 0

def play_sound_async(sound_file):
    """Play a sound file asynchronously without blocking"""
    sound_path = SOUNDS_DIR / sound_file
    if sound_path.exists():
        subprocess.Popen(
            ["afplay", str(sound_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def play_multiple_sounds(sounds):
    """Play multiple sounds with slight delay between them"""
    for i, sound in enumerate(sounds):
        if sound:
            # Add tiny delay for subsequent sounds
            if i > 0:
                subprocess.Popen(["sleep", "0.2"]).wait()
            play_sound_async(sound)

def get_tool_sound(tool_name, response):
    """Determine which sound to play based on tool and response"""
    if tool_name in TOOL_SOUND_MAP:
        tool_sounds = TOOL_SOUND_MAP[tool_name]
        
        # Determine success/error state
        if isinstance(response, dict):
            if response.get("success") is False or "error" in response:
                return tool_sounds.get("error", "error.wav"), False
            
            # Check for exit code (Bash commands)
            if "exitCode" in response:
                if response["exitCode"] == 0:
                    return tool_sounds.get("success", "success.wav"), True
                else:
                    return tool_sounds.get("error", "damage.wav"), False
            
            # Check for empty results (search tools)
            if tool_name in ["Grep", "Glob"] and "results" in response:
                if not response["results"]:
                    return tool_sounds.get("no_results", "search_complete.wav"), True
            
            # Check for TodoWrite specific cases
            if tool_name == "TodoWrite" and "todos" in response:
                todos = response["todos"]
                completed_count = sum(1 for t in todos if t.get("status") == "completed")
                if completed_count == len(todos) and completed_count > 0:
                    return tool_sounds.get("all_complete", "achievement.wav"), True
                elif completed_count > 0:
                    return tool_sounds.get("completed", "heart_get.wav"), True
            
            return tool_sounds.get("success", "success.wav"), True
        
        elif isinstance(response, str):
            response_lower = response.lower()
            if any(word in response_lower for word in ["error", "failed", "fail", "exception"]):
                return tool_sounds.get("error", "error.wav"), False
            return tool_sounds.get("success", "success.wav"), True
        
        else:
            return tool_sounds.get("success", "success.wav"), True
    
    # Check for MCP tools
    if tool_name.startswith("mcp__"):
        if isinstance(response, dict) and (response.get("success") is False or "error" in response):
            return "warning.wav", False
        return "puzzle_solved.wav", True
    
    # Default fallback
    is_success = not _is_error_response(response)
    return ("success.wav" if is_success else "error.wav"), is_success

def _is_error_response(response):
    """Helper to determine if response indicates an error"""
    if isinstance(response, dict):
        return response.get("success") is False or "error" in response
    elif isinstance(response, str):
        return any(word in response.lower() for word in ["error", "failed", "exception"])
    return False

def handle_session_start(session_id):
    """Handle session start event"""
    global error_free_count
    error_free_count = 0
    
    # Start new session in stats tracker
    stats_tracker.start_session(session_id)
    
    # Reset combo tracker for new session
    combo_tracker.reset()
    
    # Play session start sound
    play_sound_async("session_start.wav")

def handle_session_end():
    """Handle session end event"""
    # End session in stats tracker
    stats_tracker.end_session()
    
    # Play session end sound
    play_sound_async("session_night.wav")

def handle_tool_execution(tool_name, is_success):
    """Handle tool execution with all systems"""
    global error_free_count
    
    sounds_to_play = []
    
    # 1. Record in statistics
    stats_tracker.record_command(tool_name, is_success)
    
    # 2. Update error-free counter
    if is_success:
        error_free_count += 1
    else:
        error_free_count = 0
    
    # 3. Check combo status
    combo_sound, break_sound = combo_tracker.record_action(is_success)
    if combo_sound:
        sounds_to_play.append(combo_sound)
    elif break_sound:
        sounds_to_play.append(break_sound)
    
    # 4. Check achievements
    if stats_tracker.current_session:
        total_commands = stats_tracker.all_time_stats.total_commands + \
                        stats_tracker.current_session.total_commands
        current_streak = combo_tracker.state.current_streak
        tools_used = len(stats_tracker.current_session.tools_used)
        
        unlocked = achievement_manager.check_command_achievements(
            total_commands, current_streak, error_free_count, tools_used
        )
        
        # Play achievement sounds (limit to first achievement to avoid cacophony)
        if unlocked:
            achievement, sound = unlocked[0]
            sounds_to_play.append(sound)
            
            # Log achievement unlock (could display notification in future)
            with open("/tmp/zelda_achievements.log", "a") as f:
                f.write(f"🏆 Achievement Unlocked: {achievement.name} {achievement.icon}\n")
    
    return sounds_to_play

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    
    # Extract relevant information
    hook_event = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")
    tool_response = input_data.get("tool_response", {})
    session_id = input_data.get("session_id", "")
    
    # Handle different hook events
    if hook_event == "SessionStart":
        handle_session_start(session_id)
    
    elif hook_event == "Stop":
        handle_session_end()
    
    elif hook_event == "PostToolUse" and tool_name:
        # Get base tool sound and success status
        tool_sound, is_success = get_tool_sound(tool_name, tool_response)
        
        # Get all sounds to play (tool, combo, achievement)
        additional_sounds = handle_tool_execution(tool_name, is_success)
        
        # Play tool sound first, then additional sounds
        all_sounds = [tool_sound] + additional_sounds
        play_multiple_sounds(all_sounds)
    
    elif hook_event == "PreToolUse" and tool_name:
        # Play start sound for certain tools
        if tool_name == "Bash":
            play_sound_async("item_small.wav")
        elif tool_name == "Task":
            play_sound_async("notification.wav")
    
    elif hook_event in HOOK_EVENT_SOUNDS:
        # Hook event specific sounds
        play_sound_async(HOOK_EVENT_SOUNDS[hook_event])
    
    sys.exit(0)

if __name__ == "__main__":
    main()