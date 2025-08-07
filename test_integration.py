#!/usr/bin/env python3
"""
End-to-end integration test for Zelda Claude Code
Simulates actual user interactions with the system
"""

import json
import subprocess
import sys
from pathlib import Path

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
    print("🎮 Zelda Claude Code - End-to-End Integration Test")
    print("="*60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Help command
    print("\n1️⃣  Testing @zelda help...")
    response = test_zelda_command("@zelda help")
    if response and "Available Commands" in response:
        print("   ✅ Help command works")
        tests_passed += 1
    else:
        print("   ❌ Help command failed")
        tests_failed += 1
    
    # Test 2: Stats command
    print("\n2️⃣  Testing @zelda stats...")
    response = test_zelda_command("@zelda stats")
    if response and "Coding Statistics" in response:
        print("   ✅ Stats command works")
        tests_passed += 1
    else:
        print("   ❌ Stats command failed")
        tests_failed += 1
    
    # Test 3: Achievements command
    print("\n3️⃣  Testing @zelda achievements...")
    response = test_zelda_command("@zelda achievements")
    if response and "Achievements" in response:
        print("   ✅ Achievements command works")
        tests_passed += 1
    else:
        print("   ❌ Achievements command failed")
        tests_failed += 1
    
    # Test 4: Combo command
    print("\n4️⃣  Testing @zelda combo...")
    response = test_zelda_command("@zelda combo")
    if response and "Combo" in response:
        print("   ✅ Combo command works")
        tests_passed += 1
    else:
        print("   ❌ Combo command failed")
        tests_failed += 1
    
    # Test 5: Config command
    print("\n5️⃣  Testing @zelda config...")
    response = test_zelda_command("@zelda config")
    if response and "Configuration" in response:
        print("   ✅ Config view works")
        tests_passed += 1
    else:
        print("   ❌ Config view failed")
        tests_failed += 1
    
    # Test 6: Config update
    print("\n6️⃣  Testing @zelda config volume 75...")
    response = test_zelda_command("@zelda config volume 75")
    if response and ("updated" in response.lower() or "set" in response.lower()):
        print("   ✅ Config update works")
        tests_passed += 1
    else:
        print("   ❌ Config update failed")
        tests_failed += 1
    
    # Test 7: Tool execution hook
    print("\n7️⃣  Testing PostToolUse hook...")
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
        print("   ✅ PostToolUse hook works")
        tests_passed += 1
    else:
        print("   ❌ PostToolUse hook failed")
        tests_failed += 1
    
    # Test 8: Session start hook
    print("\n8️⃣  Testing SessionStart hook...")
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
        print("   ✅ SessionStart hook works")
        tests_passed += 1
    else:
        print("   ❌ SessionStart hook failed")
        tests_failed += 1
    
    # Test 9: Sound files exist
    print("\n9️⃣  Testing sound files...")
    sound_dir = Path("sounds")
    essential_sounds = ["success.wav", "error.wav", "todo_complete.wav", "achievement.wav"]
    all_exist = all((sound_dir / s).exists() for s in essential_sounds)
    
    if all_exist:
        print("   ✅ Essential sound files exist")
        tests_passed += 1
    else:
        print("   ❌ Some sound files missing")
        tests_failed += 1
    
    # Test 10: Demo script
    print("\n🔟  Testing demo script...")
    if Path("demo_sounds.sh").exists():
        print("   ✅ Demo script exists")
        tests_passed += 1
    else:
        print("   ❌ Demo script missing")
        tests_failed += 1
    
    # Summary
    print("\n" + "="*60)
    print(f"INTEGRATION TEST RESULTS: {tests_passed}/{tests_passed + tests_failed} passed")
    
    if tests_failed == 0:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("\nThe Zelda Claude Code system is fully functional!")
        print("Users can now:")
        print("  • Use @zelda commands in Claude Code")
        print("  • Get sound feedback for their actions")
        print("  • Track statistics and achievements")
        print("  • Build combo streaks")
        print("\nMay the Triforce guide your code! 🗡️✨")
        return 0
    else:
        print(f"⚠️  {tests_failed} integration tests failed")
        print("Please review the failures above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())