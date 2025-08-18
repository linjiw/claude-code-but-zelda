#!/usr/bin/env python3
"""
Test cross-platform support in zelda_hook.py
Verifies that the hook correctly detects and uses the appropriate audio player for each platform
"""

import json
import subprocess
import sys
import platform
from pathlib import Path

def test_hook_platform_detection():
    """Test that the hook works on the current platform"""
    print(f"Testing on platform: {platform.system()}")
    
    # Test data for hook
    test_events = [
        {
            "name": "SessionStart",
            "data": {"hook_event_name": "SessionStart", "session_id": "test-session"}
        },
        {
            "name": "TodoWrite Success",
            "data": {
                "hook_event_name": "PostToolUse",
                "tool_name": "TodoWrite",
                "tool_response": {"todos": [{"status": "completed"}]}
            }
        },
        {
            "name": "Bash Error",
            "data": {
                "hook_event_name": "PostToolUse",
                "tool_name": "Bash",
                "tool_response": {"exitCode": 1, "error": "Command failed"}
            }
        }
    ]
    
    hook_path = Path(__file__).parent / "hooks" / "zelda_hook.py"
    
    all_passed = True
    for test in test_events:
        print(f"\nTesting: {test['name']}")
        
        # Run hook with test data
        proc = subprocess.Popen(
            [sys.executable, str(hook_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = proc.communicate(json.dumps(test['data']).encode())
        
        # Check if hook executed without crashing
        if proc.returncode != 0:
            print(f"  ❌ Failed with exit code {proc.returncode}")
            if stderr:
                print(f"  Error: {stderr.decode()}")
            all_passed = False
        else:
            print(f"  ✅ Passed (exit code 0)")
            
        # Check for platform-specific errors
        if stderr and b"FileNotFoundError" in stderr:
            if b"afplay" in stderr and platform.system() != "Darwin":
                print(f"  ❌ ERROR: Trying to use afplay on {platform.system()}")
                all_passed = False
            elif b"aplay" in stderr and platform.system() != "Linux":
                print(f"  ❌ ERROR: Trying to use aplay on {platform.system()}")
                all_passed = False
    
    return all_passed

def verify_audio_player_availability():
    """Check which audio players are available on the system"""
    print("\n" + "="*50)
    print("Audio Player Availability Check")
    print("="*50)
    
    system = platform.system()
    print(f"Current platform: {system}")
    
    if system == "Darwin":
        players = ["afplay"]
    elif system == "Linux":
        players = ["aplay", "paplay", "ffplay", "mpg123"]
    elif system == "Windows":
        players = ["powershell"]
    else:
        print("Unknown platform")
        return
    
    print("\nChecking for audio players:")
    for player in players:
        try:
            # Use 'which' on Unix-like systems, 'where' on Windows
            cmd = "where" if system == "Windows" else "which"
            result = subprocess.run(
                [cmd, player],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  ✅ {player}: Found at {result.stdout.strip()}")
            else:
                print(f"  ❌ {player}: Not found")
        except Exception as e:
            print(f"  ❌ {player}: Error checking - {e}")

def main():
    """Run all tests"""
    print("="*50)
    print("Cross-Platform Hook Test Suite")
    print("="*50)
    
    # First check available audio players
    verify_audio_player_availability()
    
    # Then test the hook
    print("\n" + "="*50)
    print("Testing Hook Execution")
    print("="*50)
    
    if test_hook_platform_detection():
        print("\n✅ All tests passed!")
        print("The hook correctly handles the current platform.")
        return 0
    else:
        print("\n❌ Some tests failed!")
        print("Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())