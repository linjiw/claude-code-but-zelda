# 🎮 Zelda Sounds Testing Guide

## Quick Test Commands

### 1. Test Individual Sounds (Instant Feedback)
```bash
# Test each sound type
python3 scripts/play_sound_async.py success     # Cooking Success
python3 scripts/play_sound_async.py error       # Cooking Fail
python3 scripts/play_sound_async.py warning     # Assassin Appear
python3 scripts/play_sound_async.py todo_complete # GetHeart
python3 scripts/play_sound_async.py progress    # GetSmall (rupee)
```

### 2. Full Demo (Hear All Sounds)
```bash
./demo_sounds.sh
# Or use the shortcut:
./zelda-test
```

## Testing with Claude Code

### Test 1: Success Sound 🎵
**What to do:**
```bash
echo "test" > test.txt
```

**What you'll hear:** 
- **Cooking Success** sound (positive chime)
- **When:** Right after the command executes successfully

---

### Test 2: Error Sound ❌
**What to do:**
```bash
cat /nonexistent/file.txt
```

**What you'll hear:**
- **Cooking Fail** sound (negative tone)
- **When:** Immediately when the command fails

---

### Test 3: Todo Complete 📝
**What to do:**
Tell Claude: "Create a todo list with 3 items, then mark one as complete"

**What you'll hear:**
- **GetHeart** sound (achievement!)
- **When:** When Claude marks the todo item as completed

---

### Test 4: File Operations 📄
**What to do:**
Tell Claude: "Create a new file called hello.py with a print statement"

**What you'll hear:**
- **Cooking Success** when file is written
- **Multiple success sounds** as Claude works

---

### Test 5: Multiple Quick Actions 🏃
**What to do:**
```bash
ls && pwd && date && whoami
```

**What you'll hear:**
- **Rapid success sounds** (might overlap)
- Shows that sounds don't block each other

## Expected Sound Behaviors

### ✅ What's NORMAL:

1. **Slight delay** (0.02-0.05 seconds)
   - Sound starts just after the action completes
   - This is normal and doesn't block anything

2. **Overlapping sounds**
   - Multiple sounds can play at once
   - Your OS mixes them together
   - This is expected for rapid commands

3. **Different volumes**
   - Some sounds are naturally louder/quieter
   - Adjust system volume to preference (30-50% recommended)

4. **Sound continues after command finishes**
   - Longer sounds (1-2 seconds) keep playing
   - Claude Code doesn't wait for them to finish

### ⚠️ What's NOT normal:

1. **No sounds at all**
   - Check: `./install.sh` was run
   - Check: System volume isn't muted
   - Test: `afplay sounds/success.wav` (macOS)

2. **Claude Code freezing**
   - Should NEVER happen with async player
   - If it does, check hooks are using `play_sound_async.py`

3. **Error messages in Claude**
   - Sounds fail silently
   - If you see errors, hooks might be misconfigured

## Interactive Test Session

Try this sequence in Claude Code to hear various sounds:

```
1. "Create a simple Python hello world script"
   → Hear: Success sound when file is created

2. "Run the Python script"  
   → Hear: Success sound when it executes

3. "Create a todo: Fix bug, Add feature, Write tests"
   → Hear: Success sounds during creation

4. "Mark 'Fix bug' as complete"
   → Hear: GetHeart (todo complete) sound

5. "Try to read a file that doesn't exist"
   → Hear: Error sound

6. "Search for 'TODO' in all Python files"
   → Hear: Success sound for search operation
```

## Volume & Timing Guide

### Recommended Settings:
- **System Volume:** 30-50%
- **Best for:** Background feedback without distraction

### Sound Duration Reference:
| Sound | Duration | Type |
|-------|----------|------|
| GetSmall (rupee) | 0.4s | Quick ping |
| Cooking Success | 0.8s | Short melody |
| Cooking Fail | 0.9s | Error tone |
| GetHeart | 1.0s | Achievement |
| GetLarge | 1.1s | Big success |
| Assassin Appear | 0.5s | Alert |
| Game Over | 1.1s | Failure |

## Performance Verification

### Test that sounds don't block:
```bash
# This should complete instantly (< 0.1 seconds)
time python3 scripts/play_sound_async.py success

# Output should show:
# real    0m0.028s  (or similar small number)
```

### Test rapid sounds:
```bash
# Run 10 sounds rapidly
for i in {1..10}; do
    python3 scripts/play_sound_async.py progress &
done

# Should hear multiple rupee sounds overlapping
# Commands return immediately
```

## Troubleshooting

### No sounds?
```bash
# 1. Test your audio system
afplay sounds/success.wav  # macOS
aplay sounds/success.wav   # Linux

# 2. Check hooks are configured
cat ~/.config/claude/settings.json | grep hook

# 3. Reinstall
./install.sh
```

### Too loud/quiet?
- Adjust system volume
- All sounds use system audio settings
- No in-app volume control (by design for simplicity)

### Want different sounds?
```bash
# Replace any .wav file in sounds/ directory
# Keep the same filename
# Run: ./zelda-update
```

## What Success Looks Like

✅ **You'll know it's working when:**
1. Every command gives audio feedback
2. Sounds play instantly (no delay)
3. Claude Code remains responsive
4. Different events have distinct sounds
5. It feels like a video game achievement system!

## Fun Things to Try

1. **Speed run:** Execute many commands quickly to hear a symphony
2. **Todo symphony:** Create and complete multiple todos rapidly  
3. **Error percussion:** Intentionally cause different types of errors
4. **The full orchestra:** Run your test suite with sound effects

---

Enjoy your legendary coding experience! 🗡️✨

*Tip: After a day of coding with sounds, you'll instinctively know if commands succeeded just by the audio feedback!*