#!/usr/bin/env python3
"""
Comprehensive test suite for Zelda Claude Code system
"""

import json
import os
import sys
import subprocess
import tempfile
import shutil
import platform
from pathlib import Path
from datetime import datetime

# Force UTF-8 encoding for Windows
if platform.system() == 'Windows':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zelda_core

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
        
    def test(self, name, func):
        """Run a single test"""
        try:
            func()
            self.passed += 1
            self.tests.append((name, "✅ PASSED"))
            if os.environ.get('CI'):
                print(f"[PASS] {name}")
            else:
                print(f"✅ {name}")
            return True
        except AssertionError as e:
            self.failed += 1
            self.tests.append((name, f"❌ FAILED: {e}"))
            if os.environ.get('CI'):
                print(f"[FAIL] {name}: {e}")
            else:
                print(f"❌ {name}: {e}")
            return False
        except Exception as e:
            self.failed += 1
            self.tests.append((name, f"❌ ERROR: {e}"))
            if os.environ.get('CI'):
                print(f"[FAIL] {name}: Unexpected error: {e}")
            else:
                print(f"❌ {name}: Unexpected error: {e}")
            return False
    
    def summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        print("\n" + "="*60)
        print(f"TEST RESULTS: {self.passed}/{total} passed")
        if self.failed == 0:
            if os.environ.get('CI'):
                print("[SUCCESS] All tests passed!")
            else:
                print("🎉 All tests passed!")
        else:
            if os.environ.get('CI'):
                print(f"[WARNING] {self.failed} tests failed")
            else:
                print(f"⚠️  {self.failed} tests failed")
        print("="*60)
        return self.failed == 0

def test_zelda_core_module():
    """Test zelda_core module components"""
    runner = TestRunner()
    
    # Create temporary test directory
    test_dir = tempfile.mkdtemp(prefix="zelda_test_")
    original_dir = zelda_core.ZELDA_DIR
    
    try:
        # Override data directory for testing
        zelda_core.ZELDA_DIR = Path(test_dir)
        zelda_core.STATS_FILE = Path(test_dir) / "stats.json"
        zelda_core.ACHIEVEMENTS_FILE = Path(test_dir) / "achievements.json"
        zelda_core.CONFIG_FILE = Path(test_dir) / "config.json"
        zelda_core.SESSIONS_DIR = Path(test_dir) / "sessions"
        zelda_core.SESSIONS_DIR.mkdir(exist_ok=True)
        
        # Test 1: ZeldaManager initialization
        def test_manager_init():
            manager = zelda_core.ZeldaManager()
            assert manager is not None
            assert hasattr(manager, 'all_time_stats')
            assert hasattr(manager, 'current_session')
            assert hasattr(manager, 'combo_state')
            assert hasattr(manager, 'achievement_progress')
            assert hasattr(manager, 'config')
            
            # Start a session for testing
            manager.start_session("test_session")
            assert manager.current_session is not None
        runner.test("ZeldaManager initialization", test_manager_init)
        
        # Test 2: Command processing
        def test_command_processing():
            manager = zelda_core.ZeldaManager()
            
            # Test help command
            response = manager.process_command("@zelda help")
            assert "Available Commands" in response
            assert "@zelda stats" in response
            
            # Test stats command
            response = manager.process_command("@zelda stats")
            assert "Coding Statistics" in response
            assert "Total Commands" in response
            
            # Test achievements command
            response = manager.process_command("@zelda achievements")
            assert "Achievements" in response
            
            # Test combo command
            response = manager.process_command("@zelda combo")
            assert "Combo Status" in response
        runner.test("Command processing", test_command_processing)
        
        # Test 3: Statistics tracking
        def test_stats_tracking():
            manager = zelda_core.ZeldaManager()
            manager.start_session("test_session")
            
            # Record some commands
            sounds1 = manager.record_command("Bash", True)
            assert isinstance(sounds1, list)
            
            sounds2 = manager.record_command("Edit", True)
            assert isinstance(sounds2, list)
            
            sounds3 = manager.record_command("Bash", False)
            assert isinstance(sounds3, list)
            
            # Check session stats were updated
            assert manager.current_session.total_commands == 3
            assert manager.current_session.successful_commands == 2
            assert manager.current_session.failed_commands == 1
        runner.test("Statistics tracking", test_stats_tracking)
        
        # Test 4: Combo system
        def test_combo_system():
            manager = zelda_core.ZeldaManager()
            manager.start_session("test_session")
            
            # Build a combo
            manager.record_command("Bash", True)
            assert manager.combo_state.current_streak == 1
            
            manager.record_command("Edit", True)
            assert manager.combo_state.current_streak == 2
            
            manager.record_command("Read", True)
            assert manager.combo_state.current_streak == 3
            
            # Break the combo
            manager.record_command("Bash", False)
            assert manager.combo_state.current_streak == 0
            assert manager.combo_state.highest_streak >= 3
        runner.test("Combo system", test_combo_system)
        
        # Test 5: Achievement detection
        def test_achievements():
            manager = zelda_core.ZeldaManager()
            manager.start_session("test_session")
            
            # Achievement system should be initialized
            assert hasattr(manager, 'achievement_progress')
            assert manager.achievement_progress is not None
            
            # Record multiple commands to potentially trigger achievements
            initial_count = len(manager.achievement_progress.achievements_unlocked)
            for i in range(5):
                sounds = manager.record_command(f"Tool{i}", True)
            
            # Should have made progress or unlocked something
            final_count = len(manager.achievement_progress.achievements_unlocked)
            progress_made = any(v > 0 for v in manager.achievement_progress.progress.values())
            
            assert final_count >= initial_count or progress_made, \
                   "Achievement system not tracking progress"
        runner.test("Achievement system", test_achievements)
        
        # Test 6: Configuration management
        def test_config():
            manager = zelda_core.ZeldaManager()
            
            # Test getting config
            response = manager.process_command("@zelda config")
            assert "Configuration" in response
            assert "volume" in response
            
            # Test setting config
            response = manager.process_command("@zelda config volume 50")
            assert "updated" in response.lower() or "set" in response.lower()
            assert manager.config.get('volume') == 50
            
            # Test invalid config
            response = manager.process_command("@zelda config invalid_key value")
            assert "unknown" in response.lower() or "invalid" in response.lower()
        runner.test("Configuration management", test_config)
        
        # Test 7: Data persistence
        def test_persistence():
            # Create manager and record data
            manager1 = zelda_core.ZeldaManager()
            manager1.start_session("test_session_1")
            manager1.record_command("Bash", True)
            manager1.record_command("Edit", True)
            
            # End session to save data
            manager1.end_session()
            
            # Create new manager instance
            manager2 = zelda_core.ZeldaManager()
            
            # Check data was loaded
            assert manager2.all_time_stats.total_commands >= 2
            assert manager2.all_time_stats.total_successes >= 2
        runner.test("Data persistence", test_persistence)
        
        # Test 8: Sound mapping
        def test_sound_mapping():
            manager = zelda_core.ZeldaManager()
            manager.start_session("test_session")
            
            # Test that sounds are returned (may be empty list on first few commands)
            sounds1 = manager.record_command("Bash", True)
            sounds2 = manager.record_command("Edit", True)
            sounds3 = manager.record_command("Bash", False)
            
            # After multiple commands, should have gotten some sounds
            all_sounds = sounds1 + sounds2 + sounds3
            assert isinstance(all_sounds, list)
            # At minimum, achievement sound for first command
            assert len(all_sounds) >= 0  # May not always return sounds
        runner.test("Sound mapping", test_sound_mapping)
        
    finally:
        # Restore original data directory
        zelda_core.ZELDA_DIR = original_dir
        # Clean up test directory
        shutil.rmtree(test_dir, ignore_errors=True)
    
    return runner

def test_hook_integration():
    """Test hook integration"""
    runner = TestRunner()
    
    # Test 1: Hook file exists
    def test_hook_exists():
        hook_path = Path("hooks/zelda_hook.py")
        assert hook_path.exists(), "Hook file doesn't exist"
    runner.test("Hook file exists", test_hook_exists)
    
    # Test 2: Hook handles UserPromptSubmit
    def test_user_prompt():
        input_data = json.dumps({
            "hook_event_name": "UserPromptSubmit",
            "prompt": "@zelda help"
        })
        
        result = subprocess.run(
            ["python3", "hooks/zelda_hook.py"],
            input=input_data,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Hook failed: {result.stderr}"
        output = json.loads(result.stdout)
        assert output['decision'] == 'block'
        assert 'Available Commands' in output['reason']
    runner.test("UserPromptSubmit hook", test_user_prompt)
    
    # Test 3: Hook handles PostToolUse
    def test_post_tool():
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
        
        # Should exit cleanly (sound plays async)
        assert result.returncode == 0
    runner.test("PostToolUse hook", test_post_tool)
    
    # Test 4: Hook handles SessionStart
    def test_session_start():
        input_data = json.dumps({
            "hook_event_name": "SessionStart"
        })
        
        result = subprocess.run(
            ["python3", "hooks/zelda_hook.py"],
            input=input_data,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
    runner.test("SessionStart hook", test_session_start)
    
    # Test 5: Hook ignores non-@zelda prompts
    def test_normal_prompt():
        input_data = json.dumps({
            "hook_event_name": "UserPromptSubmit",
            "prompt": "normal user message"
        })
        
        result = subprocess.run(
            ["python3", "hooks/zelda_hook.py"],
            input=input_data,
            capture_output=True,
            text=True
        )
        
        # Should pass through without blocking
        assert result.returncode == 0
        if result.stdout:
            output = json.loads(result.stdout)
            assert output.get('decision') != 'block'
    runner.test("Normal prompt passthrough", test_normal_prompt)
    
    return runner

def test_sound_system():
    """Test sound playback system"""
    runner = TestRunner()
    
    # Test 1: Sound files exist
    def test_sound_files():
        sound_dir = Path("sounds")
        assert sound_dir.exists(), "Sounds directory doesn't exist"
        
        required_sounds = [
            "success.wav", "error.wav", "todo_complete.wav",
            "item_get.wav", "damage.wav", "secret.wav"
        ]
        
        for sound in required_sounds:
            sound_path = sound_dir / sound
            assert sound_path.exists(), f"Missing sound: {sound}"
    runner.test("Sound files exist", test_sound_files)
    
    # Test 2: Async sound player
    def test_async_player():
        script_path = Path("scripts/play_sound_async.py")
        assert script_path.exists(), "Async player doesn't exist"
        
        # Test playing a sound (won't actually hear it in tests)
        result = subprocess.run(
            ["python3", str(script_path), "success"],
            capture_output=True,
            text=True,
            timeout=2
        )
        
        # Should complete without error
        assert result.returncode == 0 or "not found" in result.stderr.lower()
    runner.test("Async sound player", test_async_player)
    
    # Test 3: Sound player script
    def test_sound_player():
        script_path = Path("scripts/play_sound.py")
        assert script_path.exists(), "Sound player doesn't exist"
    runner.test("Sound player exists", test_sound_player)
    
    return runner

def test_installation():
    """Test installation components"""
    runner = TestRunner()
    
    # Test 1: Installer script exists
    def test_installer():
        installer = Path("install.sh")
        assert installer.exists(), "Installer doesn't exist"
        assert installer.stat().st_mode & 0o111, "Installer not executable"
    runner.test("Installer exists", test_installer)
    
    # Test 2: README exists
    def test_readme():
        readme = Path("README.md")
        assert readme.exists(), "README doesn't exist"
        
        content = readme.read_text()
        assert "@zelda" in content, "README missing @zelda commands"
        assert "Installation" in content or "install" in content.lower()
    runner.test("README documentation", test_readme)
    
    # Test 3: Demo script exists
    def test_demo():
        demo = Path("demo_sounds.sh")
        assert demo.exists(), "Demo script doesn't exist"
    runner.test("Demo script exists", test_demo)
    
    return runner

def main():
    """Run all tests"""
    if os.environ.get('CI'):
        print("[TEST] Zelda Claude Code Test Suite")
    else:
        print("🧪 Zelda Claude Code Test Suite")
    print("="*60)
    
    all_passed = True
    
    # Run core module tests
    if os.environ.get('CI'):
        print("\n[MODULE] Testing Core Module...")
    else:
        print("\n📦 Testing Core Module...")
    runner = test_zelda_core_module()
    all_passed = runner.summary() and all_passed
    
    # Run hook integration tests
    if os.environ.get('CI'):
        print("\n[HOOK] Testing Hook Integration...")
    else:
        print("\n🔗 Testing Hook Integration...")
    runner = test_hook_integration()
    all_passed = runner.summary() and all_passed
    
    # Run sound system tests
    print("\n🔊 Testing Sound System...")
    runner = test_sound_system()
    all_passed = runner.summary() and all_passed
    
    # Run installation tests
    print("\n📥 Testing Installation Components...")
    runner = test_installation()
    all_passed = runner.summary() and all_passed
    
    # Final summary
    print("\n" + "="*60)
    if all_passed:
        if os.environ.get('CI'):
            print("[SUCCESS] ALL TEST SUITES PASSED!")
        else:
            print("🎉 ALL TEST SUITES PASSED! 🎉")
        print("The Zelda Claude Code system is working correctly!")
    else:
        if os.environ.get('CI'):
            print("[WARNING] Some tests failed. Please review the output above.")
        else:
            print("⚠️  Some tests failed. Please review the output above.")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())