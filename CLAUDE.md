# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Zelda sound effects integration for Claude Code that plays themed audio feedback during coding workflows. The system hooks into Claude Code events (tool execution, todo completion, test results) and plays appropriate Zelda sounds.

## Essential Commands

### Testing & Demo
```bash
./demo_sounds.sh                       # Test all sounds sequentially
python3 test_suite.py                  # Run comprehensive test suite
python3 scripts/play_sound.py success  # Test individual sound (success/error/todo_complete/etc)
./zelda-test                          # Quick test command
```

### Setup & Configuration
```bash
./install.sh                          # Main installer (checks dependencies, sets up sounds)
./setup_claude_hooks.sh               # Configure Claude Code hooks
python3 setup_claude_hooks_correct.py # Alternative Python-based setup
```

### Sound Management
```bash
./zelda-update                        # Update custom sounds from user-customized-sound/
python3 setup_all_custom_sounds.py   # Convert MP3s to WAV format
```

## Architecture

### Hook Integration Flow
1. Claude Code executes tool → PostToolUse hook triggers
2. Hook script receives JSON via stdin with tool details
3. Sound is determined based on tool type and status
4. Async playback via platform-specific command (afplay/aplay/PowerShell)

### Key Components
- **hooks/play_sound_hook.py**: Main hook that processes Claude Code JSON events
- **scripts/play_sound_async.py**: Cross-platform async sound player
- **sounds/**: WAV files mapped to events (success.wav, error.wav, todo_complete.wav, etc)

### Sound Event Mapping
- TodoWrite with completed status → todo_complete.wav
- Test/Bash tool success → success.wav or puzzle_solved.wav
- Tool errors → error.wav or damage.wav
- Notifications → warning.wav
- Session end → item_get.wav

## Development Notes

### Testing Approach
- No external test framework required
- Use `python3 test_suite.py` for comprehensive testing
- Individual sound tests via `python3 scripts/play_sound.py [sound_name]`

### Cross-Platform Support
- macOS: afplay
- Linux: aplay/paplay/ffplay/mpg123 (checks availability)
- Windows: PowerShell System.Media.SoundPlayer

### Important Files
- **claude_settings_example.json**: Example hooks configuration for ~/.claude/settings.json
- **sounds_backup/**: Original sounds preserved here when custom sounds are applied
- **user-customized-sound/**: MP3 files for custom sound replacements