#!/usr/bin/env python3
"""
Zelda Core - All-in-one module for Claude Code Zelda integration
This single module contains all functionality for stats, combos, achievements, and commands
"""

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum

# ============================================================================
# CONFIGURATION
# ============================================================================

ZELDA_DIR = Path.home() / ".zelda"
ZELDA_DIR.mkdir(exist_ok=True)

STATS_FILE = ZELDA_DIR / "stats.json"
ACHIEVEMENTS_FILE = ZELDA_DIR / "achievements.json"
CONFIG_FILE = ZELDA_DIR / "config.json"
SESSIONS_DIR = ZELDA_DIR / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

# Default configuration
DEFAULT_CONFIG = {
    "volume": 100,
    "sounds": {
        "enabled": True,
        "combo": True,
        "achievements": True,
        "ambient": False
    },
    "notifications": {
        "achievements": True,
        "milestones": True,
        "combos": True
    },
    "theme": "tears-of-the-kingdom"
}

# ============================================================================
# STATISTICS SYSTEM
# ============================================================================

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

@dataclass
class AllTimeStats:
    """Cumulative statistics across all sessions"""
    total_sessions: int = 0
    total_commands: int = 0
    total_successes: int = 0
    total_failures: int = 0
    longest_streak: int = 0
    longest_streak_date: Optional[str] = None
    total_time_coding: float = 0.0
    favorite_tool: Optional[str] = None
    tool_usage: Dict[str, int] = field(default_factory=dict)
    achievements: Dict[str, str] = field(default_factory=dict)
    milestones: Dict[str, str] = field(default_factory=dict)

# ============================================================================
# COMBO SYSTEM
# ============================================================================

class ComboLevel(Enum):
    """Combo level thresholds"""
    NONE = (0, None)
    BRONZE = (3, "item_small.wav")
    SILVER = (5, "heart_get.wav")
    GOLD = (10, "achievement.wav")
    PLATINUM = (20, "shrine_complete.wav")
    MASTER = (50, "session_start.wav")
    
    def __init__(self, threshold: int, sound: Optional[str]):
        self.threshold = threshold
        self.sound = sound

@dataclass
class ComboState:
    """Current combo state"""
    current_streak: int = 0
    highest_streak: int = 0
    last_level_reached: str = "NONE"
    total_combos_achieved: int = 0

# ============================================================================
# ACHIEVEMENT SYSTEM
# ============================================================================

ACHIEVEMENTS = {
    # Milestone Achievements
    "first_step": {"name": "First Steps", "desc": "Execute your first command", "req": 1, "icon": "👶"},
    "apprentice": {"name": "Apprentice Coder", "desc": "Execute 10 commands", "req": 10, "icon": "📚"},
    "journeyman": {"name": "Journeyman", "desc": "Execute 50 commands", "req": 50, "icon": "⚔️"},
    "master": {"name": "Master Coder", "desc": "Execute 100 commands", "req": 100, "icon": "🏆"},
    "legend": {"name": "Legendary Hero", "desc": "Execute 500 commands", "req": 500, "icon": "👑"},
    
    # Combo Achievements
    "combo_bronze": {"name": "Combo Starter", "desc": "3-command streak", "req": 3, "icon": "🥉"},
    "combo_silver": {"name": "Combo Pro", "desc": "5-command streak", "req": 5, "icon": "🥈"},
    "combo_gold": {"name": "Combo Master", "desc": "10-command streak", "req": 10, "icon": "🥇"},
    "combo_platinum": {"name": "Combo Legend", "desc": "20-command streak", "req": 20, "icon": "💎"},
    
    # Perfectionist Achievements
    "flawless_ten": {"name": "Flawless Ten", "desc": "10 commands without errors", "req": 10, "icon": "✨"},
    "error_free": {"name": "Error Free", "desc": "25 commands without errors", "req": 25, "icon": "💯"},
}

@dataclass
class AchievementProgress:
    """Track achievement progress"""
    achievements_unlocked: Dict[str, str] = field(default_factory=dict)  # id: unlock_date
    progress: Dict[str, int] = field(default_factory=dict)  # id: current_progress

# ============================================================================
# MAIN ZELDA MANAGER CLASS
# ============================================================================

class ZeldaManager:
    """Main manager for all Zelda features"""
    
    def __init__(self):
        self.config = self._load_config()
        self.all_time_stats = self._load_all_time_stats()
        self.current_session: Optional[SessionStats] = None
        self.combo_state = ComboState()
        self.achievement_progress = self._load_achievements()
        self.error_free_count = 0
        
    # Configuration Management
    def _load_config(self) -> dict:
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save configuration to file"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def update_config(self, key: str, value):
        """Update configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.save_config()
        
    # Statistics Management
    def _load_all_time_stats(self) -> AllTimeStats:
        """Load all-time statistics"""
        if STATS_FILE.exists():
            try:
                with open(STATS_FILE, 'r') as f:
                    data = json.load(f)
                    return AllTimeStats(**data)
            except:
                pass
        return AllTimeStats()
    
    def save_stats(self):
        """Save statistics to file"""
        with open(STATS_FILE, 'w') as f:
            json.dump(asdict(self.all_time_stats), f, indent=2)
    
    def start_session(self, session_id: str):
        """Start a new coding session"""
        self.current_session = SessionStats(
            session_id=session_id,
            start_time=datetime.now().isoformat()
        )
        self.all_time_stats.total_sessions += 1
        self.combo_state = ComboState()  # Reset combo for new session
        self.error_free_count = 0
        self.save_stats()
    
    def end_session(self):
        """End current session"""
        if not self.current_session:
            return
            
        self.current_session.end_time = datetime.now().isoformat()
        
        # Update all-time stats
        self.all_time_stats.total_commands += self.current_session.total_commands
        self.all_time_stats.total_successes += self.current_session.successful_commands
        self.all_time_stats.total_failures += self.current_session.failed_commands
        
        if self.current_session.max_streak > self.all_time_stats.longest_streak:
            self.all_time_stats.longest_streak = self.current_session.max_streak
            self.all_time_stats.longest_streak_date = datetime.now().isoformat()
        
        # Save session
        session_file = SESSIONS_DIR / f"{self.current_session.session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(asdict(self.current_session), f, indent=2)
        
        self.save_stats()
        self.current_session = None
    
    def record_command(self, tool_name: str, success: bool) -> List[str]:
        """Record a command and return sounds to play"""
        if not self.current_session:
            return []
            
        sounds = []
        
        # Update statistics
        self.current_session.total_commands += 1
        if success:
            self.current_session.successful_commands += 1
            self.error_free_count += 1
        else:
            self.current_session.failed_commands += 1
            self.error_free_count = 0
        
        # Update tool usage
        self.current_session.tools_used[tool_name] = \
            self.current_session.tools_used.get(tool_name, 0) + 1
        
        # Check combo
        combo_sound = self._update_combo(success)
        if combo_sound:
            sounds.append(combo_sound)
        
        # Check achievements
        achievement_sounds = self._check_achievements()
        sounds.extend(achievement_sounds)
        
        return sounds
    
    def _update_combo(self, success: bool) -> Optional[str]:
        """Update combo state and return sound if milestone reached"""
        if success:
            self.combo_state.current_streak += 1
            if self.combo_state.current_streak > self.combo_state.highest_streak:
                self.combo_state.highest_streak = self.combo_state.current_streak
            
            # Check for combo milestone
            for level in [ComboLevel.MASTER, ComboLevel.PLATINUM, ComboLevel.GOLD, 
                         ComboLevel.SILVER, ComboLevel.BRONZE]:
                if self.combo_state.current_streak == level.threshold:
                    self.combo_state.last_level_reached = level.name
                    self.combo_state.total_combos_achieved += 1
                    if self.config["sounds"]["combo"]:
                        return level.sound
        else:
            # Combo broken
            if self.combo_state.current_streak >= 3:
                self.combo_state.current_streak = 0
                self.combo_state.last_level_reached = "NONE"
                return "damage.wav"
            self.combo_state.current_streak = 0
        
        return None
    
    # Achievement Management
    def _load_achievements(self) -> AchievementProgress:
        """Load achievement progress"""
        if ACHIEVEMENTS_FILE.exists():
            try:
                with open(ACHIEVEMENTS_FILE, 'r') as f:
                    data = json.load(f)
                    return AchievementProgress(**data)
            except:
                pass
        return AchievementProgress()
    
    def save_achievements(self):
        """Save achievement progress"""
        with open(ACHIEVEMENTS_FILE, 'w') as f:
            json.dump(asdict(self.achievement_progress), f, indent=2)
    
    def _check_achievements(self) -> List[str]:
        """Check for newly unlocked achievements"""
        if not self.current_session:
            return []
            
        sounds = []
        total_commands = self.all_time_stats.total_commands + self.current_session.total_commands
        
        for aid, adata in ACHIEVEMENTS.items():
            if aid in self.achievement_progress.achievements_unlocked:
                continue
                
            progress = 0
            
            # Check different achievement types
            if aid in ["first_step", "apprentice", "journeyman", "master", "legend"]:
                progress = total_commands
            elif aid in ["combo_bronze", "combo_silver", "combo_gold", "combo_platinum"]:
                progress = self.combo_state.current_streak
            elif aid in ["flawless_ten", "error_free"]:
                progress = self.error_free_count
            
            self.achievement_progress.progress[aid] = progress
            
            if progress >= adata["req"]:
                # Achievement unlocked!
                self.achievement_progress.achievements_unlocked[aid] = datetime.now().isoformat()
                self.current_session.achievements_unlocked.append(aid)
                
                if self.config["sounds"]["achievements"]:
                    sounds.append("achievement.wav")
                
                # Log achievement (for display in Claude Code)
                self._log_achievement(adata["name"], adata["icon"])
                break  # Only unlock one at a time
        
        if sounds:
            self.save_achievements()
        
        return sounds
    
    def _log_achievement(self, name: str, icon: str):
        """Log achievement unlock for display"""
        log_file = Path("/tmp/zelda_notifications.log")
        with open(log_file, "a") as f:
            f.write(f"ACHIEVEMENT:{icon} {name}\n")
    
    # Command Processing
    def process_command(self, command: str) -> str:
        """Process @zelda commands and return formatted response"""
        parts = command.lower().strip().split()
        if len(parts) < 2 or parts[0] != "@zelda":
            return ""
        
        cmd = parts[1] if len(parts) > 1 else "help"
        args = parts[2:] if len(parts) > 2 else []
        
        if cmd == "stats":
            return self._format_stats()
        elif cmd == "achievements":
            return self._format_achievements()
        elif cmd == "combo":
            return self._format_combo()
        elif cmd == "config":
            return self._handle_config(args)
        elif cmd == "help":
            return self._format_help()
        else:
            return f"❓ Unknown command: {cmd}\nType `@zelda help` for available commands."
    
    def _format_stats(self) -> str:
        """Format statistics for display"""
        stats = self.all_time_stats
        session = self.current_session
        
        response = "# 📊 Zelda Coding Statistics\n\n"
        response += "## All-Time Stats\n"
        response += f"- **Total Commands:** {stats.total_commands}\n"
        response += f"- **Success Rate:** {(stats.total_successes/max(stats.total_commands,1)*100):.1f}%\n"
        response += f"- **Longest Streak:** {stats.longest_streak} 🔥\n"
        response += f"- **Total Sessions:** {stats.total_sessions}\n"
        response += f"- **Favorite Tool:** {stats.favorite_tool or 'None yet'}\n"
        
        if session:
            response += "\n## Current Session\n"
            response += f"- **Commands:** {session.total_commands}\n"
            response += f"- **Success Rate:** {session.success_rate:.1f}%\n"
            response += f"- **Current Streak:** {self.combo_state.current_streak}\n"
            response += f"- **Max Streak:** {session.max_streak}\n"
        
        response += "\n*Keep coding, Hero of Hyrule!* 🗡️✨"
        return response
    
    def _format_achievements(self) -> str:
        """Format achievements for display"""
        response = "# 🏆 Achievements\n\n"
        
        unlocked = len(self.achievement_progress.achievements_unlocked)
        total = len(ACHIEVEMENTS)
        percent = (unlocked / total * 100) if total > 0 else 0
        
        response += f"**Progress:** {unlocked}/{total} ({percent:.0f}%)\n\n"
        
        # Progress bar
        bar_length = 20
        filled = int(bar_length * percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        response += f"`[{bar}]`\n\n"
        
        # List achievements
        response += "## Unlocked\n"
        for aid, unlock_date in self.achievement_progress.achievements_unlocked.items():
            ach = ACHIEVEMENTS[aid]
            response += f"- {ach['icon']} **{ach['name']}** - {ach['desc']}\n"
        
        if not self.achievement_progress.achievements_unlocked:
            response += "*No achievements yet - keep coding!*\n"
        
        response += "\n## Locked\n"
        locked_count = 0
        for aid, ach in ACHIEVEMENTS.items():
            if aid not in self.achievement_progress.achievements_unlocked:
                progress = self.achievement_progress.progress.get(aid, 0)
                response += f"- {ach['icon']} {ach['name']} ({progress}/{ach['req']})\n"
                locked_count += 1
                if locked_count >= 5:  # Show only first 5
                    response += f"- *...and {total - unlocked - 5} more*\n"
                    break
        
        return response
    
    def _format_combo(self) -> str:
        """Format combo status for display"""
        response = "# ⚡ Combo Status\n\n"
        response += f"**Current Streak:** {self.combo_state.current_streak} 🔥\n"
        response += f"**Highest Streak:** {self.combo_state.highest_streak}\n"
        response += f"**Current Level:** {self.combo_state.last_level_reached}\n\n"
        
        # Next milestone
        next_level = None
        for level in [ComboLevel.BRONZE, ComboLevel.SILVER, ComboLevel.GOLD, 
                     ComboLevel.PLATINUM, ComboLevel.MASTER]:
            if self.combo_state.current_streak < level.threshold:
                next_level = level
                break
        
        if next_level:
            response += f"**Next Milestone:** {next_level.threshold} commands\n"
            progress = self.combo_state.current_streak / next_level.threshold * 100
            bar_length = 20
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            response += f"`[{bar}]` {progress:.0f}%\n"
        
        response += "\n## Combo Levels\n"
        response += "- 🥉 Bronze: 3 commands\n"
        response += "- 🥈 Silver: 5 commands\n"
        response += "- 🥇 Gold: 10 commands\n"
        response += "- 💎 Platinum: 20 commands\n"
        response += "- 🔥 Master: 50 commands\n"
        
        return response
    
    def _handle_config(self, args: List[str]) -> str:
        """Handle configuration commands"""
        if not args:
            # Show current config
            response = "# ⚙️ Configuration\n\n"
            response += "```json\n"
            response += json.dumps(self.config, indent=2)
            response += "\n```\n\n"
            response += "To change settings: `@zelda config <key> <value>`\n"
            response += "Example: `@zelda config volume 50`"
            return response
        
        if len(args) < 2:
            return "❌ Usage: `@zelda config <key> <value>`"
        
        key = args[0]
        value = " ".join(args[1:])
        
        # Parse value
        if value.lower() in ["true", "false"]:
            value = value.lower() == "true"
        elif value.isdigit():
            value = int(value)
        
        self.update_config(key, value)
        return f"✅ Configuration updated: {key} = {value}"
    
    def _format_help(self) -> str:
        """Format help message"""
        return """# 🎮 Zelda Claude Code Commands

## Available Commands

- `@zelda stats` - View your coding statistics
- `@zelda achievements` - Display achievement progress
- `@zelda combo` - Show current combo status
- `@zelda config` - View/change configuration
- `@zelda config <key> <value>` - Set configuration value
- `@zelda help` - Show this help message

## Configuration Keys

- `volume` - Sound volume (0-100)
- `sounds.combo` - Enable combo sounds (true/false)
- `sounds.achievements` - Enable achievement sounds (true/false)
- `notifications.achievements` - Show achievement notifications (true/false)

## Examples

```
@zelda stats
@zelda config volume 75
@zelda config sounds.combo false
```

*May the Triforce guide your code!* 🗡️✨"""

# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_manager: Optional[ZeldaManager] = None

def get_manager() -> ZeldaManager:
    """Get singleton ZeldaManager instance"""
    global _manager
    if _manager is None:
        _manager = ZeldaManager()
    return _manager