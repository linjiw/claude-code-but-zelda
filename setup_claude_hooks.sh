#!/bin/bash

echo "🎮 Zelda Sounds for Claude Code - Setup Assistant"
echo "================================================"
echo ""

# Get the current directory
ZELDA_DIR=$(pwd)

# Check if we're in the right directory
if [ ! -d "hooks" ] || [ ! -d "scripts" ] || [ ! -d "sounds" ]; then
    echo "❌ Error: Please run this script from the zelda_claude directory"
    exit 1
fi

echo "📁 Project directory: $ZELDA_DIR"
echo ""

# Find Claude Code config directory
echo "🔍 Looking for Claude Code configuration..."
CLAUDE_CONFIG_DIR="$HOME/.config/claude"

if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    echo "Creating Claude Code config directory..."
    mkdir -p "$CLAUDE_CONFIG_DIR"
fi

SETTINGS_FILE="$CLAUDE_CONFIG_DIR/settings.json"

# Create or update settings.json
if [ -f "$SETTINGS_FILE" ]; then
    echo "⚠️  Found existing settings.json"
    echo "   Backing up to settings.json.backup"
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"
fi

# Generate settings with correct paths
cat > "$SETTINGS_FILE" << EOF
{
  "hooks": {
    "user-prompt-submit-hook": "$ZELDA_DIR/hooks/on_success.sh",
    "assistant-message-done-hook": "$ZELDA_DIR/hooks/on_success.sh",
    "tool-result-hook": {
      "Bash": {
        "success": "$ZELDA_DIR/hooks/on_success.sh",
        "error": "$ZELDA_DIR/hooks/on_error.sh"
      },
      "TodoWrite": {
        "success": "$ZELDA_DIR/hooks/on_todo_complete.sh"
      },
      "Edit": {
        "success": "$ZELDA_DIR/hooks/on_success.sh",
        "error": "$ZELDA_DIR/hooks/on_error.sh"
      },
      "MultiEdit": {
        "success": "$ZELDA_DIR/hooks/on_success.sh",
        "error": "$ZELDA_DIR/hooks/on_error.sh"
      },
      "Write": {
        "success": "$ZELDA_DIR/hooks/on_success.sh"
      },
      "Read": {
        "success": "$ZELDA_DIR/hooks/on_success.sh"
      }
    }
  }
}
EOF

echo "✅ Updated Claude Code settings at: $SETTINGS_FILE"
echo ""

# Test the sounds
echo "🔊 Testing sound system..."
echo "   Playing success sound..."
python3 "$ZELDA_DIR/scripts/play_sound.py" success 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Sound system working!"
else
    echo "⚠️  Sound test failed - check your audio settings"
fi

echo ""
echo "🎮 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Download real Zelda sounds from legal sources"
echo "2. Replace the placeholder .wav files in sounds/"
echo "3. Start Claude Code and enjoy the sounds!"
echo ""
echo "Test individual sounds with:"
echo "  python3 scripts/play_sound.py success"
echo "  python3 scripts/play_sound.py error"
echo "  python3 scripts/play_sound.py todo_complete"