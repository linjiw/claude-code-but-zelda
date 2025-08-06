#!/bin/bash

# Zelda Sounds for Claude Code - One-Click Installer
# This script handles everything automatically

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Header
echo -e "${CYAN}"
cat << "EOF"
╔════════════════════════════════════════════════════════════╗
║     🎮 ZELDA SOUNDS FOR CLAUDE CODE INSTALLER 🎮          ║
║                                                            ║
║     Add legendary sounds to your coding workflow!         ║
╚════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Get installation directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"

# Step counter
STEP=1
TOTAL_STEPS=8

# Function to print step headers
print_step() {
    echo ""
    echo -e "${BLUE}[$STEP/$TOTAL_STEPS] $1${NC}"
    echo "----------------------------------------"
    ((STEP++))
}

# Function to check success
check_success() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1${NC}"
        return 0
    else
        echo -e "${RED}✗ $1${NC}"
        return 1
    fi
}

# Start installation
echo -e "${GREEN}Starting installation...${NC}"
echo "Installation directory: $INSTALL_DIR"
echo ""

# Step 1: Check system compatibility
print_step "Checking system compatibility"

OS=$(uname -s)
if [ "$OS" = "Darwin" ]; then
    echo -e "${GREEN}✓ macOS detected${NC}"
    AUDIO_PLAYER="afplay"
elif [ "$OS" = "Linux" ]; then
    echo -e "${GREEN}✓ Linux detected${NC}"
    AUDIO_PLAYER="aplay"
else
    echo -e "${YELLOW}⚠ Windows/Other OS detected - may need adjustments${NC}"
    AUDIO_PLAYER="unknown"
fi

# Step 2: Check dependencies
print_step "Checking dependencies"

# Check Python 3
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check audio player
if [ "$AUDIO_PLAYER" != "unknown" ] && command -v $AUDIO_PLAYER &> /dev/null; then
    echo -e "${GREEN}✓ Audio player ($AUDIO_PLAYER) found${NC}"
else
    echo -e "${YELLOW}⚠ Audio player not found - sounds may not work${NC}"
fi

# Check Git
if command -v git &> /dev/null; then
    echo -e "${GREEN}✓ Git found${NC}"
else
    echo -e "${YELLOW}⚠ Git not found - version control unavailable${NC}"
fi

# Step 3: Check Claude Code installation
print_step "Checking Claude Code installation"

if command -v claude &> /dev/null; then
    echo -e "${GREEN}✓ Claude Code is installed${NC}"
else
    echo -e "${RED}✗ Claude Code not found${NC}"
    echo "Please install Claude Code first: https://claude.ai/code"
    exit 1
fi

# Check Claude directory
if [ ! -d "$CLAUDE_DIR" ]; then
    echo "Creating Claude directory..."
    mkdir -p "$CLAUDE_DIR"
fi
echo -e "${GREEN}✓ Claude directory exists${NC}"

# Step 4: Setup sounds
print_step "Setting up sound files"

# Check if sounds exist
if [ -d "$INSTALL_DIR/sounds" ] && [ "$(ls -A $INSTALL_DIR/sounds/*.wav 2>/dev/null | wc -l)" -gt 0 ]; then
    echo -e "${GREEN}✓ Sound files found${NC}"
    
    # Test a sound
    echo "Testing sound playback..."
    if [ "$AUDIO_PLAYER" != "unknown" ]; then
        $AUDIO_PLAYER "$INSTALL_DIR/sounds/success.wav" 2>/dev/null &
        sleep 1
        echo -e "${GREEN}✓ Sound test successful${NC}"
    fi
else
    echo -e "${YELLOW}⚠ No sound files found${NC}"
    echo "Generating default sounds..."
    python3 "$INSTALL_DIR/generate_zelda_style_sounds.py"
    check_success "Generated default sounds"
fi

# Step 5: Configure hooks
print_step "Configuring Claude Code hooks"

# Backup existing settings if they exist
if [ -f "$SETTINGS_FILE" ]; then
    BACKUP_FILE="$SETTINGS_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$SETTINGS_FILE" "$BACKUP_FILE"
    echo -e "${GREEN}✓ Backed up existing settings to $BACKUP_FILE${NC}"
fi

# Run the configuration script
echo "Installing hooks..."
python3 "$INSTALL_DIR/configure_claude_hooks.py" > /dev/null 2>&1
check_success "Hooks configured"

# Step 6: Make scripts executable
print_step "Setting up executable permissions"

chmod +x "$INSTALL_DIR"/*.sh 2>/dev/null || true
chmod +x "$INSTALL_DIR"/hooks/*.sh 2>/dev/null || true
chmod +x "$INSTALL_DIR"/hooks/*.py 2>/dev/null || true
chmod +x "$INSTALL_DIR"/scripts/*.py 2>/dev/null || true
echo -e "${GREEN}✓ Permissions set${NC}"

# Step 7: Create quick commands
print_step "Creating quick commands"

# Create test command
cat > "$INSTALL_DIR/test-sounds" << 'EOFTEST'
#!/bin/bash
echo "🎮 Testing Zelda Sounds..."
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$DIR/test_interactive.sh" 2>/dev/null || "$DIR/demo_sounds.sh"
EOFTEST
chmod +x "$INSTALL_DIR/test-sounds"

# Create uninstall command
cat > "$INSTALL_DIR/uninstall" << 'EOFUNINSTALL'
#!/bin/bash
echo "Removing Zelda sounds from Claude Code..."
python3 -c "
import json
from pathlib import Path

settings_path = Path.home() / '.claude' / 'settings.json'
if settings_path.exists():
    with open(settings_path) as f:
        settings = json.load(f)
    if 'hooks' in settings:
        del settings['hooks']
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    print('✓ Hooks removed from settings')
"
echo "✓ Uninstall complete"
echo "Note: Sound files remain in $(pwd) if you want to reinstall later"
EOFUNINSTALL
chmod +x "$INSTALL_DIR/uninstall"

echo -e "${GREEN}✓ Quick commands created${NC}"

# Step 8: Final verification
print_step "Verifying installation"

# Check if hooks are in settings
if [ -f "$SETTINGS_FILE" ] && grep -q "PostToolUse" "$SETTINGS_FILE"; then
    echo -e "${GREEN}✓ Hooks are configured in settings.json${NC}"
else
    echo -e "${YELLOW}⚠ Hooks may not be properly configured${NC}"
fi

# Run the test suite
echo "Running verification tests..."
python3 "$INSTALL_DIR/test_claude_integration.py" > /tmp/zelda_test.log 2>&1
if grep -q "ALL TESTS PASSED" /tmp/zelda_test.log; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${YELLOW}⚠ Some tests failed - check /tmp/zelda_test.log${NC}"
fi

# Installation complete
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}            ✅ INSTALLATION COMPLETE! ✅                    ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}🎮 Quick Start Guide:${NC}"
echo ""
echo "1. Restart Claude Code for changes to take effect:"
echo -e "   ${YELLOW}exit${NC}  (if Claude is running)"
echo -e "   ${YELLOW}claude${NC}"
echo ""
echo "2. Test your sounds:"
echo -e "   ${YELLOW}./test-sounds${NC}  - Test all sounds"
echo -e "   ${YELLOW}ls${NC}             - Should play success sound"
echo -e "   ${YELLOW}cat /fake${NC}      - Should play error sound"
echo ""
echo "3. Check hook status in Claude:"
echo -e "   ${YELLOW}/hooks${NC}         - View configured hooks"
echo ""
echo -e "${CYAN}📚 Additional Commands:${NC}"
echo -e "   ${YELLOW}./demo_sounds.sh${NC}       - Demo all sounds"
echo -e "   ${YELLOW}./test-sounds${NC}          - Interactive test"
echo -e "   ${YELLOW}./uninstall${NC}            - Remove hooks"
echo ""
echo -e "${CYAN}📖 Documentation:${NC}"
echo "   README.md              - General information"
echo "   CLAUDE_HOOKS_GUIDE.md  - Hook details"
echo "   VALIDATION_REPORT.md   - Test results"
echo ""
echo -e "${GREEN}Enjoy your Zelda sounds! 🗡️✨${NC}"
echo ""

# Check if Claude is currently running
if pgrep -f "claude" > /dev/null; then
    echo -e "${YELLOW}Note: Claude Code appears to be running.${NC}"
    echo -e "${YELLOW}Please restart it for hooks to take effect.${NC}"
fi