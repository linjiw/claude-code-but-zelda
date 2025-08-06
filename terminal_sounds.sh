#!/bin/bash
# Add this to your ~/.zshrc or ~/.bashrc for terminal-level sounds

# Sound files location
SOUND_DIR="$HOME/Downloads/zelda_claude/sounds"

# Function to play success sound after commands
play_command_sound() {
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        # Success sound
        afplay "$SOUND_DIR/success.wav" 2>/dev/null &
    else
        # Error sound
        afplay "$SOUND_DIR/error.wav" 2>/dev/null &
    fi
}

# Add to prompt command (ZSH)
if [ -n "$ZSH_VERSION" ]; then
    precmd_functions+=(play_command_sound)
fi

# Add to prompt command (Bash)
if [ -n "$BASH_VERSION" ]; then
    PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND;}play_command_sound"
fi

echo "✅ Terminal sounds configured!"
echo "Now every command in your terminal will play Zelda sounds!"
echo ""
echo "To activate:"
echo "  source ~/.zshrc    # For ZSH"
echo "  source ~/.bashrc   # For Bash"