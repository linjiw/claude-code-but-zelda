#!/usr/bin/env python3
"""
Unified Zelda Hook for Claude Code
Handles all Zelda features: sounds, stats, combos, achievements, and commands
With performance optimizations for faster response times
"""

import json
import sys
import subprocess
import time
import platform
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from zelda_core import get_manager

# Performance optimizations (lazy loaded)
_optimizations = None

def get_optimizations():
    """Lazy load performance optimizations"""
    global _optimizations
    if _optimizations is None:
        try:
            from performance_optimizations import initialize_optimizations
            _optimizations = initialize_optimizations(SOUNDS_DIR)
        except ImportError:
            # Fallback if optimizations not available
            _optimizations = {}
    return _optimizations

# Get the sounds directory
SOUNDS_DIR = Path(__file__).parent.parent / "sounds"

# Tool-to-sound mapping
TOOL_SOUND_MAP = {
    "Read": {"success": "file_open.wav", "error": "error.wav"},
    "Write": {"success": "file_create.wav", "error": "build_error.wav"},
    "Edit": {"success": "item_small.wav", "error": "error.wav"},
    "MultiEdit": {"success": "achievement.wav", "error": "build_error.wav"},
    "NotebookEdit": {"success": "puzzle_solved.wav", "error": "error.wav"},
    "Grep": {"success": "search_found.wav", "no_results": "search_complete.wav", "error": "error.wav"},
    "Glob": {"success": "search_found.wav", "error": "error.wav"},
    "LS": {"success": "menu_select.wav", "error": "error.wav"},
    "Bash": {"start": "item_small.wav", "success": "success.wav", "error": "damage.wav"},
    "Task": {"start": "session_start.wav", "success": "shrine_complete.wav", "error": "game_over.wav"},
    "WebFetch": {"success": "search_found.wav", "error": "error.wav"},
    "WebSearch": {"success": "search_complete.wav", "error": "error.wav"},
    "TodoWrite": {"success": "todo_complete.wav", "completed": "heart_get.wav", "all_complete": "achievement.wav"},
    "ExitPlanMode": {"success": "menu_select.wav"},
}

# Hook event sounds
HOOK_EVENT_SOUNDS = {
    "Notification": "warning.wav",
    "Stop": "session_night.wav",
    "SubagentStop": "shrine_complete.wav",
    "SessionStart": "session_start.wav",
    "PreCompact": "menu_select.wav"
}

# Get manager instance
manager = get_manager()

def play_sound_async(sound_file):
    """Play a sound file asynchronously with caching support"""
    opts = get_optimizations()
    
    # Use cached sound path if available
    if "sound_cache" in opts:
        sound_path = opts["sound_cache"].get_sound_path_or_cache(sound_file)
        if not sound_path:
            return
    else:
        sound_path = SOUNDS_DIR / sound_file
        if not sound_path.exists():
            return
    
    if manager.config["sounds"]["enabled"]:
        volume = manager.config.get("volume", 100) / 100.0
        # Cross-platform audio playback
        system = platform.system()
        
        try:
            if system == 'Darwin':  # macOS
                subprocess.Popen(
                    ["afplay", str(sound_path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            elif system == 'Linux':
                # Try multiple Linux audio players in order of preference
                players = ['aplay', 'paplay', 'ffplay', 'mpg123']
                for player in players:
                    try:
                        if player == 'ffplay':
                            subprocess.Popen(
                                [player, '-nodisp', '-autoexit', str(sound_path)],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL
                            )
                        else:
                            subprocess.Popen(
                                [player, str(sound_path)],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL
                            )
                        break  # Success, exit the loop
                    except FileNotFoundError:
                        continue  # Try next player
            elif system == 'Windows':
                # Windows PowerShell command
                ps_command = f'''
                Start-Job -ScriptBlock {{
                    Add-Type -TypeDefinition @"
                    using System.Media;
                    public class Sound {{
                        public static void Play(string file) {{
                            var player = new SoundPlayer(file);
                            player.Play();
                        }}
                    }}
"@
                    [Sound]::Play("{str(sound_path)}")
                }}
                '''
                subprocess.Popen(
                    ['powershell', '-Command', ps_command],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        except Exception:
            # Silently fail - don't interrupt workflow
            pass

def play_multiple_sounds(sounds):
    """Play multiple sounds with slight delay"""
    for i, sound in enumerate(sounds):
        if sound and manager.config["sounds"]["enabled"]:
            if i > 0:
                subprocess.Popen(["sleep", "0.2"]).wait()
            play_sound_async(sound)

def determine_tool_success(tool_name, response):
    """Determine if tool execution was successful"""
    if isinstance(response, dict):
        if response.get("success") is False or "error" in response:
            return False
        if "exitCode" in response:
            return response["exitCode"] == 0
    elif isinstance(response, str):
        return not any(word in response.lower() for word in ["error", "failed", "exception"])
    return True

def get_tool_sound(tool_name, response):
    """Get appropriate sound for tool execution"""
    if tool_name not in TOOL_SOUND_MAP:
        return "success.wav" if determine_tool_success(tool_name, response) else "error.wav"
    
    tool_sounds = TOOL_SOUND_MAP[tool_name]
    is_success = determine_tool_success(tool_name, response)
    
    # Special cases
    if tool_name == "TodoWrite" and isinstance(response, dict) and "todos" in response:
        todos = response["todos"]
        completed = sum(1 for t in todos if t.get("status") == "completed")
        if completed == len(todos) and completed > 0:
            return tool_sounds.get("all_complete", "achievement.wav")
        elif completed > 0:
            return tool_sounds.get("completed", "heart_get.wav")
    
    return tool_sounds.get("success" if is_success else "error", "success.wav" if is_success else "error.wav")

def handle_user_prompt(prompt):
    """Handle user prompts, intercepting @zelda commands"""
    # Check if this is a @zelda command
    if prompt.strip().lower().startswith("@zelda"):
        # Process the command
        response = manager.process_command(prompt.strip())
        
        if response:
            # Return the formatted response for Claude to display
            output = {
                "decision": "block",  # Prevent the prompt from being processed normally
                "reason": response,   # This will be shown to the user
                "suppressOutput": True
            }
            print(json.dumps(output))
            sys.exit(0)
    
    # Not a @zelda command, let it proceed normally
    sys.exit(0)

def handle_tool_execution(tool_name, response):
    """Handle tool execution events with debouncing"""
    opts = get_optimizations()
    
    # Check debouncer if available
    if "debouncer" in opts:
        if not opts["debouncer"].should_process(tool_name):
            # Skip if command was executed too recently
            return
    
    # Performance monitoring start
    start_time = time.time() if "monitor" in opts else None
    
    # Determine success
    is_success = determine_tool_success(tool_name, response)
    
    # Get base sound
    tool_sound = get_tool_sound(tool_name, response)
    
    # Record command and get additional sounds (combo, achievements)
    additional_sounds = manager.record_command(tool_name, is_success)
    
    # Play all sounds
    all_sounds = [tool_sound] + additional_sounds
    play_multiple_sounds(all_sounds)
    
    # Record performance metrics
    if start_time and "monitor" in opts:
        duration_ms = (time.time() - start_time) * 1000
        opts["monitor"].record_timing("hook_execution_times", duration_ms)

def handle_session_start(session_id):
    """Handle session start"""
    manager.start_session(session_id)
    play_sound_async("session_start.wav")
    
    # Check for notifications
    notifications_file = Path("/tmp/zelda_notifications.log")
    if notifications_file.exists():
        # Clear old notifications
        notifications_file.unlink()

def handle_session_end():
    """Handle session end"""
    manager.end_session()
    play_sound_async("session_night.wav")

def main():
    """Main hook handler"""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    
    # Extract event information
    hook_event = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")
    tool_response = input_data.get("tool_response", {})
    session_id = input_data.get("session_id", "")
    prompt = input_data.get("prompt", "")
    
    # Handle different events
    if hook_event == "UserPromptSubmit":
        handle_user_prompt(prompt)
    
    elif hook_event == "SessionStart":
        handle_session_start(session_id)
    
    elif hook_event == "Stop":
        handle_session_end()
    
    elif hook_event == "PostToolUse" and tool_name:
        handle_tool_execution(tool_name, tool_response)
    
    elif hook_event == "PreToolUse" and tool_name:
        # Play start sounds for certain tools
        if tool_name == "Bash":
            play_sound_async("item_small.wav")
        elif tool_name == "Task":
            play_sound_async("notification.wav")
    
    elif hook_event in HOOK_EVENT_SOUNDS:
        play_sound_async(HOOK_EVENT_SOUNDS[hook_event])
    
    # Check for notifications to display
    notifications_file = Path("/tmp/zelda_notifications.log")
    if notifications_file.exists():
        try:
            with open(notifications_file, 'r') as f:
                notifications = f.read().strip()
            
            if notifications and hook_event == "Stop":
                # Display notifications at session end
                for line in notifications.split('\n'):
                    if line.startswith("ACHIEVEMENT:"):
                        achievement = line.replace("ACHIEVEMENT:", "").strip()
                        # Could return this to Claude Code somehow
                
                # Clear notifications after displaying
                notifications_file.unlink()
        except:
            pass
    
    sys.exit(0)

if __name__ == "__main__":
    main()