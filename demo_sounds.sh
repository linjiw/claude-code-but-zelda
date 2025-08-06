#!/bin/bash

echo "🎮 Zelda Sound Effects Demo"
echo "==========================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Array of sound types and descriptions
declare -a sounds=(
    "menu_select:Starting a new quest..."
    "success:Command executed successfully!"
    "item_get:Achievement unlocked!"
    "rupee:Making progress..."
    "todo_complete:Secret discovered!"
    "puzzle_solved:All tests passed!"
    "warning:Warning - check this out"
    "error:Uh oh, something went wrong"
    "damage:Test failed"
)

echo "Playing all available sounds..."
echo ""

for sound_info in "${sounds[@]}"; do
    IFS=':' read -r sound_type description <<< "$sound_info"
    echo "🔊 $description"
    python3 "$SCRIPT_DIR/scripts/play_sound.py" "$sound_type"
    sleep 1
done

echo ""
echo "Demo complete! 🏆"
echo ""
echo "To use with Claude Code:"
echo "1. Run ./setup_claude_hooks.sh"
echo "2. Replace sounds with real Zelda audio files"
echo "3. Start coding with Claude Code!"