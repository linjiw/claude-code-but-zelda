# 🎮 Final Zelda Sound Shopping List for Claude Code

## 📦 Essential Sounds to Purchase (All ≤10 seconds!)

Based on the sound database analysis with the **10-second limit**, here are the **PERFECT** sounds to purchase:

### ✅ Core Action Sounds

| ID | Sound Name | Use Case | Duration | Size |
|----|------------|----------|----------|------|
| **#0244** | Cooking Success Finish | Command success | **0:02** | 0.91 MB |
| **#0238** | Cooking Fail Finish | Command error | **0:03** | 0.93 MB |
| **#0744** | GetSmall | Minor success | **0:02** | 0.91 MB |
| **#0743** | GetMedium | Todo completed | **0:05** | 1.03 MB |
| **#0741** | GetLarge | Major achievement | **0:06** | 1.06 MB |
| **#0740** | GetHeart | Health/life up | **0:06** | 1.03 MB |

### ⚔️ Testing & Build Sounds

| ID | Sound Name | Use Case | Duration | Size |
|----|------------|----------|----------|------|
| **#0952** | Mercenary Clear | Test suite pass | **0:04** | 0.99 MB |
| **#0363** | Dm F S Y Game Over | Test suite fail | **0:06** | 1.05 MB |
| **#0369** | Dm F S Y Recycle Box Fail | Build error | **0:04** | 0.98 MB |

### 🔔 Alerts & Notifications

| ID | Sound Name | Use Case | Duration | Size |
|----|------------|----------|----------|------|
| **#0206** | Assassin Appear | Warning/Alert | **0:03** | 0.94 MB |
| **#0943** | Location Open Small Dungeon Sub | File opened | **0:03** | 0.93 MB |

### 🔍 Search & Discovery

| ID | Sound Name | Use Case | Duration | Size |
|----|------------|----------|----------|------|
| **#0364** | Dm F S Y Hide Chara Discovery | Search found | **0:04** | 0.97 MB |
| **#0250** | Deep Hole Dive Blowing 0 | Grep success | **0:04** | 0.95 MB |

### 🎯 Session Management

| ID | Sound Name | Use Case | Duration | Size |
|----|------------|----------|----------|------|
| **#0124** | SmallDungeon Start | Session start | **0:10** | 1.18 MB |
| **#0164** | UotoriVillage Night Intro Fade | Evening session | **0:09** | 1.15 MB |

---

## 💰 Purchase Summary

**Total Sounds:** 15 unique sounds  
**Max Duration:** 10 seconds (most are 2-6 seconds!)  
**Total Size:** ~15 MB  
**Estimated Cost:** $15-30 (assuming $1-2 per sound)

### ✨ Key Benefits of Short Sounds:
- **No interruption** to coding flow
- **Instant feedback** (2-3 second sounds)
- **Less fatigue** from repetitive long sounds
- **Stackable** - multiple sounds can play quickly

## 🔍 How to Use the Search Tool

```bash
# Search for specific sounds
python3 zelda_sound_search.py search "battle"

# Get sounds by ID
python3 zelda_sound_search.py id 243 237 740

# Find all needed sounds automatically
python3 zelda_sound_search.py needed

# Show database statistics
python3 zelda_sound_search.py stats
```

## 📝 Sound ID Quick Reference

### Primary Sounds (2-3 seconds - Ultra Fast!)
- **#244** - Success (Cooking Success Finish) - 2 sec
- **#238** - Error (Cooking Fail Finish) - 3 sec
- **#744** - Small Win (GetSmall) - 2 sec
- **#206** - Alert (Assassin Appear) - 3 sec

### Achievement Sounds (5-6 seconds)
- **#743** - Todo Complete (GetMedium) - 5 sec
- **#741** - Major Achievement (GetLarge) - 6 sec
- **#363** - Test Fail (Game Over) - 6 sec

### Perfect Sound Mapping
```javascript
const soundMap = {
  // Ultra-fast feedback (2-3 sec)
  "bash_success": "#244",  // Cooking Success Finish
  "bash_error": "#238",    // Cooking Fail Finish
  "file_saved": "#744",    // GetSmall
  
  // Milestones (5-6 sec)
  "todo_complete": "#743", // GetMedium
  "all_tests_pass": "#952", // Mercenary Clear
  "tests_fail": "#363",    // Game Over
  
  // Alerts (3-4 sec)
  "warning": "#206",       // Assassin Appear
  "search_found": "#364",  // Discovery
  
  // Session (9-10 sec)
  "session_start": "#124", // SmallDungeon Start
}
```

## 🎯 Next Steps

1. **Purchase these 15 sounds** from the Zelda sound store
2. **Convert to WAV format** using the existing conversion scripts
3. **Map to appropriate file names** (success.wav, error.wav, etc.)
4. **Test with the demo script** to ensure all sounds work
5. **Update the hook handler** to use the new comprehensive mapping

---

*With these sounds, every coding session becomes a legendary adventure! 🗡️✨*