#!/usr/bin/env python3
"""
End-to-end integration test for Zelda Claude Code
Simulates actual user interactions with the system
"""

import json
import subprocess
import sys
import os
import platform
from pathlib import Path

# Force UTF-8 encoding for Windows
if platform.system() == 'Windows':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def run_command(cmd):
    """Run a shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def test_zelda_command(command):
    """Test a @zelda command through the hook"""
    input_data = json.dumps({
        "hook_event_name": "UserPromptSubmit",
        "prompt": command
    })
    
    result = subprocess.run(
        ["python3", "hooks/zelda_hook.py"],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0 and result.stdout:
        output = json.loads(result.stdout)
        if output.get('decision') == 'block':
            return output.get('reason', 'Command processed')
    return None

def main():
    # Use ASCII for CI environments
    if os.environ.get('CI'):
        print("[GAME] Zelda Claude Code - End-to-End Integration Test")
    else:
        print("🎮 Zelda Claude Code - End-to-End Integration Test")
    print("="*60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Help command
    print("\n[1] Testing @zelda help...")
    response = test_zelda_command("@zelda help")
    if response and "Available Commands" in response:
        print("   [PASS] Help command works")
        tests_passed += 1
    else:
        print("   [FAIL] Help command failed")
        tests_failed += 1
    
    # Test 2: Stats command
    print("\n[2] Testing @zelda stats...")
    response = test_zelda_command("@zelda stats")
    if response and "Coding Statistics" in response:
        print("   [PASS] Stats command works")
        tests_passed += 1
    else:
        print("   [FAIL] Stats command failed")
        tests_failed += 1
    
    # Test 3: Achievements command
    print("\n[3] Testing @zelda achievements...")
    response = test_zelda_command("@zelda achievements")
    if response and "Achievements" in response:
        print("   [PASS] Achievements command works")
        tests_passed += 1
    else:
        print("   [FAIL] Achievements command failed")
        tests_failed += 1
    
    # Test 4: Combo command
    print("\n[4] Testing @zelda combo...")
    response = test_zelda_command("@zelda combo")
    if response and "Combo" in response:
        print("   [PASS] Combo command works")
        tests_passed += 1
    else:
        print("   [FAIL] Combo command failed")
        tests_failed += 1
    
    # Test 5: Config command
    print("\n[5] Testing @zelda config...")
    response = test_zelda_command("@zelda config")
    if response and "Configuration" in response:
        print("   [PASS] Config view works")
        tests_passed += 1
    else:
        print("   [FAIL] Config view failed")
        tests_failed += 1
    
    # Test 6: Config update
    print("\n[6] Testing @zelda config volume 75...")
    response = test_zelda_command("@zelda config volume 75")
    if response and ("updated" in response.lower() or "set" in response.lower()):
        print("   [PASS] Config update works")
        tests_passed += 1
    else:
        print("   [FAIL] Config update failed")
        tests_failed += 1
    
    # Test 7: Tool execution hook
    print("\n[7] Testing PostToolUse hook...")
    input_data = json.dumps({
        "hook_event_name": "PostToolUse",
        "tool_name": "Bash",
        "tool_status": "success"
    })
    
    result = subprocess.run(
        ["python3", "hooks/zelda_hook.py"],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("   [PASS] PostToolUse hook works")
        tests_passed += 1
    else:
        print("   [FAIL] PostToolUse hook failed")
        tests_failed += 1
    
    # Test 8: Session start hook
    print("\n[8] Testing SessionStart hook...")
    input_data = json.dumps({
        "hook_event_name": "SessionStart"
    })
    
    result = subprocess.run(
        ["python3", "hooks/zelda_hook.py"],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("   [PASS] SessionStart hook works")
        tests_passed += 1
    else:
        print("   [FAIL] SessionStart hook failed")
        tests_failed += 1
    
    # Test 9: Sound files exist
    print("\n[9] Testing sound files...")
    sound_dir = Path("sounds")
    essential_sounds = ["success.wav", "error.wav", "todo_complete.wav", "achievement.wav"]
    all_exist = all((sound_dir / s).exists() for s in essential_sounds)
    
    if all_exist:
        print("   [PASS] Essential sound files exist")
        tests_passed += 1
    else:
        print("   [FAIL] Some sound files missing")
        tests_failed += 1
    
    # Test 10: Demo script
    print("\n[10] Testing demo script...")
    if Path("demo_sounds.sh").exists():
        print("   [PASS] Demo script exists")
        tests_passed += 1
    else:
        print("   [FAIL] Demo script missing")
        tests_failed += 1
    
    # Summary
    print("\n" + "="*60)
    print(f"INTEGRATION TEST RESULTS: {tests_passed}/{tests_passed + tests_failed} passed")
    
    if tests_failed == 0:
        if os.environ.get('CI'):
            print("[SUCCESS] ALL INTEGRATION TESTS PASSED!")
        else:
            print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("\nThe Zelda Claude Code system is fully functional!")
        print("Users can now:")
        print("  - Use @zelda commands in Claude Code")
        print("  - Get sound feedback for their actions")
        print("  - Track statistics and achievements")
        print("  - Build combo streaks")
        if not os.environ.get('CI'):
            print("\nMay the Triforce guide your code! 🗡️✨")
        return 0
    else:
        if os.environ.get('CI'):
            print(f"[WARNING] {tests_failed} integration tests failed")
        else:
            print(f"⚠️  {tests_failed} integration tests failed")
        print("Please review the failures above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())