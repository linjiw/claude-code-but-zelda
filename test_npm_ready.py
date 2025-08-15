#!/usr/bin/env python3
"""
NPM Publishing Readiness Test
Quick validation that everything is ready for npm publish
"""

import json
import os
import sys
import subprocess
from pathlib import Path

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'

def print_test(name, passed, details=""):
    symbol = "✅" if passed else "❌"
    color = GREEN if passed else RED
    print(f"{color}{symbol} {name}{NC}")
    if details and not passed:
        print(f"   {details}")
    return passed

def test_npm_package():
    """Test npm package configuration"""
    print("\n📦 NPM Package Tests:")
    all_passed = True
    
    # Check package.json
    package_path = Path("package.json")
    if not package_path.exists():
        return print_test("package.json exists", False, "File not found")
    
    with open(package_path) as f:
        package = json.load(f)
    
    all_passed &= print_test("package.json valid", True)
    all_passed &= print_test("Version is 3.0.0", package.get("version") == "3.0.0")
    all_passed &= print_test("Name is correct", package.get("name") == "zelda-claude-code")
    all_passed &= print_test("Has bin entry", "bin" in package)
    all_passed &= print_test("Has postinstall", "postinstall" in package.get("scripts", {}))
    
    return all_passed

def test_core_files():
    """Test that core files exist"""
    print("\n📁 Core Files:")
    all_passed = True
    
    required_files = [
        "hooks/zelda_hook.py",
        "scripts/play_sound.py",
        "scripts/play_sound_async.py",
        "zelda_core.py",
        "postinstall.js",
        "universal_installer.py",
        "README.md",
        "CLAUDE.md"
    ]
    
    for file_path in required_files:
        exists = Path(file_path).exists()
        all_passed &= print_test(f"{file_path}", exists)
    
    return all_passed

def test_sounds():
    """Test that sounds exist"""
    print("\n🔊 Sound Files:")
    all_passed = True
    
    sounds_dir = Path("sounds")
    if not sounds_dir.exists():
        return print_test("sounds/ directory", False, "Directory not found")
    
    wav_files = list(sounds_dir.glob("*.wav"))
    all_passed &= print_test(f"Found {len(wav_files)} sound files", len(wav_files) > 0)
    
    # Check key sounds
    key_sounds = ["success.wav", "error.wav", "session_start.wav", "achievement.wav"]
    for sound in key_sounds:
        exists = (sounds_dir / sound).exists()
        all_passed &= print_test(f"  {sound}", exists)
    
    return all_passed

def test_python_compatibility():
    """Test Python compatibility"""
    print("\n🐍 Python Compatibility:")
    all_passed = True
    
    # Test Python version
    version = sys.version_info
    all_passed &= print_test(f"Python {version.major}.{version.minor}", version >= (3, 6))
    
    # Test hook can be imported
    try:
        import zelda_core
        all_passed &= print_test("zelda_core imports", True)
    except ImportError as e:
        all_passed &= print_test("zelda_core imports", False, str(e))
    
    return all_passed

def test_hook_execution():
    """Test hook can execute"""
    print("\n🪝 Hook Execution:")
    all_passed = True
    
    hook_path = Path("hooks/zelda_hook.py")
    if not hook_path.exists():
        return print_test("Hook exists", False)
    
    # Test with minimal input
    test_input = json.dumps({"hook_event_name": "test"})
    
    try:
        result = subprocess.run(
            ["python3", str(hook_path)],
            input=test_input,
            text=True,
            capture_output=True,
            timeout=3
        )
        all_passed &= print_test("Hook executes without error", result.returncode == 0)
    except subprocess.TimeoutExpired:
        all_passed &= print_test("Hook executes without error", False, "Timeout")
    except Exception as e:
        all_passed &= print_test("Hook executes without error", False, str(e))
    
    return all_passed

def test_claude_integration():
    """Test Claude Code integration readiness"""
    print("\n🔗 Claude Code Integration:")
    all_passed = True
    
    settings_path = Path.home() / ".claude" / "settings.json"
    
    if settings_path.exists():
        try:
            with open(settings_path) as f:
                settings = json.load(f)
            
            has_hooks = "hooks" in settings
            all_passed &= print_test("Settings has hooks", has_hooks)
            
            if has_hooks:
                has_post_tool = "PostToolUse" in settings["hooks"]
                all_passed &= print_test("PostToolUse configured", has_post_tool)
                
                if has_post_tool:
                    post_tool = settings["hooks"]["PostToolUse"]
                    is_valid = isinstance(post_tool, (list, str))
                    all_passed &= print_test("Hook format valid", is_valid)
        except Exception as e:
            all_passed &= print_test("Settings valid JSON", False, str(e))
    else:
        print_test("Settings file exists", True, "Will be created on install")
    
    return all_passed

def main():
    print("=" * 50)
    print("🎮 Zelda Claude Code - NPM Publishing Readiness")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run all test categories
    all_tests_passed &= test_npm_package()
    all_tests_passed &= test_core_files()
    all_tests_passed &= test_sounds()
    all_tests_passed &= test_python_compatibility()
    all_tests_passed &= test_hook_execution()
    all_tests_passed &= test_claude_integration()
    
    # Summary
    print("\n" + "=" * 50)
    if all_tests_passed:
        print(f"{GREEN}✅ ALL TESTS PASSED - Ready for NPM publish!{NC}")
        print(f"\nRun: ./publish_npm.sh")
        return 0
    else:
        print(f"{RED}❌ Some tests failed - Please fix before publishing{NC}")
        return 1

if __name__ == "__main__":
    sys.exit(main())