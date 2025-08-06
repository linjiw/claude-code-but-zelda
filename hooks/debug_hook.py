#!/usr/bin/env python3
"""
Debug hook to understand what Claude Code sends
"""

import json
import sys
from datetime import datetime

# Read JSON input from stdin
try:
    input_data = json.load(sys.stdin)
    
    # Log to file for debugging
    with open("/tmp/claude_hook_debug.log", "a") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"Hook Event: {input_data.get('hook_event_name', 'Unknown')}\n")
        f.write(f"Tool Name: {input_data.get('tool_name', 'Unknown')}\n")
        f.write(f"Full JSON:\n")
        f.write(json.dumps(input_data, indent=2))
        f.write(f"\n{'='*60}\n")
    
    # Also play sound based on simple logic
    import subprocess
    from pathlib import Path
    
    sounds_dir = Path(__file__).parent.parent / "sounds"
    tool_response = input_data.get("tool_response", {})
    
    # Simple success detection
    if isinstance(tool_response, str):
        # String response - check for common success patterns
        if any(word in tool_response.lower() for word in ["listed", "success", "created", "updated"]):
            sound = "success.wav"
        elif any(word in tool_response.lower() for word in ["error", "failed", "not found"]):
            sound = "error.wav"
        else:
            sound = "success.wav"  # Default to success
    else:
        # Assume success for non-string responses
        sound = "success.wav"
    
    sound_path = sounds_dir / sound
    if sound_path.exists():
        subprocess.Popen(
            ["afplay", str(sound_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    
except Exception as e:
    with open("/tmp/claude_hook_debug.log", "a") as f:
        f.write(f"ERROR: {e}\n")

# Always exit successfully
sys.exit(0)