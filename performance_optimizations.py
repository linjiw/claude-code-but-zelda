#!/usr/bin/env python3
"""
Performance Optimization Module for Zelda Claude Code
Implements caching, debouncing, and async processing
"""

import json
import time
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Optional, Set
from collections import deque
from threading import Lock, Thread
from concurrent.futures import ThreadPoolExecutor
import mmap
import hashlib

class SoundCache:
    """In-memory sound file cache with preloading"""
    
    def __init__(self, sounds_dir: Path):
        self.sounds_dir = sounds_dir
        self.cache: Dict[str, bytes] = {}
        self.cache_lock = Lock()
        self.preload_common_sounds()
    
    def preload_common_sounds(self):
        """Preload frequently used sounds into memory"""
        common_sounds = [
            "success.wav", "error.wav", "todo_complete.wav",
            "item_small.wav", "heart_get.wav", "achievement.wav",
            "session_start.wav", "damage.wav", "search_found.wav"
        ]
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            for sound in common_sounds:
                executor.submit(self._load_sound, sound)
    
    def _load_sound(self, sound_name: str) -> Optional[bytes]:
        """Load a sound file into cache"""
        sound_path = self.sounds_dir / sound_name
        if not sound_path.exists():
            return None
        
        with self.cache_lock:
            if sound_name not in self.cache:
                try:
                    with open(sound_path, 'rb') as f:
                        self.cache[sound_name] = f.read()
                except Exception:
                    return None
        
        return self.cache.get(sound_name)
    
    def get_sound_path_or_cache(self, sound_name: str) -> Optional[Path]:
        """Get sound from cache or return path for streaming"""
        # For now, return path since afplay needs file path
        # Future: implement memory-mapped playback
        return self.sounds_dir / sound_name if (self.sounds_dir / sound_name).exists() else None


class CommandDebouncer:
    """Debounce rapid command executions"""
    
    def __init__(self, threshold_ms: int = 100):
        self.threshold_ms = threshold_ms
        self.last_commands: deque = deque(maxlen=10)
        self.lock = Lock()
    
    def should_process(self, command: str) -> bool:
        """Check if command should be processed or debounced"""
        current_time = time.time() * 1000
        
        with self.lock:
            # Check if same command was executed recently
            for cmd_time, cmd in self.last_commands:
                if cmd == command and (current_time - cmd_time) < self.threshold_ms:
                    return False
            
            self.last_commands.append((current_time, command))
            return True


class AsyncSoundPlayer:
    """Asynchronous sound player with queue management"""
    
    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.play_queue = asyncio.Queue()
        self.currently_playing = 0
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent)
    
    async def play_sound_async(self, sound_path: Path, volume: float = 1.0):
        """Play sound asynchronously without blocking"""
        if self.currently_playing >= self.max_concurrent:
            return  # Drop sound if too many playing
        
        self.currently_playing += 1
        
        def play():
            try:
                subprocess.run(
                    ["afplay", str(sound_path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10
                )
            finally:
                self.currently_playing -= 1
        
        # Submit to thread pool
        self.executor.submit(play)


class OptimizedFileIO:
    """Optimized file I/O with memory mapping and caching"""
    
    def __init__(self):
        self.file_cache: Dict[Path, Dict] = {}
        self.cache_lock = Lock()
        self.cache_ttl = 60  # Cache for 60 seconds
        self.last_cache_time: Dict[Path, float] = {}
    
    def read_json_cached(self, file_path: Path) -> Dict:
        """Read JSON with caching"""
        with self.cache_lock:
            # Check cache validity
            if file_path in self.file_cache:
                if time.time() - self.last_cache_time.get(file_path, 0) < self.cache_ttl:
                    return self.file_cache[file_path].copy()
            
            # Read from disk
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.file_cache[file_path] = data
                    self.last_cache_time[file_path] = time.time()
                    return data.copy()
            except Exception:
                return {}
    
    def write_json_async(self, file_path: Path, data: Dict):
        """Write JSON asynchronously"""
        def write():
            try:
                # Write to temp file first
                temp_path = file_path.with_suffix('.tmp')
                with open(temp_path, 'w') as f:
                    json.dump(data, f, indent=2)
                # Atomic rename
                temp_path.replace(file_path)
                
                # Update cache
                with self.cache_lock:
                    self.file_cache[file_path] = data
                    self.last_cache_time[file_path] = time.time()
            except Exception:
                pass
        
        Thread(target=write, daemon=True).start()


class BatchProcessor:
    """Batch multiple operations for efficiency"""
    
    def __init__(self, batch_size: int = 5, flush_interval: float = 0.5):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.pending_operations = []
        self.lock = Lock()
        self.last_flush = time.time()
        
        # Start background flusher
        Thread(target=self._background_flush, daemon=True).start()
    
    def add_operation(self, operation: callable):
        """Add operation to batch"""
        with self.lock:
            self.pending_operations.append(operation)
            
            if len(self.pending_operations) >= self.batch_size:
                self._flush()
    
    def _flush(self):
        """Execute all pending operations"""
        if not self.pending_operations:
            return
        
        operations = self.pending_operations.copy()
        self.pending_operations.clear()
        self.last_flush = time.time()
        
        # Execute in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            for op in operations:
                executor.submit(op)
    
    def _background_flush(self):
        """Periodically flush pending operations"""
        while True:
            time.sleep(self.flush_interval)
            with self.lock:
                if self.pending_operations and (time.time() - self.last_flush) > self.flush_interval:
                    self._flush()


class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    def __init__(self):
        self.metrics = {
            "hook_execution_times": deque(maxlen=100),
            "sound_play_times": deque(maxlen=100),
            "file_io_times": deque(maxlen=100),
            "cache_hits": 0,
            "cache_misses": 0
        }
        self.lock = Lock()
    
    def record_timing(self, category: str, duration_ms: float):
        """Record timing metric"""
        with self.lock:
            if category in self.metrics:
                self.metrics[category].append(duration_ms)
    
    def record_cache_hit(self, hit: bool):
        """Record cache hit/miss"""
        with self.lock:
            if hit:
                self.metrics["cache_hits"] += 1
            else:
                self.metrics["cache_misses"] += 1
    
    def get_stats(self) -> Dict:
        """Get performance statistics"""
        with self.lock:
            stats = {}
            
            for key, values in self.metrics.items():
                if isinstance(values, deque) and values:
                    stats[f"{key}_avg_ms"] = sum(values) / len(values)
                    stats[f"{key}_max_ms"] = max(values)
                elif isinstance(values, int):
                    stats[key] = values
            
            # Calculate cache hit rate
            total_cache = self.metrics["cache_hits"] + self.metrics["cache_misses"]
            if total_cache > 0:
                stats["cache_hit_rate"] = self.metrics["cache_hits"] / total_cache
            
            return stats


# Singleton instances
_sound_cache: Optional[SoundCache] = None
_debouncer: Optional[CommandDebouncer] = None
_async_player: Optional[AsyncSoundPlayer] = None
_file_io: Optional[OptimizedFileIO] = None
_batch_processor: Optional[BatchProcessor] = None
_monitor: Optional[PerformanceMonitor] = None


def initialize_optimizations(sounds_dir: Path):
    """Initialize all optimization systems"""
    global _sound_cache, _debouncer, _async_player, _file_io, _batch_processor, _monitor
    
    _sound_cache = SoundCache(sounds_dir)
    _debouncer = CommandDebouncer(threshold_ms=100)
    _async_player = AsyncSoundPlayer(max_concurrent=3)
    _file_io = OptimizedFileIO()
    _batch_processor = BatchProcessor(batch_size=5, flush_interval=0.5)
    _monitor = PerformanceMonitor()
    
    return {
        "sound_cache": _sound_cache,
        "debouncer": _debouncer,
        "async_player": _async_player,
        "file_io": _file_io,
        "batch_processor": _batch_processor,
        "monitor": _monitor
    }


def get_optimizations():
    """Get optimization instances"""
    return {
        "sound_cache": _sound_cache,
        "debouncer": _debouncer,
        "async_player": _async_player,
        "file_io": _file_io,
        "batch_processor": _batch_processor,
        "monitor": _monitor
    }