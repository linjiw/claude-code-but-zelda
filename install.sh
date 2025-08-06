#!/bin/bash

echo "🎮 Zelda Sounds for Claude Code - Installer"
echo "==========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the installation directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to check command availability
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is not installed"
        return 1
    fi
}

# Function to check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION is installed"
        return 0
    else
        echo -e "${RED}✗${NC} Python 3 is not installed"
        return 1
    fi
}

echo "📋 Checking requirements..."
echo "------------------------"

# Check for required tools
MISSING_DEPS=0

check_python || MISSING_DEPS=1

# Check for audio converter (ffmpeg or afconvert)
if command -v ffmpeg &> /dev/null; then
    echo -e "${GREEN}✓${NC} ffmpeg is installed"
elif command -v afconvert &> /dev/null; then
    echo -e "${GREEN}✓${NC} afconvert is installed (macOS)"
else
    echo -e "${YELLOW}⚠${NC}  No audio converter found (ffmpeg or afconvert recommended)"
fi

# Check for git
check_command git || echo -e "${YELLOW}⚠${NC}  Git not required but recommended"

if [ $MISSING_DEPS -eq 1 ]; then
    echo ""
    echo -e "${RED}Some dependencies are missing!${NC}"
    echo "Please install Python 3 to continue."
    exit 1
fi

echo ""
echo "🎵 Setting up sound files..."
echo "------------------------"

# Check if custom sounds exist
if [ -d "$INSTALL_DIR/user-customized-sound" ]; then
    echo "Found custom sound directory!"
    
    # Ask if user wants to convert custom sounds
    read -p "Convert custom MP3 files to WAV? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 "$INSTALL_DIR/setup_all_custom_sounds.py"
    fi
else
    echo "No custom sounds found. Using default 8-bit sounds."
    
    # Generate default sounds if they don't exist
    if [ ! -f "$INSTALL_DIR/sounds/success.wav" ]; then
        echo "Generating default 8-bit sounds..."
        python3 "$INSTALL_DIR/generate_zelda_style_sounds.py"
    fi
fi

echo ""
echo "⚙️  Configuring Claude Code..."
echo "------------------------"

# Create Claude config directory if it doesn't exist
CLAUDE_CONFIG_DIR="$HOME/.config/claude"
mkdir -p "$CLAUDE_CONFIG_DIR"

# Check if settings.json already exists
SETTINGS_FILE="$CLAUDE_CONFIG_DIR/settings.json"
if [ -f "$SETTINGS_FILE" ]; then
    echo -e "${YELLOW}⚠${NC}  Found existing Claude Code settings"
    echo "   Backing up to settings.json.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Generate settings.json with correct paths
cat > "$SETTINGS_FILE" << EOF
{
  "hooks": {
    "user-prompt-submit-hook": "$INSTALL_DIR/hooks/on_success.sh",
    "assistant-message-done-hook": "$INSTALL_DIR/hooks/on_success.sh",
    "tool-result-hook": {
      "Bash": {
        "success": "$INSTALL_DIR/hooks/on_success.sh",
        "error": "$INSTALL_DIR/hooks/on_error.sh"
      },
      "TodoWrite": {
        "success": "$INSTALL_DIR/hooks/on_todo_complete.sh"
      },
      "Edit": {
        "success": "$INSTALL_DIR/hooks/on_success.sh",
        "error": "$INSTALL_DIR/hooks/on_error.sh"
      },
      "MultiEdit": {
        "success": "$INSTALL_DIR/hooks/on_success.sh",
        "error": "$INSTALL_DIR/hooks/on_error.sh"
      },
      "Write": {
        "success": "$INSTALL_DIR/hooks/on_success.sh"
      },
      "Read": {
        "success": "$INSTALL_DIR/hooks/on_success.sh"
      },
      "Grep": {
        "success": "$INSTALL_DIR/hooks/on_success.sh"
      },
      "Task": {
        "success": "$INSTALL_DIR/hooks/on_success.sh"
      }
    }
  }
}
EOF

echo -e "${GREEN}✓${NC} Claude Code settings updated at: $SETTINGS_FILE"

echo ""
echo "🔊 Testing sound system..."
echo "------------------------"

# Test a sound
python3 "$INSTALL_DIR/scripts/play_sound.py" success 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Sound system is working!"
else
    echo -e "${YELLOW}⚠${NC}  Sound test failed - check your audio settings"
fi

echo ""
echo "📦 Creating command shortcuts..."
echo "------------------------"

# Create a command to test sounds
cat > "$INSTALL_DIR/zelda-test" << 'EOF'
#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$DIR/demo_sounds.sh"
EOF
chmod +x "$INSTALL_DIR/zelda-test"

# Create a command to update sounds
cat > "$INSTALL_DIR/zelda-update" << 'EOF'
#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$DIR/setup_all_custom_sounds.py"
EOF
chmod +x "$INSTALL_DIR/zelda-update"

echo -e "${GREEN}✓${NC} Created helper commands:"
echo "   • ./zelda-test    - Test all sounds"
echo "   • ./zelda-update  - Update custom sounds"

echo ""
echo "✨ Installation Complete!"
echo "========================"
echo ""
echo "🎮 Quick Start:"
echo "   1. Test sounds: ./zelda-test"
echo "   2. Start Claude Code and enjoy the sounds!"
echo ""
echo "📚 Documentation:"
echo "   • README.md - General information"
echo "   • SOUND_REFERENCE.md - Sound mappings"
echo ""
echo "🎵 To add custom sounds:"
echo "   1. Place MP3 files in user-customized-sound/"
echo "   2. Run: ./zelda-update"
echo ""
echo -e "${GREEN}Happy coding with Zelda sounds! 🗡️${NC}"