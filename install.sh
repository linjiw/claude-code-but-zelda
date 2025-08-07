#!/bin/bash

# ============================================================================
# Zelda Claude Code - One-Click Installer
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print with color
print_color() {
    echo -e "${2}${1}${NC}"
}

# Header
clear
print_color "

   ╔═══════════════════════════════════════════╗
   ║   🎮 ZELDA CLAUDE CODE INSTALLER 🎮      ║
   ║   Transform coding into an adventure!     ║
   ╚═══════════════════════════════════════════╝
" "$BLUE"

print_color "Starting installation..." "$GREEN"

# ============================================================================
# 1. Check Prerequisites
# ============================================================================

print_color "\n[1/5] Checking prerequisites..." "$YELLOW"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    print_color "❌ Python 3 is required but not installed." "$RED"
    exit 1
fi
print_color "✅ Python 3 found" "$GREEN"

# Check for audio player
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v afplay &> /dev/null; then
        print_color "⚠️  afplay not found (should be included in macOS)" "$YELLOW"
    else
        print_color "✅ Audio player (afplay) found" "$GREEN"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v aplay &> /dev/null; then
        print_color "✅ Audio player (aplay) found" "$GREEN"
    elif command -v paplay &> /dev/null; then
        print_color "✅ Audio player (paplay) found" "$GREEN"
    else
        print_color "⚠️  No audio player found. Install alsa-utils or pulseaudio" "$YELLOW"
    fi
fi

# ============================================================================
# 2. Set up directory structure
# ============================================================================

print_color "\n[2/5] Setting up directories..." "$YELLOW"

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create .zelda directory in home
mkdir -p ~/.zelda
mkdir -p ~/.zelda/sessions
print_color "✅ Created ~/.zelda directory for data storage" "$GREEN"

# ============================================================================
# 3. Configure Claude Code Hooks
# ============================================================================

print_color "\n[3/5] Configuring Claude Code hooks..." "$YELLOW"

# Check if Claude settings directory exists
CLAUDE_SETTINGS_DIR="$HOME/.claude"
SETTINGS_FILE="$CLAUDE_SETTINGS_DIR/settings.json"

if [ ! -d "$CLAUDE_SETTINGS_DIR" ]; then
    mkdir -p "$CLAUDE_SETTINGS_DIR"
    print_color "✅ Created ~/.claude directory" "$GREEN"
fi

# Create or update settings.json
HOOK_PATH="$SCRIPT_DIR/hooks/zelda_hook.py"

# Check if settings.json exists
if [ -f "$SETTINGS_FILE" ]; then
    # Backup existing settings
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup.$(date +%s)"
    print_color "✅ Backed up existing settings.json" "$GREEN"
    
    # Update settings with our hooks using Python
    python3 << EOF
import json
import sys

settings_file = "$SETTINGS_FILE"
hook_path = "$HOOK_PATH"

try:
    with open(settings_file, 'r') as f:
        settings = json.load(f)
except:
    settings = {}

# Initialize hooks if not present
if 'hooks' not in settings:
    settings['hooks'] = {}

# Configure our hooks
hooks_config = {
    "PostToolUse": [
        {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": f"python3 {hook_path}"
                }
            ]
        }
    ],
    "UserPromptSubmit": [
        {
            "hooks": [
                {
                    "type": "command",
                    "command": f"python3 {hook_path}"
                }
            ]
        }
    ],
    "SessionStart": [
        {
            "hooks": [
                {
                    "type": "command",
                    "command": f"python3 {hook_path}"
                }
            ]
        }
    ],
    "Stop": [
        {
            "hooks": [
                {
                    "type": "command",
                    "command": f"python3 {hook_path}"
                }
            ]
        }
    ],
    "Notification": [
        {
            "hooks": [
                {
                    "type": "command",
                    "command": f"python3 {hook_path}"
                }
            ]
        }
    ]
}

# Merge hooks (don't overwrite other hooks)
for event, config in hooks_config.items():
    if event not in settings['hooks']:
        settings['hooks'][event] = config
    else:
        # Check if our hook is already there
        hook_exists = False
        for matcher_config in settings['hooks'][event]:
            if 'hooks' in matcher_config:
                for hook in matcher_config['hooks']:
                    if 'zelda_hook.py' in hook.get('command', ''):
                        hook_exists = True
                        break
        
        if not hook_exists:
            settings['hooks'][event].extend(config)

# Save updated settings
with open(settings_file, 'w') as f:
    json.dump(settings, f, indent=2)

print("✅ Hooks configured successfully")
EOF

else
    # Create new settings.json
    cat > "$SETTINGS_FILE" << EOF
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $HOOK_PATH"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 $HOOK_PATH"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 $HOOK_PATH"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 $HOOK_PATH"
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 $HOOK_PATH"
          }
        ]
      }
    ]
  }
}
EOF
    print_color "✅ Created new settings.json with Zelda hooks" "$GREEN"
fi

# ============================================================================
# 4. Verify Sound Files
# ============================================================================

print_color "\n[4/5] Verifying sound files..." "$YELLOW"

SOUND_COUNT=$(ls -1 sounds/*.wav 2>/dev/null | wc -l)
if [ "$SOUND_COUNT" -gt 0 ]; then
    print_color "✅ Found $SOUND_COUNT sound files" "$GREEN"
else
    print_color "⚠️  No sound files found. Please add WAV files to sounds/ directory" "$YELLOW"
fi

# ============================================================================
# 5. Test Installation
# ============================================================================

print_color "\n[5/5] Testing installation..." "$YELLOW"

# Test Python module
python3 -c "from zelda_core import get_manager; m = get_manager(); print('✅ Zelda core module working')" 2>/dev/null || {
    print_color "❌ Failed to load zelda_core module" "$RED"
    exit 1
}

# Test hook
echo '{"hook_event_name":"test"}' | python3 hooks/zelda_hook.py 2>/dev/null
print_color "✅ Hook handler working" "$GREEN"

# ============================================================================
# Installation Complete
# ============================================================================

print_color "\n╔════════════════════════════════════════════╗" "$GREEN"
print_color "║     🎉 INSTALLATION COMPLETE! 🎉           ║" "$GREEN"
print_color "╚════════════════════════════════════════════╝" "$GREEN"

print_color "\n📖 How to use Zelda Claude Code:" "$BLUE"
print_color "────────────────────────────────" "$BLUE"
echo ""
echo "In Claude Code, type these commands:"
echo ""
print_color "  @zelda stats         " "$YELLOW" && echo "View your coding statistics"
print_color "  @zelda achievements  " "$YELLOW" && echo "Check your achievements"
print_color "  @zelda combo        " "$YELLOW" && echo "See current combo streak"
print_color "  @zelda config       " "$YELLOW" && echo "View/change settings"
print_color "  @zelda help         " "$YELLOW" && echo "Show all commands"
echo ""
print_color "🎮 Features:" "$BLUE"
echo "  • Sounds play automatically as you code"
echo "  • Stats track in the background"
echo "  • Achievements unlock as you progress"
echo "  • Combos reward consecutive successes"
echo ""
print_color "🚀 Next Steps:" "$BLUE"
echo "  1. Restart Claude Code (exit and start again)"
echo "  2. Start coding and enjoy the sounds!"
echo "  3. Type @zelda stats to see your progress"
echo ""
print_color "⚠️  Important: You must restart Claude Code for hooks to take effect!" "$YELLOW"
echo ""
print_color "May the Triforce guide your code! 🗡️✨" "$GREEN"
echo ""