#!/usr/bin/env python3
"""
Statistics Tracking System for Zelda Claude Code
Tracks commands, success rates, streaks, and tool usage
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field

@dataclass
class SessionStats:
    """Statistics for a single coding session"""
    session_id: str
    start_time: str
    end_time: Optional[str] = None
    total_commands: int = 0
    successful_commands: int = 0
    failed_commands: int = 0
    current_streak: int = 0
    max_streak: int = 0
    tools_used: Dict[str, int] = field(default_factory=dict)
    achievements_unlocked: List[str] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        if self.total_commands == 0:
            return 0.0
        return (self.successful_commands / self.total_commands) * 100
    
    @property
    def duration(self) -> Optional[timedelta]:
        if not self.end_time:
            return None
        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time)
        return end - start

@dataclass
class AllTimeStats:
    """Cumulative statistics across all sessions"""
    total_sessions: int = 0
    total_commands: int = 0
    total_successes: int = 0
    total_failures: int = 0
    longest_streak: int = 0
    longest_streak_date: Optional[str] = None
    total_time_coding: float = 0.0  # in minutes
    favorite_tool: Optional[str] = None
    tool_usage: Dict[str, int] = field(default_factory=dict)
    achievements: Dict[str, str] = field(default_factory=dict)  # achievement_id: unlock_date
    milestones: Dict[str, str] = field(default_factory=dict)  # milestone: date_reached
    
    @property
    def overall_success_rate(self) -> float:
        if self.total_commands == 0:
            return 0.0
        return (self.total_successes / self.total_commands) * 100

class StatsTracker:
    """Main statistics tracking system"""
    
    def __init__(self, stats_dir: Optional[Path] = None):
        self.stats_dir = stats_dir or Path.home() / ".zelda"
        self.stats_dir.mkdir(exist_ok=True)
        
        self.stats_file = self.stats_dir / "stats.json"
        self.sessions_dir = self.stats_dir / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        
        self.current_session: Optional[SessionStats] = None
        self.all_time_stats: AllTimeStats = self._load_all_time_stats()
        
    def _load_all_time_stats(self) -> AllTimeStats:
        """Load cumulative statistics from file"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    data = json.load(f)
                    return AllTimeStats(**data)
            except (json.JSONDecodeError, TypeError):
                # Corrupted file, start fresh
                return AllTimeStats()
        return AllTimeStats()
    
    def _save_all_time_stats(self):
        """Save cumulative statistics to file"""
        with open(self.stats_file, 'w') as f:
            json.dump(asdict(self.all_time_stats), f, indent=2)
    
    def start_session(self, session_id: str) -> SessionStats:
        """Start a new coding session"""
        self.current_session = SessionStats(
            session_id=session_id,
            start_time=datetime.now().isoformat()
        )
        self.all_time_stats.total_sessions += 1
        self._save_all_time_stats()
        return self.current_session
    
    def end_session(self):
        """End the current session and save stats"""
        if not self.current_session:
            return
        
        self.current_session.end_time = datetime.now().isoformat()
        
        # Update all-time stats
        self.all_time_stats.total_commands += self.current_session.total_commands
        self.all_time_stats.total_successes += self.current_session.successful_commands
        self.all_time_stats.total_failures += self.current_session.failed_commands
        
        # Update longest streak
        if self.current_session.max_streak > self.all_time_stats.longest_streak:
            self.all_time_stats.longest_streak = self.current_session.max_streak
            self.all_time_stats.longest_streak_date = datetime.now().isoformat()
        
        # Update tool usage
        for tool, count in self.current_session.tools_used.items():
            self.all_time_stats.tool_usage[tool] = \
                self.all_time_stats.tool_usage.get(tool, 0) + count
        
        # Find favorite tool
        if self.all_time_stats.tool_usage:
            self.all_time_stats.favorite_tool = max(
                self.all_time_stats.tool_usage.items(),
                key=lambda x: x[1]
            )[0]
        
        # Calculate session duration
        if self.current_session.duration:
            self.all_time_stats.total_time_coding += \
                self.current_session.duration.total_seconds() / 60
        
        # Save session to file
        session_file = self.sessions_dir / f"{self.current_session.session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(asdict(self.current_session), f, indent=2)
        
        # Save all-time stats
        self._save_all_time_stats()
        
        self.current_session = None
    
    def record_command(self, tool_name: str, success: bool):
        """Record a command execution"""
        if not self.current_session:
            return
        
        self.current_session.total_commands += 1
        
        if success:
            self.current_session.successful_commands += 1
            self.current_session.current_streak += 1
            if self.current_session.current_streak > self.current_session.max_streak:
                self.current_session.max_streak = self.current_session.current_streak
        else:
            self.current_session.failed_commands += 1
            self.current_session.current_streak = 0
        
        # Track tool usage
        self.current_session.tools_used[tool_name] = \
            self.current_session.tools_used.get(tool_name, 0) + 1
        
        # Check for milestones
        self._check_milestones()
    
    def _check_milestones(self):
        """Check if any milestones have been reached"""
        total = self.all_time_stats.total_commands + \
                (self.current_session.total_commands if self.current_session else 0)
        
        milestones = {
            1: "first_command",
            10: "novice_coder",
            50: "apprentice_coder",
            100: "journeyman_coder",
            500: "expert_coder",
            1000: "master_coder",
            5000: "legendary_coder"
        }
        
        for count, milestone_id in milestones.items():
            if total >= count and milestone_id not in self.all_time_stats.milestones:
                self.all_time_stats.milestones[milestone_id] = datetime.now().isoformat()
                if self.current_session:
                    self.current_session.achievements_unlocked.append(milestone_id)
                self._save_all_time_stats()
                return milestone_id
        
        return None
    
    def get_current_streak(self) -> int:
        """Get the current success streak"""
        if self.current_session:
            return self.current_session.current_streak
        return 0
    
    def get_stats_summary(self) -> Dict:
        """Get a summary of statistics for display"""
        summary = {
            "all_time": {
                "total_sessions": self.all_time_stats.total_sessions,
                "total_commands": self.all_time_stats.total_commands,
                "success_rate": f"{self.all_time_stats.overall_success_rate:.1f}%",
                "longest_streak": self.all_time_stats.longest_streak,
                "total_time": f"{self.all_time_stats.total_time_coding:.1f} minutes",
                "favorite_tool": self.all_time_stats.favorite_tool,
                "achievements": len(self.all_time_stats.achievements),
                "milestones": len(self.all_time_stats.milestones)
            }
        }
        
        if self.current_session:
            summary["current_session"] = {
                "commands": self.current_session.total_commands,
                "success_rate": f"{self.current_session.success_rate:.1f}%",
                "current_streak": self.current_session.current_streak,
                "max_streak": self.current_session.max_streak,
                "top_tools": sorted(
                    self.current_session.tools_used.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            }
        
        return summary

# Singleton instance
_tracker_instance: Optional[StatsTracker] = None

def get_tracker() -> StatsTracker:
    """Get the singleton StatsTracker instance"""
    global _tracker_instance
    if _tracker_instance is None:
        _tracker_instance = StatsTracker()
    return _tracker_instance