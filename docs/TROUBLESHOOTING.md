# 🔧 Troubleshooting: No Sounds in Claude Code

## Root Cause Identified

**The Issue:** Claude Code uses different internal tools than expected:
- `ls` command → Uses **List** tool (not Bash)
- `cat` command → Uses **Read** tool (not Bash)
- Shell commands → Sometimes use **Shell** or **Execute** (not always Bash)

## Quick Fix

### Step 1: Update Configuration
```bash
# Run the fix script
python3 fix_claude_hooks.py
```

### Step 2: Restart Claude Code
```bash
# Exit current session
exit

# Start new session
claude
```

### Step 3: Test Again
```bash
> ls        # Now should play success sound
> cat /fake # Now should play error sound
```

## Why This Happened

Claude Code has **18+ different tools** internally:
- **List/LS** - Directory listing
- **Read** - File reading
- **Write** - File writing
- **Bash/Shell/Execute** - Command execution
- **TodoWrite** - Todo management
- And many more...

Our initial setup only configured hooks for a few tools (Bash, Edit, Write).

## Complete Tool Mapping

| User Action | Claude Tool | Hook Needed |
|-------------|------------|-------------|
| `ls` | List | List success hook |
| `cat file` | Read | Read success/error hook |
| `echo "test"` | Bash/Shell | Bash success hook |
| `./script.sh` | Execute | Execute success/error hook |
| Create file | Write | Write success hook |
| Edit file | Edit/MultiEdit | Edit success hook |
| Search files | Grep/Glob | Grep success hook |
| Todo tasks | TodoWrite | TodoWrite success hook |

## Verification Steps

### 1. Check Hook Configuration
```bash
cat ~/.config/claude/settings.json | grep -c "success"
# Should show 30+ lines (many tool hooks)
```

### 2. Test Each Tool Type
```bash
# In Claude Code:
> ls                    # List tool → success sound
> cat README.md         # Read tool → success sound
> echo "test"           # Bash tool → success sound
> grep "test" *.md      # Grep tool → success sound
> cat /nonexistent      # Read tool → error sound
```

### 3. Monitor Hook Execution
```bash
# In another terminal, watch for hook calls:
ps aux | grep play_sound_async
```

## Common Issues & Solutions

### Issue: Still No Sounds After Fix

**Solution 1:** Force reload settings
```bash
# Clear Claude Code cache
rm -rf ~/.cache/claude/*

# Restart Claude Code
claude
```

**Solution 2:** Check hook permissions
```bash
# Make all hooks executable
chmod +x hooks/*.sh
ls -la hooks/
```

**Solution 3:** Test hooks directly
```bash
# Test a hook manually
./hooks/on_success.sh
# Should hear success sound
```

### Issue: Some Commands Work, Others Don't

This means partial configuration. Run:
```bash
python3 fix_claude_hooks.py
```

This adds ALL 18+ tools to the configuration.

### Issue: Sounds Play in Terminal but Not Claude Code

**Check 1:** Process running
```bash
# Check if Claude Code is using the config
lsof ~/.config/claude/settings.json
```

**Check 2:** Python path
```bash
# Ensure python3 is available
which python3
# Should show: /usr/bin/python3 or similar
```

## Testing Checklist

✅ **After fix, you should hear sounds for:**
- [ ] `ls` command (List tool)
- [ ] `cat file` command (Read tool)
- [ ] `echo "test"` command (Bash tool)
- [ ] `pwd` command (Shell tool)
- [ ] Creating a file (Write tool)
- [ ] Editing a file (Edit tool)
- [ ] Searching with grep (Grep tool)
- [ ] Todo operations (TodoWrite tool)
- [ ] Failed commands (error sounds)

## Debug Mode

To see what's happening behind the scenes:

### 1. Enable verbose logging
```bash
# In Claude Code, check what tools are being used:
> /status
# Shows current configuration
```

### 2. Test with debug output
```bash
# Modify a hook temporarily for debugging:
echo '#!/bin/bash
echo "Hook triggered: on_success.sh" >> /tmp/claude_hooks.log
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/../scripts/play_sound_async.py" success &' > hooks/on_success_debug.sh

chmod +x hooks/on_success_debug.sh

# Then check the log:
tail -f /tmp/claude_hooks.log
```

## Final Notes

**Why the comprehensive approach works:**
- Covers ALL possible Claude Code tools
- Future-proof against new tools
- Consistent experience across all commands
- No gaps in sound feedback

**The fix ensures:**
- ✅ All 18+ tools have hooks
- ✅ Both success and error states covered
- ✅ Special handling for TodoWrite and Test tools
- ✅ Non-blocking async execution

After running `python3 fix_claude_hooks.py` and restarting Claude Code, you should hear Zelda sounds for ALL operations!