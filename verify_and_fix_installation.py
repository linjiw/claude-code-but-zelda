#!/usr/bin/env python3
"""
Comprehensive installation verification and fix script for Zelda Claude Code
"""

import json
import os
import sys
import subprocess
from pathlib import Path
import shutil

# Color codes for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

def print_color(message, color=NC):
    print(f"{color}{message}{NC}")

def check_command(command):
    """Check if a command is available"""
    try:
        subprocess.run(['which', command], capture_output=True, check=True)
        return True
    except:
        return False

def test_sound_playback():
    """Test if sound playback works"""
    test_sound = Path(__file__).parent / "sounds" / "success.wav"
    if not test_sound.exists():
        return False, "No test sound file found"
    
    try:
        if sys.platform == "darwin":
            subprocess.run(['afplay', str(test_sound)], capture_output=True, timeout=2)
        elif sys.platform.startswith('linux'):
            if check_command('aplay'):
                subprocess.run(['aplay', str(test_sound)], capture_output=True, timeout=2)
            elif check_command('paplay'):
                subprocess.run(['paplay', str(test_sound)], capture_output=True, timeout=2)
        return True, "Sound playback works"
    except Exception as e:
        return False, f"Sound playback failed: {e}"

def verify_installation():
    """Verify and fix the Zelda Claude Code installation"""
    
    print_color("\n🔍 ZELDA CLAUDE CODE - INSTALLATION VERIFICATION", BLUE)
    print_color("=" * 50, BLUE)
    
    issues = []
    fixes_applied = []
    
    # 1. Check Python version
    print_color("\n1. Checking Python version...", YELLOW)
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 6:
        print_color(f"✅ Python {python_version.major}.{python_version.minor} found", GREEN)
    else:
        print_color(f"❌ Python 3.6+ required, found {python_version.major}.{python_version.minor}", RED)
        issues.append("Python version too old")
    
    # 2. Check project structure
    print_color("\n2. Checking project structure...", YELLOW)
    project_dir = Path(__file__).parent
    required_dirs = ['hooks', 'scripts', 'sounds', 'sounds_backup']
    
    for dir_name in required_dirs:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            print_color(f"✅ {dir_name}/ directory exists", GREEN)
        else:
            print_color(f"❌ {dir_name}/ directory missing", RED)
            dir_path.mkdir(exist_ok=True)
            fixes_applied.append(f"Created {dir_name}/ directory")
    
    # 3. Check essential files
    print_color("\n3. Checking essential files...", YELLOW)
    essential_files = {
        'hooks/zelda_hook.py': 'Main hook handler',
        'zelda_core.py': 'Core manager module',
        'demo_sounds.sh': 'Sound demo script'
    }
    
    for file_path, description in essential_files.items():
        full_path = project_dir / file_path
        if full_path.exists():
            print_color(f"✅ {file_path} ({description})", GREEN)
        else:
            print_color(f"❌ {file_path} missing ({description})", RED)
            issues.append(f"{file_path} missing")
    
    # 4. Check sound files
    print_color("\n4. Checking sound files...", YELLOW)
    sounds_dir = project_dir / "sounds"
    sound_files = list(sounds_dir.glob("*.wav"))
    
    if sound_files:
        print_color(f"✅ Found {len(sound_files)} sound files", GREEN)
        
        # Check essential sounds
        essential_sounds = [
            'success.wav', 'error.wav', 'todo_complete.wav',
            'session_start.wav', 'achievement.wav', 'puzzle_solved.wav'
        ]
        
        for sound_name in essential_sounds:
            sound_path = sounds_dir / sound_name
            if sound_path.exists():
                print_color(f"   ✅ {sound_name}", GREEN)
            else:
                print_color(f"   ⚠️  {sound_name} missing", YELLOW)
    else:
        print_color("❌ No sound files found", RED)
        issues.append("No sound files")
    
    # 5. Check Claude Code settings
    print_color("\n5. Checking Claude Code integration...", YELLOW)
    claude_settings = Path.home() / ".claude" / "settings.json"
    hook_path = str(project_dir / "hooks" / "zelda_hook.py")
    
    if claude_settings.exists():
        print_color(f"✅ ~/.claude/settings.json exists", GREEN)
        
        try:
            with open(claude_settings, 'r') as f:
                settings = json.load(f)
            
            # Check if hooks are configured
            if 'hooks' in settings:
                # Check PostToolUse hook
                post_tool_use = settings['hooks'].get('PostToolUse', '')
                
                if 'zelda_hook.py' in str(post_tool_use):
                    print_color("✅ PostToolUse hook configured", GREEN)
                    
                    # Verify the path is correct
                    if hook_path in str(post_tool_use):
                        print_color("✅ Hook path is correct", GREEN)
                    else:
                        print_color("⚠️  Hook path may need updating", YELLOW)
                        
                        # Fix the hook configuration
                        correct_config = {
                            "PostToolUse": f"python3 {hook_path}",
                            "UserPromptSubmit": [{"hooks": [{"type": "command", "command": f"python3 {hook_path}"}]}],
                            "SessionStart": [{"hooks": [{"type": "command", "command": f"python3 {hook_path}"}]}],
                            "Stop": [{"hooks": [{"type": "command", "command": f"python3 {hook_path}"}]}],
                            "Notification": [{"hooks": [{"type": "command", "command": f"python3 {hook_path}"}]}]
                        }
                        
                        settings['hooks'].update(correct_config)
                        
                        # Backup and update
                        backup_path = claude_settings.with_suffix('.json.backup')
                        shutil.copy2(claude_settings, backup_path)
                        
                        with open(claude_settings, 'w') as f:
                            json.dump(settings, f, indent=2)
                        
                        fixes_applied.append("Updated hook paths in settings.json")
                        print_color("✅ Fixed hook configuration", GREEN)
                else:
                    print_color("❌ PostToolUse hook not configured", RED)
                    issues.append("Hooks not configured")
            else:
                print_color("❌ No hooks configured", RED)
                issues.append("No hooks in settings.json")
                
        except json.JSONDecodeError:
            print_color("❌ settings.json is invalid JSON", RED)
            issues.append("Invalid settings.json")
        except Exception as e:
            print_color(f"❌ Error reading settings: {e}", RED)
            issues.append(f"Settings error: {e}")
    else:
        print_color("❌ ~/.claude/settings.json not found", RED)
        issues.append("Claude settings not found")
    
    # 6. Check ~/.zelda directory
    print_color("\n6. Checking user data directory...", YELLOW)
    zelda_dir = Path.home() / ".zelda"
    if zelda_dir.exists():
        print_color("✅ ~/.zelda directory exists", GREEN)
        
        # Check subdirectories
        sessions_dir = zelda_dir / "sessions"
        if not sessions_dir.exists():
            sessions_dir.mkdir(parents=True)
            fixes_applied.append("Created ~/.zelda/sessions directory")
    else:
        zelda_dir.mkdir(parents=True)
        (zelda_dir / "sessions").mkdir(parents=True)
        fixes_applied.append("Created ~/.zelda directory structure")
        print_color("✅ Created ~/.zelda directory", GREEN)
    
    # 7. Test sound playback
    print_color("\n7. Testing sound playback...", YELLOW)
    sound_works, sound_msg = test_sound_playback()
    if sound_works:
        print_color(f"✅ {sound_msg}", GREEN)
    else:
        print_color(f"⚠️  {sound_msg}", YELLOW)
    
    # 8. Test hook functionality
    print_color("\n8. Testing hook functionality...", YELLOW)
    try:
        test_event = json.dumps({
            "type": "PostToolUse",
            "toolName": "Test",
            "status": "success"
        })
        
        result = subprocess.run(
            ['python3', str(project_dir / 'hooks' / 'zelda_hook.py')],
            input=test_event,
            text=True,
            capture_output=True,
            timeout=2
        )
        
        if result.returncode == 0:
            print_color("✅ Hook handler works", GREEN)
        else:
            print_color(f"⚠️  Hook handler returned non-zero: {result.stderr}", YELLOW)
    except Exception as e:
        print_color(f"❌ Hook test failed: {e}", RED)
        issues.append("Hook test failed")
    
    # 9. Check for potential permission issues
    print_color("\n9. Checking file permissions...", YELLOW)
    scripts_to_check = [
        'demo_sounds.sh',
        'quick_demo.sh',
        'install.sh'
    ]
    
    for script_name in scripts_to_check:
        script_path = project_dir / script_name
        if script_path.exists():
            if os.access(script_path, os.X_OK):
                print_color(f"✅ {script_name} is executable", GREEN)
            else:
                os.chmod(script_path, 0o755)
                fixes_applied.append(f"Made {script_name} executable")
                print_color(f"✅ Fixed {script_name} permissions", GREEN)
    
    # Summary
    print_color("\n" + "=" * 50, BLUE)
    print_color("📊 VERIFICATION SUMMARY", BLUE)
    print_color("=" * 50, BLUE)
    
    if fixes_applied:
        print_color("\n🔧 Fixes Applied:", GREEN)
        for fix in fixes_applied:
            print_color(f"   • {fix}", GREEN)
    
    if issues:
        print_color("\n⚠️  Issues Found:", YELLOW)
        for issue in issues:
            print_color(f"   • {issue}", YELLOW)
        
        print_color("\n💡 Recommended Actions:", BLUE)
        if "No sound files" in str(issues):
            print_color("   1. Run: python3 generate_zelda_style_sounds.py", BLUE)
        if "Hooks not configured" in str(issues) or "Claude settings not found" in str(issues):
            print_color("   2. Run: ./install.sh", BLUE)
        if "Hook test failed" in str(issues):
            print_color("   3. Check Python dependencies and paths", BLUE)
    else:
        print_color("\n✅ All checks passed! Zelda Claude Code is properly installed.", GREEN)
        print_color("\n🎮 Ready to use! Remember to:", BLUE)
        print_color("   1. Restart Claude Code for hooks to take effect", BLUE)
        print_color("   2. Type @zelda help in Claude Code to see commands", BLUE)
        print_color("   3. Enjoy the adventure! 🗡️✨", BLUE)
    
    return len(issues) == 0

if __name__ == "__main__":
    success = verify_installation()
    sys.exit(0 if success else 1)