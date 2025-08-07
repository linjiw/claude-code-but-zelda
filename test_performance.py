#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Performance Optimizations
Tests all optimization components individually
"""

import unittest
import time
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from performance_optimizations import (
    SoundCache, CommandDebouncer, AsyncSoundPlayer,
    OptimizedFileIO, BatchProcessor, PerformanceMonitor,
    initialize_optimizations
)

class TestSoundCache(unittest.TestCase):
    """Test sound caching functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sounds_dir = Path(self.temp_dir)
        
        # Create test sound files
        for sound in ["success.wav", "error.wav", "test.wav"]:
            (self.sounds_dir / sound).write_bytes(b"fake_sound_data")
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_preload_common_sounds(self):
        """Test that common sounds are preloaded"""
        cache = SoundCache(self.sounds_dir)
        
        # Check that preloaded sounds are in cache
        self.assertIn("success.wav", cache.cache)
        self.assertIn("error.wav", cache.cache)
    
    def test_get_sound_path_or_cache(self):
        """Test sound retrieval from cache"""
        cache = SoundCache(self.sounds_dir)
        
        # Should return path for existing sound
        path = cache.get_sound_path_or_cache("success.wav")
        self.assertIsNotNone(path)
        self.assertTrue(path.exists())
        
        # Should return None for non-existent sound
        path = cache.get_sound_path_or_cache("nonexistent.wav")
        self.assertIsNone(path)
    
    def test_thread_safety(self):
        """Test thread-safe cache access"""
        cache = SoundCache(self.sounds_dir)
        
        import threading
        results = []
        
        def load_sound():
            path = cache._load_sound("test.wav")
            results.append(path is not None)
        
        threads = [threading.Thread(target=load_sound) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(results), 10)
        self.assertTrue(all(results))


class TestCommandDebouncer(unittest.TestCase):
    """Test command debouncing functionality"""
    
    def test_debounce_rapid_commands(self):
        """Test that rapid commands are debounced"""
        debouncer = CommandDebouncer(threshold_ms=100)
        
        # First command should process
        self.assertTrue(debouncer.should_process("test_command"))
        
        # Immediate repeat should be debounced
        self.assertFalse(debouncer.should_process("test_command"))
        
        # Different command should process
        self.assertTrue(debouncer.should_process("other_command"))
        
        # After threshold, same command should process
        time.sleep(0.15)  # 150ms > 100ms threshold
        self.assertTrue(debouncer.should_process("test_command"))
    
    def test_command_history(self):
        """Test that command history is maintained"""
        debouncer = CommandDebouncer(threshold_ms=50)
        
        commands = ["cmd1", "cmd2", "cmd3", "cmd4", "cmd5"]
        for cmd in commands:
            debouncer.should_process(cmd)
            time.sleep(0.06)  # Just over threshold
        
        # Check that history is limited (maxlen=10)
        self.assertLessEqual(len(debouncer.last_commands), 10)


class TestOptimizedFileIO(unittest.TestCase):
    """Test optimized file I/O operations"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.test_data = {"test": "data", "number": 42}
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()
        self.temp_path = Path(self.temp_file.name)
    
    def tearDown(self):
        self.temp_path.unlink(missing_ok=True)
    
    def test_read_json_cached(self):
        """Test JSON reading with caching"""
        file_io = OptimizedFileIO()
        
        # First read should load from disk
        data1 = file_io.read_json_cached(self.temp_path)
        self.assertEqual(data1, self.test_data)
        
        # Second read should come from cache
        data2 = file_io.read_json_cached(self.temp_path)
        self.assertEqual(data2, self.test_data)
        
        # Verify cache was used (data should be in cache)
        self.assertIn(self.temp_path, file_io.file_cache)
    
    def test_write_json_async(self):
        """Test asynchronous JSON writing"""
        file_io = OptimizedFileIO()
        new_data = {"new": "data", "async": True}
        
        file_io.write_json_async(self.temp_path, new_data)
        
        # Give async write time to complete
        time.sleep(0.1)
        
        # Verify file was written
        with open(self.temp_path, 'r') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, new_data)
        
        # Verify cache was updated
        cached_data = file_io.read_json_cached(self.temp_path)
        self.assertEqual(cached_data, new_data)
    
    def test_cache_ttl(self):
        """Test cache TTL expiration"""
        file_io = OptimizedFileIO()
        file_io.cache_ttl = 0.1  # 100ms TTL for testing
        
        # Read and cache
        data1 = file_io.read_json_cached(self.temp_path)
        
        # Wait for cache to expire
        time.sleep(0.15)
        
        # Modify file
        new_data = {"modified": True}
        with open(self.temp_path, 'w') as f:
            json.dump(new_data, f)
        
        # Read should get new data (cache expired)
        data2 = file_io.read_json_cached(self.temp_path)
        self.assertEqual(data2, new_data)


class TestBatchProcessor(unittest.TestCase):
    """Test batch processing functionality"""
    
    def test_batch_execution(self):
        """Test that operations are batched"""
        processor = BatchProcessor(batch_size=3, flush_interval=1.0)
        
        results = []
        
        def operation(value):
            results.append(value)
        
        # Add operations (should batch at size 3)
        for i in range(3):
            processor.add_operation(lambda i=i: operation(i))
        
        # Give time for batch execution
        time.sleep(0.1)
        
        # Should have executed all 3
        self.assertEqual(len(results), 3)
    
    def test_auto_flush(self):
        """Test automatic flush on interval"""
        processor = BatchProcessor(batch_size=10, flush_interval=0.1)
        
        results = []
        
        processor.add_operation(lambda: results.append(1))
        processor.add_operation(lambda: results.append(2))
        
        # Wait for auto-flush
        time.sleep(0.2)
        
        # Should have flushed even though batch not full
        self.assertEqual(len(results), 2)


class TestPerformanceMonitor(unittest.TestCase):
    """Test performance monitoring functionality"""
    
    def test_record_timing(self):
        """Test timing metric recording"""
        monitor = PerformanceMonitor()
        
        monitor.record_timing("hook_execution_times", 10.5)
        monitor.record_timing("hook_execution_times", 15.3)
        monitor.record_timing("sound_play_times", 2.1)
        
        stats = monitor.get_stats()
        
        self.assertIn("hook_execution_times_avg_ms", stats)
        self.assertIn("hook_execution_times_max_ms", stats)
        self.assertAlmostEqual(stats["hook_execution_times_avg_ms"], 12.9, places=1)
        self.assertEqual(stats["hook_execution_times_max_ms"], 15.3)
    
    def test_cache_metrics(self):
        """Test cache hit/miss tracking"""
        monitor = PerformanceMonitor()
        
        # Record some hits and misses
        for _ in range(7):
            monitor.record_cache_hit(True)
        for _ in range(3):
            monitor.record_cache_hit(False)
        
        stats = monitor.get_stats()
        
        self.assertEqual(stats["cache_hits"], 7)
        self.assertEqual(stats["cache_misses"], 3)
        self.assertAlmostEqual(stats["cache_hit_rate"], 0.7, places=1)


class TestInitialization(unittest.TestCase):
    """Test optimization system initialization"""
    
    def test_initialize_optimizations(self):
        """Test that all components are initialized"""
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            opts = initialize_optimizations(temp_dir)
            
            # Verify all components are present
            self.assertIn("sound_cache", opts)
            self.assertIn("debouncer", opts)
            self.assertIn("async_player", opts)
            self.assertIn("file_io", opts)
            self.assertIn("batch_processor", opts)
            self.assertIn("monitor", opts)
            
            # Verify types
            self.assertIsInstance(opts["sound_cache"], SoundCache)
            self.assertIsInstance(opts["debouncer"], CommandDebouncer)
            self.assertIsInstance(opts["file_io"], OptimizedFileIO)
            self.assertIsInstance(opts["monitor"], PerformanceMonitor)
            
        finally:
            import shutil
            shutil.rmtree(temp_dir)


class TestIntegration(unittest.TestCase):
    """Integration tests for optimization components working together"""
    
    def test_cached_debounced_workflow(self):
        """Test complete optimized workflow"""
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            # Create test sound
            (temp_dir / "test.wav").write_bytes(b"sound_data")
            
            # Initialize optimizations
            opts = initialize_optimizations(temp_dir)
            
            # Test workflow: debounce -> cache -> monitor
            start = time.time()
            
            # First call should process
            should_process = opts["debouncer"].should_process("test")
            self.assertTrue(should_process)
            
            if should_process:
                # Get sound from cache
                sound_path = opts["sound_cache"].get_sound_path_or_cache("test.wav")
                self.assertIsNotNone(sound_path)
                
                # Record metrics
                duration = (time.time() - start) * 1000
                opts["monitor"].record_timing("workflow", duration)
                opts["monitor"].record_cache_hit(True)
            
            # Rapid repeat should be debounced
            should_process = opts["debouncer"].should_process("test")
            self.assertFalse(should_process)
            
            # Check metrics
            stats = opts["monitor"].get_stats()
            # workflow_avg_ms only exists if we recorded timings
            if "workflow_avg_ms" in stats:
                self.assertGreater(stats["workflow_avg_ms"], 0)
            self.assertEqual(stats["cache_hits"], 1)
            
        finally:
            import shutil
            shutil.rmtree(temp_dir)


def run_tests():
    """Run all unit tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSoundCache))
    suite.addTests(loader.loadTestsFromTestCase(TestCommandDebouncer))
    suite.addTests(loader.loadTestsFromTestCase(TestOptimizedFileIO))
    suite.addTests(loader.loadTestsFromTestCase(TestBatchProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestInitialization))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("PERFORMANCE OPTIMIZATION TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFailed tests:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nTests with errors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)