#!/usr/bin/env python3
"""
Achievement System for Zelda Claude Code
Tracks and awards achievements for various coding milestones
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class AchievementCategory(Enum):
    """Categories of achievements"""
    MILESTONE = "milestone"      # Command count milestones
    COMBO = "combo"              # Streak achievements
    EXPLORER = "explorer"        # Tool usage variety
    PERFECTIONIST = "perfectionist"  # Error-free sessions
    SPEEDRUNNER = "speedrunner"  # Time-based achievements
    COLLECTOR = "collector"      # Collection achievements

@dataclass
class Achievement:
    """Definition of an achievement"""
    id: str
    name: str
    description: str
    category: AchievementCategory
    sound: str
    icon: str  # Emoji icon
    requirement: int  # Numeric requirement
    hidden: bool = False  # Hidden until unlocked
    
@dataclass 
class AchievementProgress:
    """Track progress toward an achievement"""
    achievement_id: str
    current_progress: int
    requirement: int
    unlocked: bool = False
    unlock_date: Optional[str] = None
    
    @property
    def progress_percent(self) -> float:
        if self.requirement == 0:
            return 100.0
        return min(100.0, (self.current_progress / self.requirement) * 100)

class AchievementManager:
    """Manages all achievements and tracking"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path.home() / ".zelda"
        self.data_dir.mkdir(exist_ok=True)
        
        self.achievements_file = self.data_dir / "achievements.json"
        self.achievements = self._define_achievements()
        self.progress = self._load_progress()
        
    def _define_achievements(self) -> Dict[str, Achievement]:
        """Define all available achievements"""
        achievements = [
            # Milestone Achievements
            Achievement("first_step", "First Steps", "Execute your first command", 
                       AchievementCategory.MILESTONE, "item_small.wav", "👶", 1),
            Achievement("apprentice", "Apprentice Coder", "Execute 10 commands",
                       AchievementCategory.MILESTONE, "heart_get.wav", "📚", 10),
            Achievement("journeyman", "Journeyman", "Execute 50 commands",
                       AchievementCategory.MILESTONE, "achievement.wav", "⚔️", 50),
            Achievement("master", "Master Coder", "Execute 100 commands",
                       AchievementCategory.MILESTONE, "shrine_complete.wav", "🏆", 100),
            Achievement("legend", "Legendary Hero", "Execute 500 commands",
                       AchievementCategory.MILESTONE, "session_start.wav", "👑", 500),
            Achievement("deity", "Coding Deity", "Execute 1000 commands",
                       AchievementCategory.MILESTONE, "session_start.wav", "🌟", 1000, hidden=True),
            
            # Combo Achievements
            Achievement("combo_bronze", "Combo Starter", "Achieve a 3-command streak",
                       AchievementCategory.COMBO, "item_small.wav", "🥉", 3),
            Achievement("combo_silver", "Combo Pro", "Achieve a 5-command streak",
                       AchievementCategory.COMBO, "heart_get.wav", "🥈", 5),
            Achievement("combo_gold", "Combo Master", "Achieve a 10-command streak",
                       AchievementCategory.COMBO, "achievement.wav", "🥇", 10),
            Achievement("combo_platinum", "Combo Legend", "Achieve a 20-command streak",
                       AchievementCategory.COMBO, "shrine_complete.wav", "💎", 20),
            Achievement("combo_perfect", "Perfect Flow", "Achieve a 50-command streak",
                       AchievementCategory.COMBO, "session_start.wav", "🔥", 50, hidden=True),
            
            # Explorer Achievements
            Achievement("tool_user", "Tool User", "Use 5 different tools",
                       AchievementCategory.EXPLORER, "search_found.wav", "🔧", 5),
            Achievement("tool_master", "Tool Master", "Use 10 different tools",
                       AchievementCategory.EXPLORER, "puzzle_solved.wav", "🛠️", 10),
            Achievement("polyglot", "Polyglot", "Use all available tools",
                       AchievementCategory.EXPLORER, "achievement.wav", "🌐", 20, hidden=True),
            
            # Perfectionist Achievements  
            Achievement("flawless_ten", "Flawless Ten", "10 commands without errors",
                       AchievementCategory.PERFECTIONIST, "heart_get.wav", "✨", 10),
            Achievement("error_free", "Error Free", "25 commands without errors",
                       AchievementCategory.PERFECTIONIST, "achievement.wav", "💯", 25),
            Achievement("perfect_session", "Perfect Session", "50 commands without errors",
                       AchievementCategory.PERFECTIONIST, "shrine_complete.wav", "🎯", 50),
            
            # Speedrunner Achievements
            Achievement("quick_start", "Quick Start", "5 commands in 1 minute",
                       AchievementCategory.SPEEDRUNNER, "item_small.wav", "⚡", 5),
            Achievement("speed_demon", "Speed Demon", "20 commands in 5 minutes",
                       AchievementCategory.SPEEDRUNNER, "achievement.wav", "🏃", 20),
            Achievement("lightning", "Lightning Coder", "50 commands in 10 minutes",
                       AchievementCategory.SPEEDRUNNER, "session_start.wav", "⚡", 50, hidden=True),
            
            # Collector Achievements
            Achievement("sound_hunter", "Sound Hunter", "Unlock 5 achievements",
                       AchievementCategory.COLLECTOR, "search_complete.wav", "🎵", 5),
            Achievement("achievement_hunter", "Achievement Hunter", "Unlock 10 achievements",
                       AchievementCategory.COLLECTOR, "puzzle_solved.wav", "🏅", 10),
            Achievement("completionist", "Completionist", "Unlock 20 achievements",
                       AchievementCategory.COLLECTOR, "achievement.wav", "💎", 20),
        ]
        
        return {a.id: a for a in achievements}
    
    def _load_progress(self) -> Dict[str, AchievementProgress]:
        """Load achievement progress from file"""
        if self.achievements_file.exists():
            try:
                with open(self.achievements_file, 'r') as f:
                    data = json.load(f)
                    progress = {}
                    for aid, pdata in data.items():
                        progress[aid] = AchievementProgress(**pdata)
                    return progress
            except (json.JSONDecodeError, TypeError):
                pass
        
        # Initialize progress for all achievements
        progress = {}
        for aid, achievement in self.achievements.items():
            progress[aid] = AchievementProgress(
                achievement_id=aid,
                current_progress=0,
                requirement=achievement.requirement
            )
        return progress
    
    def _save_progress(self):
        """Save achievement progress to file"""
        data = {aid: asdict(p) for aid, p in self.progress.items()}
        with open(self.achievements_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def update_progress(self, updates: Dict[str, int]) -> List[Tuple[Achievement, str]]:
        """
        Update progress for multiple achievement types
        Returns list of (achievement, sound) for newly unlocked achievements
        """
        unlocked = []
        
        for achievement_id, new_value in updates.items():
            if achievement_id not in self.progress:
                continue
                
            progress = self.progress[achievement_id]
            achievement = self.achievements[achievement_id]
            
            # Update progress value
            old_progress = progress.current_progress
            progress.current_progress = max(progress.current_progress, new_value)
            
            # Check if newly unlocked
            if not progress.unlocked and progress.current_progress >= progress.requirement:
                progress.unlocked = True
                progress.unlock_date = datetime.now().isoformat()
                unlocked.append((achievement, achievement.sound))
        
        # Check collector achievements (based on other achievements)
        total_unlocked = sum(1 for p in self.progress.values() if p.unlocked)
        collector_updates = {
            "sound_hunter": total_unlocked,
            "achievement_hunter": total_unlocked,
            "completionist": total_unlocked
        }
        
        for aid, count in collector_updates.items():
            if aid in self.progress:
                progress = self.progress[aid]
                achievement = self.achievements[aid]
                
                if not progress.unlocked:
                    progress.current_progress = count
                    if count >= progress.requirement:
                        progress.unlocked = True
                        progress.unlock_date = datetime.now().isoformat()
                        unlocked.append((achievement, achievement.sound))
        
        # Save if anything was unlocked
        if unlocked:
            self._save_progress()
        
        return unlocked
    
    def check_command_achievements(self, total_commands: int, streak: int, 
                                  error_free_count: int, tools_used: int) -> List[Tuple[Achievement, str]]:
        """Check achievements related to command execution"""
        updates = {
            # Milestones
            "first_step": total_commands,
            "apprentice": total_commands,
            "journeyman": total_commands,
            "master": total_commands,
            "legend": total_commands,
            "deity": total_commands,
            
            # Combos
            "combo_bronze": streak,
            "combo_silver": streak,
            "combo_gold": streak,
            "combo_platinum": streak,
            "combo_perfect": streak,
            
            # Perfectionist
            "flawless_ten": error_free_count,
            "error_free": error_free_count,
            "perfect_session": error_free_count,
            
            # Explorer
            "tool_user": tools_used,
            "tool_master": tools_used,
            "polyglot": tools_used,
        }
        
        return self.update_progress(updates)
    
    def get_achievement_summary(self) -> Dict:
        """Get summary of achievement progress"""
        total = len(self.achievements)
        unlocked = sum(1 for p in self.progress.values() if p.unlocked)
        
        # Group by category
        by_category = {}
        for achievement in self.achievements.values():
            if achievement.category not in by_category:
                by_category[achievement.category] = {"total": 0, "unlocked": 0}
            
            by_category[achievement.category]["total"] += 1
            if self.progress[achievement.id].unlocked:
                by_category[achievement.category]["unlocked"] += 1
        
        # Find next closest achievement
        next_achievement = None
        min_remaining = float('inf')
        
        for aid, progress in self.progress.items():
            if not progress.unlocked:
                remaining = progress.requirement - progress.current_progress
                if remaining < min_remaining:
                    min_remaining = remaining
                    next_achievement = self.achievements[aid]
        
        return {
            "total_achievements": total,
            "unlocked": unlocked,
            "percentage": (unlocked / total * 100) if total > 0 else 0,
            "by_category": by_category,
            "next_closest": next_achievement.name if next_achievement else None,
            "recent_unlocks": self._get_recent_unlocks(5)
        }
    
    def _get_recent_unlocks(self, limit: int) -> List[Dict]:
        """Get recently unlocked achievements"""
        unlocked = [
            {
                "name": self.achievements[p.achievement_id].name,
                "icon": self.achievements[p.achievement_id].icon,
                "date": p.unlock_date
            }
            for p in self.progress.values()
            if p.unlocked and p.unlock_date
        ]
        
        # Sort by date
        unlocked.sort(key=lambda x: x["date"], reverse=True)
        
        return unlocked[:limit]

# Singleton instance
_achievement_manager: Optional[AchievementManager] = None

def get_achievement_manager() -> AchievementManager:
    """Get the singleton AchievementManager instance"""
    global _achievement_manager
    if _achievement_manager is None:
        _achievement_manager = AchievementManager()
    return _achievement_manager