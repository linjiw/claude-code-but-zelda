# 🔄 Zelda Claude Code - Refactoring Plan

## 🎯 Ultimate Design Goal

**Make Zelda features completely native to Claude Code** - users should never need to leave Claude Code or run Python scripts manually.

## 🚫 Current Problems

1. **Manual Script Execution**: Users must run `python3 zelda_cli.py stats` outside Claude Code
2. **Scattered Configuration**: Settings across multiple files
3. **Complex Installation**: Multiple steps, manual configuration
4. **Standalone Feel**: Features feel disconnected from Claude Code
5. **Too Many Files**: Overwhelming directory structure

## ✅ Target Architecture

### **Vision: Everything Through Claude Code Commands**

Users type commands directly in Claude Code:
```
@zelda stats          # Show statistics
@zelda achievements   # Display achievements  
@zelda combo         # Show combo status
@zelda config        # Configure settings
@zelda volume 50     # Adjust volume
@zelda disable combo # Toggle features
```

These commands are intercepted by hooks and processed seamlessly.

## 📦 New Simplified Structure

```
zelda_claude/
├── install.sh                    # One-click installer
├── README.md                     # Simple user guide
├── zelda_core.py                # Single core module with all logic
├── hooks/
│   └── zelda_hook.py           # Single unified hook handler
├── sounds/                      # Sound files (unchanged)
├── config/
│   └── default_settings.json   # Default configuration
└── .zelda/                      # Hidden directory for internal use
    ├── stats.json
    ├── achievements.json
    └── user_config.json
```

## 🔧 Refactoring Steps

### Phase 1: Consolidation
1. **Merge all Python modules into single `zelda_core.py`**
   - Stats, combos, achievements in one file
   - Easier to maintain and deploy
   
2. **Create unified hook handler**
   - Single hook that handles everything
   - Intercepts `@zelda` commands via UserPromptSubmit
   - Returns formatted responses to Claude Code

3. **Remove standalone scripts**
   - No more `zelda_cli.py`
   - No more separate search scripts
   - Everything accessed through Claude Code

### Phase 2: Claude Code Integration

#### **Command Interception System**
```python
# In hook handler
def handle_user_prompt(prompt):
    if prompt.startswith("@zelda"):
        command = parse_zelda_command(prompt)
        result = execute_command(command)
        return format_for_claude(result)
```

#### **Response Formatting**
Return formatted markdown that Claude Code will display:
```python
def format_stats_response():
    return """
    ## 📊 Your Zelda Stats
    
    **Total Commands:** 150
    **Success Rate:** 92%
    **Current Streak:** 🔥 15
    **Best Streak:** 27
    
    Keep coding, Hero! 🗡️
    """
```

### Phase 3: Smart Features

1. **Auto-Configuration**
   - Detect Claude Code settings location
   - Auto-configure hooks on first run
   - No manual JSON editing

2. **Inline Settings**
   ```
   @zelda config volume 75
   @zelda config sounds.combo off
   @zelda config theme breath-of-the-wild
   ```

3. **Progress Notifications**
   - Achievement unlocks appear in Claude Code
   - Milestone notifications
   - Combo streak updates

### Phase 4: Installation Simplification

**New One-Line Install:**
```bash
curl -sSL https://zelda.claude/install | bash
```

Or local:
```bash
./install.sh
```

This script will:
1. Check dependencies
2. Configure Claude Code hooks
3. Set up sounds
4. Initialize stats
5. Show success message with instructions

## 🎮 User Experience Flow

### First Time Setup
1. User clones repo
2. Runs `./install.sh`
3. Done! Everything works in Claude Code

### Daily Usage
1. User codes normally in Claude Code
2. Sounds play automatically
3. Type `@zelda stats` anytime to check progress
4. Type `@zelda achievements` to see unlocks
5. Configure with `@zelda config [setting]`

### No More:
- Running Python scripts
- Checking terminal for stats
- Manual configuration editing
- Complex file management

## 📝 Implementation Priority

1. **HIGH**: Command interception via UserPromptSubmit hook
2. **HIGH**: Single consolidated Python module
3. **HIGH**: Formatted responses for Claude Code
4. **MEDIUM**: Auto-configuration system
5. **MEDIUM**: Inline settings commands
6. **LOW**: Web-based installer
7. **LOW**: Theme system

## 🚀 Benefits of Refactoring

1. **Native Feel**: Everything happens in Claude Code
2. **Zero Friction**: No context switching
3. **Intuitive**: Natural command syntax
4. **Maintainable**: Single core module
5. **Extensible**: Easy to add new features
6. **Professional**: Polished user experience

## 📊 Success Metrics

- Installation takes < 30 seconds
- All features accessible without leaving Claude Code
- No manual Python script execution needed
- Settings configurable through commands
- Stats/achievements display inline

## 🎯 End Goal

**A user installs once and never thinks about it again** - they just enjoy the enhanced coding experience with sounds, stats, and achievements all seamlessly integrated into their Claude Code workflow.

---

*Transform Claude Code into a game, not a game with Claude Code on the side*