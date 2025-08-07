#!/usr/bin/env python3
"""
Combo Detection System for Zelda Claude Code
Tracks consecutive successes and plays escalating sounds
"""

from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum

class ComboLevel(Enum):
    """Combo level thresholds and their rewards"""
    NONE = (0, None)
    BRONZE = (3, "item_small.wav")      # 3 in a row - small achievement
    SILVER = (5, "heart_get.wav")       # 5 in a row - nice!
    GOLD = (10, "achievement.wav")      # 10 in a row - impressive!
    PLATINUM = (20, "shrine_complete.wav")  # 20 in a row - legendary!
    MASTER = (50, "session_start.wav")  # 50 in a row - god mode!
    
    def __init__(self, threshold: int, sound: Optional[str]):
        self.threshold = threshold
        self.sound = sound

@dataclass
class ComboState:
    """Current combo state"""
    current_streak: int = 0
    highest_streak: int = 0
    last_level_reached: ComboLevel = ComboLevel.NONE
    total_combos_achieved: int = 0
    
class ComboTracker:
    """Tracks and manages combo streaks"""
    
    def __init__(self):
        self.state = ComboState()
        self.combo_broken_sound = "damage.wav"
        
    def record_action(self, success: bool) -> Tuple[Optional[str], Optional[str]]:
        """
        Record an action and return sounds to play
        Returns: (combo_sound, break_sound) - one will always be None
        """
        if success:
            return self._handle_success()
        else:
            return self._handle_failure()
    
    def _handle_success(self) -> Tuple[Optional[str], None]:
        """Handle a successful action"""
        self.state.current_streak += 1
        
        # Update highest streak
        if self.state.current_streak > self.state.highest_streak:
            self.state.highest_streak = self.state.current_streak
        
        # Check for combo milestones
        combo_sound = self._check_combo_milestone()
        
        return (combo_sound, None)
    
    def _handle_failure(self) -> Tuple[None, Optional[str]]:
        """Handle a failed action"""
        break_sound = None
        
        # Only play break sound if we had a streak going
        if self.state.current_streak >= 3:
            break_sound = self.combo_broken_sound
        
        # Reset streak
        self.state.current_streak = 0
        self.state.last_level_reached = ComboLevel.NONE
        
        return (None, break_sound)
    
    def _check_combo_milestone(self) -> Optional[str]:
        """Check if we've reached a new combo level"""
        current_level = self._get_combo_level(self.state.current_streak)
        
        # Only play sound when we first reach a new level
        if current_level != self.state.last_level_reached and \
           current_level != ComboLevel.NONE:
            
            # We've reached a new level!
            self.state.last_level_reached = current_level
            self.state.total_combos_achieved += 1
            
            return current_level.sound
        
        return None
    
    def _get_combo_level(self, streak: int) -> ComboLevel:
        """Get the combo level for a given streak"""
        # Check from highest to lowest
        for level in [ComboLevel.MASTER, ComboLevel.PLATINUM, 
                     ComboLevel.GOLD, ComboLevel.SILVER, ComboLevel.BRONZE]:
            if streak >= level.threshold:
                return level
        return ComboLevel.NONE
    
    def get_combo_status(self) -> dict:
        """Get current combo status for display"""
        current_level = self._get_combo_level(self.state.current_streak)
        next_level = self._get_next_level(self.state.current_streak)
        
        status = {
            "current_streak": self.state.current_streak,
            "highest_streak": self.state.highest_streak,
            "current_level": current_level.name,
            "total_combos": self.state.total_combos_achieved
        }
        
        if next_level:
            status["next_milestone"] = next_level.threshold
            status["progress_to_next"] = f"{self.state.current_streak}/{next_level.threshold}"
        
        return status
    
    def _get_next_level(self, streak: int) -> Optional[ComboLevel]:
        """Get the next combo level to reach"""
        for level in [ComboLevel.BRONZE, ComboLevel.SILVER, 
                     ComboLevel.GOLD, ComboLevel.PLATINUM, ComboLevel.MASTER]:
            if streak < level.threshold:
                return level
        return None
    
    def reset(self):
        """Reset combo state"""
        self.state = ComboState()

# Singleton instance
_combo_tracker: Optional[ComboTracker] = None

def get_combo_tracker() -> ComboTracker:
    """Get the singleton ComboTracker instance"""
    global _combo_tracker
    if _combo_tracker is None:
        _combo_tracker = ComboTracker()
    return _combo_tracker