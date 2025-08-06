#!/bin/bash
# Hook for passing tests
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/../scripts/play_sound_async.py" test_pass &