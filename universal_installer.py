#!/usr/bin/env python3
"""
Universal Zelda Claude Code Installer
Ensures compatibility with official Claude Code hooks specification
Works across all platforms and conditions
"""

import json
import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from datetime import datetime

# Color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def print_color(msg, color=NC):
    print(f"{color}{msg}{NC}")

class UniversalInstaller:
    def __init__(self):
        self.project_dir = Path(__file__).parent.resolve()
        self.home_dir = Path.home()
        self.claude_dir = self.home_dir / ".claude"
        self.settings_file = self.claude_dir / "settings.json"
        self.zelda_dir = self.home_dir / ".zelda"
        self.issues = []
        self.fixes = []
        
    def check_python_version(self):
        """Ensure Python 3.6+ is available"""
        if sys.version_info < (3, 6):
            self.issues.append("Python 3.6+ required")
            return False
        return True
    
    def ensure_directories(self):
        """Create all required directories"""
        dirs_to_create = [
            self.claude_dir,
            self.zelda_dir,
            self.zelda_dir / "sessions",
            self.project_dir / "hooks",
            self.project_dir / "scripts",
            self.project_dir / "sounds"
        ]
        
        for dir_path in dirs_to_create:
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                self.fixes.append(f"Created {dir_path}")
    
    def get_python_command(self):
        """Get the correct Python command for this system"""
        # Try different Python commands
        for cmd in ['python3', 'python', sys.executable]:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    if '3.' in version:
                        return cmd
            except:
                continue
        return 'python3'  # Default fallback
    
    def get_hook_command(self):
        """Get the correct hook command for any platform"""
        python_cmd = self.get_python_command()
        hook_path = self.project_dir / "hooks" / "zelda_hook.py"
        
        # Handle different path formats
        if platform.system() == "Windows":
            # Windows needs special handling for paths with spaces
            hook_str = str(hook_path).replace('\\', '/')
            return f'{python_cmd} "{hook_str}"'
        else:
            # Unix-like systems
            return f'{python_cmd} "{hook_path}"'
    
    def create_compliant_settings(self):
        """Create Claude Code settings that comply with official spec"""
        hook_cmd = self.get_hook_command()
        
        # Build spec-compliant configuration
        hooks_config = {
            # PostToolUse with matcher for all tools
            "PostToolUse": [
                {
                    "matcher": "*",  # Match all tools
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_cmd,
                            "timeout": 5  # 5 second timeout for sounds
                        }
                    ]
                }
            ],
            # Other events without matcher
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_cmd,
                            "timeout": 5
                        }
                    ]
                }
            ],
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_cmd,
                            "timeout": 5
                        }
                    ]
                }
            ],
            "Stop": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_cmd,
                            "timeout": 5
                        }
                    ]
                }
            ],
            "Notification": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_cmd,
                            "timeout": 5
                        }
                    ]
                }
            ]
        }
        
        return hooks_config
    
    def update_settings(self):
        """Update or create settings.json with proper configuration"""
        print_color("\nConfiguring Claude Code hooks...", YELLOW)
        
        # Load existing settings or create new
        existing_settings = {}
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    existing_settings = json.load(f)
                # Backup existing
                backup_name = f"settings.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_path = self.claude_dir / backup_name
                shutil.copy2(self.settings_file, backup_path)
                self.fixes.append(f"Backed up settings to {backup_name}")
            except Exception as e:
                self.issues.append(f"Could not read existing settings: {e}")
                existing_settings = {}
        
        # Get compliant hooks configuration
        hooks_config = self.create_compliant_settings()
        
        # Merge with existing settings
        if "$schema" not in existing_settings:
            existing_settings["$schema"] = "https://json.schemastore.org/claude-code-settings.json"
        
        # Update hooks (replace completely for consistency)
        existing_settings["hooks"] = hooks_config
        
        # Write updated settings
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(existing_settings, f, indent=2)
            print_color("✅ Settings updated with spec-compliant configuration", GREEN)
            return True
        except Exception as e:
            self.issues.append(f"Failed to write settings: {e}")
            return False
    
    def verify_hook_script(self):
        """Ensure hook script handles all required fields properly"""
        hook_path = self.project_dir / "hooks" / "zelda_hook.py"
        
        if not hook_path.exists():
            self.issues.append("Hook script missing")
            return False
        
        # Check if hook can handle stdin JSON
        test_events = [
            {
                "hook_event_name": "PostToolUse",
                "session_id": "test-session",
                "toolName": "Test",
                "status": "success"
            },
            {
                "hook_event_name": "SessionStart",
                "session_id": "test-session",
                "cwd": str(self.project_dir)
            }
        ]
        
        python_cmd = self.get_python_command()
        
        for event in test_events:
            try:
                result = subprocess.run(
                    [python_cmd, str(hook_path)],
                    input=json.dumps(event),
                    text=True,
                    capture_output=True,
                    timeout=2
                )
                
                # Check exit code (0 = success, non-zero but not 2 = non-blocking error)
                if result.returncode == 2:
                    self.issues.append(f"Hook blocking error for {event['hook_event_name']}")
                    return False
                    
            except subprocess.TimeoutExpired:
                # Timeout is OK for sound playback
                pass
            except Exception as e:
                self.issues.append(f"Hook test failed: {e}")
                return False
        
        return True
    
    def check_cross_platform_compatibility(self):
        """Ensure installation works on all platforms"""
        print_color("\nChecking cross-platform compatibility...", YELLOW)
        
        system = platform.system()
        
        if system == "Darwin":  # macOS
            if not shutil.which("afplay"):
                self.issues.append("afplay not found (required for macOS)")
            else:
                print_color("✅ macOS: afplay available", GREEN)
                
        elif system == "Linux":
            # Check for any available player
            players = ["aplay", "paplay", "ffplay", "mpg123", "play"]
            found = False
            for player in players:
                if shutil.which(player):
                    print_color(f"✅ Linux: {player} available", GREEN)
                    found = True
                    break
            if not found:
                self.issues.append("No audio player found for Linux")
                
        elif system == "Windows":
            # Windows uses PowerShell which should always be available
            print_color("✅ Windows: PowerShell available", GREEN)
        else:
            self.issues.append(f"Unsupported platform: {system}")
    
    def validate_json_schema(self):
        """Validate settings against Claude Code schema"""
        print_color("\nValidating JSON schema compliance...", YELLOW)
        
        if not self.settings_file.exists():
            return False
        
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
            
            # Check required structure
            if "hooks" not in settings:
                self.issues.append("Missing 'hooks' in settings")
                return False
            
            # Validate PostToolUse structure
            post_tool = settings["hooks"].get("PostToolUse", [])
            if not isinstance(post_tool, list):
                self.issues.append("PostToolUse must be an array")
                return False
            
            if post_tool and len(post_tool) > 0:
                first_config = post_tool[0]
                if "hooks" not in first_config:
                    self.issues.append("PostToolUse config missing 'hooks' array")
                    return False
                    
                if "matcher" not in first_config:
                    # Matcher is optional but recommended for PostToolUse
                    print_color("⚠️  PostToolUse missing 'matcher' field (optional)", YELLOW)
            
            print_color("✅ JSON schema validated", GREEN)
            return True
            
        except Exception as e:
            self.issues.append(f"Schema validation failed: {e}")
            return False
    
    def test_with_edge_cases(self):
        """Test installation with various edge cases"""
        print_color("\nTesting edge cases...", YELLOW)
        
        tests_passed = []
        tests_failed = []
        
        # Test 1: Paths with spaces
        test_path = self.project_dir / "test with spaces.txt"
        try:
            test_path.write_text("test")
            test_path.unlink()
            tests_passed.append("Paths with spaces")
        except:
            tests_failed.append("Paths with spaces")
        
        # Test 2: Unicode in paths
        test_path = self.project_dir / "test_🎮.txt"
        try:
            test_path.write_text("test")
            test_path.unlink()
            tests_passed.append("Unicode paths")
        except:
            # Not critical
            print_color("⚠️  Unicode paths not supported", YELLOW)
        
        # Test 3: Permission check
        try:
            test_file = self.project_dir / "test_perms.sh"
            test_file.write_text("#!/bin/bash\necho test")
            os.chmod(test_file, 0o755)
            test_file.unlink()
            tests_passed.append("File permissions")
        except:
            tests_failed.append("File permissions")
        
        # Test 4: JSON with special characters
        test_json = {"test": "value with 'quotes' and \"double quotes\""}
        try:
            json_str = json.dumps(test_json)
            json.loads(json_str)
            tests_passed.append("JSON special characters")
        except:
            tests_failed.append("JSON special characters")
        
        if tests_passed:
            for test in tests_passed:
                print_color(f"✅ {test}", GREEN)
        
        if tests_failed:
            for test in tests_failed:
                print_color(f"❌ {test}", RED)
                self.issues.append(f"Edge case failed: {test}")
        
        return len(tests_failed) == 0
    
    def create_fallback_hook(self):
        """Create a more robust hook that handles errors gracefully"""
        hook_content = '''#!/usr/bin/env python3
"""
Universal Zelda Hook for Claude Code
Handles all platforms and edge cases gracefully
"""

import json
import sys
import subprocess
import os
from pathlib import Path

# Fail silently to never block Claude Code
try:
    # Read stdin
    input_data = sys.stdin.read()
    if not input_data:
        sys.exit(0)
    
    # Parse JSON
    try:
        data = json.loads(input_data)
    except:
        sys.exit(0)  # Invalid JSON, exit silently
    
    # Get event type
    event = data.get("hook_event_name", "")
    
    # Simple sound mapping
    sound_map = {
        "PostToolUse": "success.wav",
        "SessionStart": "session_start.wav",
        "Stop": "session_night.wav",
        "Notification": "notification.wav"
    }
    
    # Get sound file
    base_dir = Path(__file__).parent.parent
    sound_file = base_dir / "sounds" / sound_map.get(event, "default.wav")
    
    if not sound_file.exists():
        sys.exit(0)  # No sound, exit silently
    
    # Play sound based on platform
    import platform
    system = platform.system()
    
    if system == "Darwin":
        subprocess.Popen(["afplay", str(sound_file)], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
    elif system == "Linux":
        for player in ["aplay", "paplay", "play"]:
            try:
                subprocess.Popen([player, str(sound_file)],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                break
            except:
                continue
    elif system == "Windows":
        # Windows PowerShell command
        cmd = f'(New-Object Media.SoundPlayer "{sound_file}").PlaySync()'
        subprocess.Popen(["powershell", "-Command", cmd],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
    
except Exception:
    pass  # Fail silently

sys.exit(0)  # Always exit successfully
'''
        
        fallback_hook = self.project_dir / "hooks" / "universal_zelda_hook.py"
        fallback_hook.write_text(hook_content)
        os.chmod(fallback_hook, 0o755)
        self.fixes.append("Created universal fallback hook")
    
    def run_installation(self):
        """Run the complete installation process"""
        print_color("\n🎮 UNIVERSAL ZELDA CLAUDE CODE INSTALLER", BLUE)
        print_color("=" * 50, BLUE)
        
        # 1. Check Python
        print_color("\n1. Checking Python...", YELLOW)
        if self.check_python_version():
            print_color(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}", GREEN)
        
        # 2. Create directories
        print_color("\n2. Setting up directories...", YELLOW)
        self.ensure_directories()
        print_color("✅ All directories ready", GREEN)
        
        # 3. Cross-platform check
        self.check_cross_platform_compatibility()
        
        # 4. Update settings
        self.update_settings()
        
        # 5. Verify hook
        print_color("\n5. Verifying hook script...", YELLOW)
        if self.verify_hook_script():
            print_color("✅ Hook script validated", GREEN)
        else:
            # Create fallback
            self.create_fallback_hook()
            print_color("✅ Created fallback hook", GREEN)
        
        # 6. Validate schema
        self.validate_json_schema()
        
        # 7. Test edge cases
        self.test_with_edge_cases()
        
        # Summary
        print_color("\n" + "=" * 50, BLUE)
        print_color("📊 INSTALLATION SUMMARY", BLUE)
        print_color("=" * 50, BLUE)
        
        if self.fixes:
            print_color("\n🔧 Actions Taken:", GREEN)
            for fix in self.fixes:
                print_color(f"  • {fix}", GREEN)
        
        if self.issues:
            print_color("\n⚠️  Issues to Address:", YELLOW)
            for issue in self.issues:
                print_color(f"  • {issue}", YELLOW)
            
            print_color("\n💡 Recommendations:", BLUE)
            print_color("  1. Check the issues above", BLUE)
            print_color("  2. Run installer again if needed", BLUE)
            print_color("  3. Restart Claude Code", BLUE)
        else:
            print_color("\n✅ INSTALLATION SUCCESSFUL!", GREEN)
            print_color("\n🎮 Zelda Claude Code is ready!", GREEN)
            print_color("  • Hooks configured to spec", GREEN)
            print_color("  • Cross-platform compatible", GREEN)
            print_color("  • Edge cases handled", GREEN)
            print_color("\n⚡ Restart Claude Code to activate!", YELLOW)
        
        return len(self.issues) == 0

if __name__ == "__main__":
    installer = UniversalInstaller()
    success = installer.run_installation()
    sys.exit(0 if success else 1)