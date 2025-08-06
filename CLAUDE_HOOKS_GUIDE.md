# 🎮 Claude Code Zelda Sounds - Complete Setup Guide

## ✅ Current Status

**Hooks are now properly configured** according to Claude Code's official documentation!

## How Claude Code Hooks Work

Claude Code hooks are shell commands that execute at specific points:
1. **PostToolUse** - After any tool executes (ls, cat, write files, etc.)
2. **Notification** - When Claude needs your input or permission
3. **Stop** - When Claude finishes responding
4. **PreToolUse** - Before tools execute (can block them)

## What We've Implemented

### Hook Script: `play_sound_hook.py`
- Receives JSON data via stdin from Claude Code
- Parses tool execution results
- Plays appropriate Zelda sound based on success/failure
- Non-blocking (uses async playback)

### Sound Mappings
| Event | Sound | Zelda Track |
|-------|-------|-------------|
| Tool Success | `success.wav` | Cooking Success |
| Tool Error | `error.wav` | Cooking Fail |
| Todo Complete | `todo_complete.wav` | GetHeart |
| Test Pass | `puzzle_solved.wav` | GetMedium |
| Test Fail | `damage.wav` | Game Over |
| Notification | `warning.wav` | Assassin Appear |
| Claude Finishes | `item_get.wav` | GetLarge |

## Testing Your Setup

### Step 1: Verify Hook Configuration

In Claude Code, run:
```
/hooks
```

You should see:
- **PostToolUse** with matcher `*` → play_sound_hook.py
- **Notification** → play_sound_hook.py  
- **Stop** → play_sound_hook.py

### Step 2: Restart Claude Code

**IMPORTANT**: Hooks are captured at startup. You must restart:
```bash
# Exit Claude Code
exit

# Start fresh
claude
```

### Step 3: Test Commands

```bash
# Success sound test
> ls
# You should hear: Cooking Success

# Error sound test  
> cat /nonexistent
# You should hear: Cooking Fail

# Todo completion test
> Create a todo list with 3 items
> Mark one as complete
# You should hear: GetHeart when marking complete
```

## How It Actually Works

1. **You type a command** (e.g., `ls`)
2. **Claude uses a tool** (e.g., `List` tool)
3. **Tool executes** and returns result
4. **PostToolUse hook triggers**
5. **Hook receives JSON** with tool name, input, and response
6. **Hook script plays sound** based on success/failure
7. **Claude continues** (hook doesn't block)

### Example JSON Input to Hook

```json
{
  "session_id": "abc123",
  "hook_event_name": "PostToolUse",
  "tool_name": "List",
  "tool_input": {
    "path": "."
  },
  "tool_response": {
    "success": true,
    "files": ["file1.txt", "file2.py"]
  }
}
```

## Troubleshooting

### If No Sounds Play

1. **Check hooks are registered**:
   ```
   /hooks
   ```

2. **Verify hook script works**:
   ```bash
   echo '{"tool_name":"Test","tool_response":{"success":true}}' | python3 hooks/play_sound_hook.py
   ```
   Should hear success sound

3. **Check Claude debug output**:
   ```bash
   claude --debug
   ```
   Look for "Executing hooks" messages

4. **Ensure sounds exist**:
   ```bash
   ls -la sounds/*.wav
   afplay sounds/success.wav  # Test directly
   ```

### Common Issues

| Issue | Solution |
|-------|----------|
| No sounds at all | Restart Claude Code completely |
| Hooks not showing in `/hooks` | Check ~/.claude/settings.json |
| "Command not found" | Use absolute paths in hooks |
| Sounds delayed | Normal - async playback |

## Advanced Configuration

### Add More Specific Matchers

Edit `~/.claude/settings.json` to add tool-specific sounds:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "TodoWrite",
        "hooks": [{
          "type": "command",
          "command": "afplay /path/to/special_todo_sound.wav"
        }]
      },
      {
        "matcher": "*",
        "hooks": [{
          "type": "command",
          "command": "python3 /path/to/play_sound_hook.py"
        }]
      }
    ]
  }
}
```

### Add PreToolUse Hooks

Block dangerous operations with warning sounds:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "python3 /path/to/validate_command.py"
        }]
      }
    ]
  }
}
```

## Summary

✅ **Hooks configured correctly** using official Claude Code format
✅ **JSON stdin handling** implemented properly
✅ **All tools covered** with `*` matcher
✅ **Non-blocking execution** with async sound playback
✅ **Multiple event types** supported (PostToolUse, Notification, Stop)

**Next step**: Restart Claude Code and enjoy your Zelda sounds! 🎮