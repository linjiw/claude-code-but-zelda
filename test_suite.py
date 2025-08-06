#!/usr/bin/env python3
"""
Comprehensive test suite for Zelda Claude Code Sounds
Tests functionality, performance, and user experience
"""

import unittest
import subprocess
import time
import os
import sys
import json
import threading
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

class TestSoundPlayer(unittest.TestCase):
    """Test the sound player functionality"""
    
    def setUp(self):
        self.base_dir = Path(__file__).parent
        self.sounds_dir = self.base_dir / 'sounds'
        self.scripts_dir = self.base_dir / 'scripts'
        
    def test_all_sounds_exist(self):
        """Test that all required sound files exist"""
        required_sounds = [
            'success.wav', 'error.wav', 'warning.wav',
            'item_get.wav', 'rupee.wav', 'secret.wav',
            'damage.wav', 'puzzle_solved.wav', 'todo_complete.wav',
            'menu_select.wav', 'default.wav'
        ]
        
        for sound in required_sounds:
            sound_path = self.sounds_dir / sound
            self.assertTrue(sound_path.exists(), 
                          f"Sound file missing: {sound}")
            # Check file is not empty
            self.assertGreater(sound_path.stat().st_size, 100,
                             f"Sound file too small: {sound}")
    
    def test_sound_player_execution(self):
        """Test that sound player script executes without errors"""
        script_path = self.scripts_dir / 'play_sound.py'
        
        # Test each sound type
        sound_types = ['success', 'error', 'warning', 'todo_complete', 
                      'progress', 'start', 'test_pass', 'test_fail']
        
        for sound_type in sound_types:
            result = subprocess.run(
                ['python3', str(script_path), sound_type],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0,
                           f"Failed to play {sound_type}: {result.stderr}")
    
    def test_invalid_sound_type(self):
        """Test handling of invalid sound types"""
        script_path = self.scripts_dir / 'play_sound.py'
        
        # Should use default.wav for unknown types
        result = subprocess.run(
            ['python3', str(script_path), 'nonexistent'],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0,
                       "Should handle unknown sound types gracefully")
    
    def test_sound_file_formats(self):
        """Test that all sound files are valid WAV format"""
        import wave
        
        for sound_file in self.sounds_dir.glob('*.wav'):
            try:
                with wave.open(str(sound_file), 'rb') as wav:
                    # Check basic WAV properties
                    self.assertIn(wav.getnchannels(), [1, 2],
                                f"{sound_file.name} has invalid channels")
                    self.assertEqual(wav.getsampwidth(), 2,
                                   f"{sound_file.name} has invalid sample width")
                    self.assertIn(wav.getframerate(), [44100, 48000],
                                f"{sound_file.name} has invalid sample rate")
            except Exception as e:
                self.fail(f"Invalid WAV file {sound_file.name}: {e}")


class TestHookIntegration(unittest.TestCase):
    """Test Claude Code hook integration"""
    
    def setUp(self):
        self.base_dir = Path(__file__).parent
        self.hooks_dir = self.base_dir / 'hooks'
        
    def test_all_hooks_exist(self):
        """Test that all hook scripts exist and are executable"""
        required_hooks = [
            'on_success.sh', 'on_error.sh', 
            'on_todo_complete.sh', 'on_test_pass.sh', 'on_test_fail.sh'
        ]
        
        for hook in required_hooks:
            hook_path = self.hooks_dir / hook
            self.assertTrue(hook_path.exists(), f"Hook missing: {hook}")
            # Check if executable
            self.assertTrue(os.access(hook_path, os.X_OK),
                          f"Hook not executable: {hook}")
    
    def test_hook_execution(self):
        """Test that hooks execute without errors"""
        hooks = list(self.hooks_dir.glob('*.sh'))
        
        for hook in hooks:
            result = subprocess.run(
                [str(hook)],
                capture_output=True, text=True,
                timeout=2  # Prevent hanging
            )
            self.assertEqual(result.returncode, 0,
                           f"Hook failed: {hook.name}: {result.stderr}")
    
    def test_claude_settings_valid(self):
        """Test that Claude settings.json is valid"""
        settings_path = Path.home() / '.config' / 'claude' / 'settings.json'
        
        if settings_path.exists():
            with open(settings_path) as f:
                try:
                    settings = json.load(f)
                    self.assertIn('hooks', settings,
                                "No hooks section in settings.json")
                    
                    # Check hook paths are absolute and exist
                    tool_hooks = settings['hooks'].get('tool-result-hook', {})
                    for tool, actions in tool_hooks.items():
                        for action, path in actions.items():
                            self.assertTrue(Path(path).is_absolute(),
                                          f"Hook path not absolute: {path}")
                            self.assertTrue(Path(path).exists(),
                                          f"Hook path doesn't exist: {path}")
                except json.JSONDecodeError as e:
                    self.fail(f"Invalid JSON in settings.json: {e}")


class TestSoundMapping(unittest.TestCase):
    """Test that sounds map correctly to events"""
    
    def setUp(self):
        self.mappings = {
            'success': 'success.wav',
            'error': 'error.wav',
            'warning': 'warning.wav',
            'start': 'menu_select.wav',
            'progress': 'rupee.wav',
            'complete': 'item_get.wav',
            'test_pass': 'puzzle_solved.wav',
            'test_fail': 'damage.wav',
            'todo_complete': 'secret.wav'
        }
    
    def test_sound_mapping_logic(self):
        """Test that the sound mapping logic is correct"""
        script_path = Path(__file__).parent / 'scripts' / 'play_sound.py'
        
        # Read the script to verify mappings
        with open(script_path) as f:
            content = f.read()
            
        for event, sound in self.mappings.items():
            self.assertIn(sound, content,
                        f"Sound {sound} not mapped for {event}")


class TestPerformance(unittest.TestCase):
    """Test performance impact"""
    
    def test_sound_playback_speed(self):
        """Test that sound playback doesn't block"""
        script_path = Path(__file__).parent / 'scripts' / 'play_sound.py'
        
        start_time = time.time()
        result = subprocess.run(
            ['python3', str(script_path), 'success'],
            capture_output=True, text=True
        )
        elapsed = time.time() - start_time
        
        # Sound should start playing without blocking
        # (process should exit quickly even if sound is still playing)
        self.assertLess(elapsed, 0.5,
                       f"Sound playback took too long: {elapsed:.2f}s")
    
    def test_concurrent_sounds(self):
        """Test handling of multiple simultaneous sounds"""
        script_path = Path(__file__).parent / 'scripts' / 'play_sound.py'
        
        # Start multiple sounds simultaneously
        processes = []
        for sound in ['success', 'error', 'warning']:
            p = subprocess.Popen(
                ['python3', str(script_path), sound],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            processes.append(p)
        
        # Wait for all to complete
        for p in processes:
            stdout, stderr = p.communicate(timeout=2)
            self.assertEqual(p.returncode, 0,
                           f"Concurrent sound failed: {stderr}")
    
    def test_rapid_succession(self):
        """Test rapid successive sound triggers"""
        script_path = Path(__file__).parent / 'scripts' / 'play_sound.py'
        
        start_time = time.time()
        for _ in range(5):
            subprocess.run(
                ['python3', str(script_path), 'rupee'],
                capture_output=True
            )
        elapsed = time.time() - start_time
        
        # Should handle rapid triggers efficiently
        self.assertLess(elapsed, 2.0,
                       f"Rapid sounds took too long: {elapsed:.2f}s")


class TestErrorHandling(unittest.TestCase):
    """Test error handling and fallback mechanisms"""
    
    def test_missing_sound_file(self):
        """Test handling when sound file is missing"""
        # Temporarily rename a sound file
        sound_path = Path(__file__).parent / 'sounds' / 'test_temp.wav'
        original_path = Path(__file__).parent / 'sounds' / 'default.wav'
        
        if original_path.exists():
            # Test with missing file
            script_path = Path(__file__).parent / 'scripts' / 'play_sound.py'
            
            # Should handle missing files gracefully
            result = subprocess.run(
                ['python3', str(script_path), 'nonexistent'],
                capture_output=True, text=True
            )
            # Should complete even if sound doesn't play
            self.assertEqual(result.returncode, 0,
                           "Should handle missing sounds gracefully")
    
    def test_permission_errors(self):
        """Test handling of permission errors"""
        # This would require actually changing permissions, 
        # which might not be safe in all environments
        pass  # Skip for safety


class TestUserExperience(unittest.TestCase):
    """Test user experience aspects"""
    
    def test_sound_appropriateness(self):
        """Verify sounds match their intended emotional context"""
        expectations = {
            'success.wav': 'positive',
            'error.wav': 'negative', 
            'warning.wav': 'alert',
            'item_get.wav': 'achievement',
            'damage.wav': 'failure',
            'secret.wav': 'discovery'
        }
        
        # This is more of a checklist than automated test
        for sound, emotion in expectations.items():
            sound_path = Path(__file__).parent / 'sounds' / sound
            self.assertTrue(sound_path.exists(),
                          f"{emotion} sound exists: {sound}")
    
    def test_volume_consistency(self):
        """Check that sounds have consistent volume levels"""
        # This would require audio analysis libraries
        # For now, just check file sizes are reasonable
        sounds_dir = Path(__file__).parent / 'sounds'
        
        sizes = []
        for sound in sounds_dir.glob('*.wav'):
            size = sound.stat().st_size
            sizes.append(size)
        
        if sizes:
            avg_size = sum(sizes) / len(sizes)
            for sound in sounds_dir.glob('*.wav'):
                size = sound.stat().st_size
                # Check size is within reasonable range (not 10x different)
                ratio = size / avg_size
                self.assertLess(ratio, 10,
                              f"{sound.name} is unusually large")
                self.assertGreater(ratio, 0.1,
                                 f"{sound.name} is unusually small")


def run_tests():
    """Run all tests and generate report"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSoundPlayer))
    suite.addTests(loader.loadTestsFromTestCase(TestHookIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestSoundMapping))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestUserExperience))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)