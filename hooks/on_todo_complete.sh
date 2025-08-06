#!/bin/bash
# Hook for todo item completion
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/../scripts/play_sound.py" todo_complete