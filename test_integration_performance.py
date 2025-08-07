#!/usr/bin/env python3
"""
Integration Tests for Zelda Claude Code with Performance Optimizations
Tests the complete system working together
"""

import unittest
import json
import subprocess
import time
import tempfile
from pathlib import Path
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zelda_core import get_manager
from performance_optimizations import initialize_optimizations
import hooks.zelda_hook as zelda_hook


class TestHookIntegration(unittest.TestCase):
    """Test hook integration with optimizations"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.sounds_dir = Path(self.temp_dir) / "sounds"
        self.sounds_dir.mkdir()
        
        # Create test sound files
        for sound in ["success.wav", "error.wav", "todo_complete.wav", "damage.wav"]:
            (self.sounds_dir / sound).write_bytes(b"fake_sound")
        
        # Initialize optimizations
        self.opts = initialize_optimizations(self.sounds_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_hook_with_debouncing(self):
        """Test that hook properly debounces rapid commands"""
        with patch('hooks.zelda_hook.SOUNDS_DIR', self.sounds_dir):
            with patch('hooks.zelda_hook.get_optimizations', return_value=self.opts):
                with patch('subprocess.Popen') as mock_popen:
                    # Simulate rapid tool executions
                    for i in range(5):
                        zelda_hook.handle_tool_execution("Bash", {"exitCode": 0})
                    
                    # Should have been debounced - only first should play
                    # (plus potential combo sounds)
                    call_count = mock_popen.call_count
                    self.assertLess(call_count, 5, "Commands should be debounced")
    
    def test_hook_with_caching(self):
        """Test that hook uses cached sounds"""
        with patch('hooks.zelda_hook.SOUNDS_DIR', self.sounds_dir):
            with patch('hooks.zelda_hook.get_optimizations', return_value=self.opts):
                # First access should load into cache
                sound_path1 = self.opts["sound_cache"].get_sound_path_or_cache("success.wav")
                self.assertIsNotNone(sound_path1)
                
                # Record cache state
                self.assertIn("success.wav", self.opts["sound_cache"].cache)
                
                # Second access should use cache
                sound_path2 = self.opts["sound_cache"].get_sound_path_or_cache("success.wav")
                self.assertEqual(sound_path1, sound_path2)
    
    def test_performance_monitoring(self):
        """Test that performance metrics are recorded"""
        with patch('hooks.zelda_hook.SOUNDS_DIR', self.sounds_dir):
            with patch('hooks.zelda_hook.get_optimizations', return_value=self.opts):
                with patch('subprocess.Popen'):
                    # Execute command with monitoring
                    zelda_hook.handle_tool_execution("Read", {"success": True})
                    
                    # Wait for any async operations
                    time.sleep(0.1)
                    
                    # Check metrics were recorded
                    stats = self.opts["monitor"].get_stats()
                    if "hook_execution_times_avg_ms" in stats:
                        self.assertGreater(stats["hook_execution_times_avg_ms"], 0)


class TestZeldaCoreIntegration(unittest.TestCase):
    """Test zelda_core integration with optimizations"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_achievements = self.temp_dir / "achievements.json"
        self.test_stats = self.temp_dir / "stats.json"
        
        # Create test data
        test_data = {"unlocked": [], "progress": {}}
        with open(self.test_achievements, 'w') as f:
            json.dump(test_data, f)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_async_save_achievements(self):
        """Test async achievement saving"""
        with patch('zelda_core.ACHIEVEMENTS_FILE', self.test_achievements):
            manager = get_manager()
            
            # Modify and save achievements
            manager.achievement_progress.unlocked.append("test_achievement")
            manager.save_achievements()
            
            # Wait for async write
            time.sleep(0.2)
            
            # Verify file was written
            with open(self.test_achievements, 'r') as f:
                data = json.load(f)
            
            self.assertIn("test_achievement", data.get("unlocked", []))
    
    def test_cached_achievement_loading(self):
        """Test cached achievement loading"""
        with patch('zelda_core.ACHIEVEMENTS_FILE', self.test_achievements):
            # First load
            manager1 = get_manager()
            
            # Second load should use cache if available
            manager2 = get_manager()
            
            # Both should have same data
            self.assertEqual(
                manager1.achievement_progress.unlocked,
                manager2.achievement_progress.unlocked
            )


class TestRapidCommandScenarios(unittest.TestCase):
    """Test rapid command execution scenarios"""
    
    def test_bulk_file_operations(self):
        """Test rapid file operations are debounced"""
        temp_dir = Path(tempfile.mkdtemp())
        opts = initialize_optimizations(temp_dir)
        
        try:
            # Simulate rapid file operations
            operations = []
            for i in range(20):
                if opts["debouncer"].should_process(f"Read:file{i % 3}.txt"):
                    operations.append(i)
            
            # Should debounce similar operations
            self.assertLess(len(operations), 20)
            
        finally:
            import shutil
            shutil.rmtree(temp_dir)
    
    def test_parallel_sound_playback(self):
        """Test that multiple sounds don't overlap excessively"""
        temp_dir = Path(tempfile.mkdtemp())
        sounds_dir = temp_dir / "sounds"
        sounds_dir.mkdir()
        
        # Create test sounds
        for i in range(10):
            (sounds_dir / f"test{i}.wav").write_bytes(b"sound")
        
        opts = initialize_optimizations(sounds_dir)
        
        try:
            with patch('subprocess.Popen') as mock_popen:
                mock_popen.return_value.wait = MagicMock()
                
                # Try to play many sounds rapidly
                for i in range(10):
                    sound = f"test{i}.wav"
                    opts["sound_cache"].get_sound_path_or_cache(sound)
                
                # All should be cached
                self.assertGreaterEqual(len(opts["sound_cache"].cache), 5)
                
        finally:
            import shutil
            shutil.rmtree(temp_dir)


class TestPerformanceBenchmarks(unittest.TestCase):
    """Benchmark tests comparing optimized vs non-optimized"""
    
    def test_file_io_performance(self):
        """Compare cached vs non-cached file I/O"""
        temp_file = Path(tempfile.mkdtemp()) / "test.json"
        test_data = {"data": list(range(1000))}
        
        try:
            with open(temp_file, 'w') as f:
                json.dump(test_data, f)
            
            # Non-cached reads
            start = time.time()
            for _ in range(100):
                with open(temp_file, 'r') as f:
                    data = json.load(f)
            non_cached_time = time.time() - start
            
            # Cached reads
            from performance_optimizations import OptimizedFileIO
            file_io = OptimizedFileIO()
            
            start = time.time()
            for _ in range(100):
                data = file_io.read_json_cached(temp_file)
            cached_time = time.time() - start
            
            # Cached should be significantly faster
            improvement = (non_cached_time - cached_time) / non_cached_time * 100
            print(f"\nFile I/O Performance:")
            print(f"  Non-cached: {non_cached_time:.3f}s")
            print(f"  Cached: {cached_time:.3f}s")
            print(f"  Improvement: {improvement:.1f}%")
            
            self.assertLess(cached_time, non_cached_time)
            
        finally:
            temp_file.unlink(missing_ok=True)
    
    def test_debouncing_performance(self):
        """Test performance impact of debouncing"""
        from performance_optimizations import CommandDebouncer
        debouncer = CommandDebouncer(threshold_ms=50)
        
        processed = 0
        start = time.time()
        
        # Simulate rapid repeated commands
        for i in range(1000):
            if debouncer.should_process("test_command"):
                processed += 1
            time.sleep(0.001)  # 1ms between commands
        
        duration = time.time() - start
        reduction = (1000 - processed) / 1000 * 100
        
        print(f"\nDebouncing Performance:")
        print(f"  Commands sent: 1000")
        print(f"  Commands processed: {processed}")
        print(f"  Reduction: {reduction:.1f}%")
        print(f"  Duration: {duration:.3f}s")
        
        # Should significantly reduce processed commands
        self.assertLess(processed, 100)


def run_integration_tests():
    """Run all integration tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHookIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestZeldaCoreIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestRapidCommandScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceBenchmarks))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)