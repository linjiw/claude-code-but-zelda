# Zelda Sound Effects for Claude Code

Add legendary Zelda sound effects to your Claude Code workflow! 🎮

## Features

- **Success sounds**: Item get, puzzle solved
- **Error sounds**: Damage, game over  
- **Progress sounds**: Rupee collection, menu select
- **Todo completion**: Secret discovery sound
- **Test results**: Different sounds for pass/fail

## Setup Instructions

### 1. Sound Files Status ✅

Custom sounds have been integrated! The system now uses your personalized sound effects:

**Current Sound Mappings:**
- `success.wav` - Cooking Success sound
- `item_get.wav` - GetLarge sound  
- `error.wav` - Cooking Fail sound
- `warning.wav` - Original 8-bit warning
- `menu_select.wav` - Original 8-bit menu
- `rupee.wav` - GetSmall sound (progress)
- `puzzle_solved.wav` - GetMedium sound
- `damage.wav` - Game Over sound
- `secret.wav` - Location Open sound
- `todo_complete.wav` - GetHeart sound

**Backup Location:** Original sounds backed up to `sounds_backup/`

### 2. Configure Claude Code

Add hooks to your Claude Code settings:

```bash
# Find your Claude Code config directory
claude code config

# Edit the settings.json file
```

Copy the hooks configuration from `claude_settings_example.json` to your settings.json, updating the paths to match your installation location.

### 3. Test the Setup

Test individual sounds:
```bash
python3 scripts/play_sound.py success
python3 scripts/play_sound.py error
python3 scripts/play_sound.py todo_complete
```

## Sound Event Mapping

| Event | Sound | Description |
|-------|-------|-------------|
| Command success | Item get | Successful tool execution |
| Command error | Damage/error | Failed command |
| Todo complete | Secret found | Todo item marked complete |
| Test pass | Puzzle solved | All tests passing |
| Test fail | Damage | Test failures |
| Workflow start | Menu select | Beginning new task |

## Customization

Edit `scripts/play_sound.py` to:
- Change sound mappings
- Add new event types
- Adjust volume (platform-specific)

## Troubleshooting

### No sound on macOS
- Check System Preferences > Sound
- Ensure `afplay` is available: `which afplay`

### No sound on Linux
- Install audio player: `sudo apt-get install alsa-utils`
- Or: `sudo apt-get install pulseaudio-utils`

### No sound on Windows
- PowerShell execution policy may block scripts
- Run: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Platform Support

- ✅ macOS (afplay)
- ✅ Linux (aplay/paplay/ffplay)
- ✅ Windows (PowerShell/System.Media)

## Legal Note

Only use sound effects you have the right to use:
- Public domain sounds
- Creative Commons licensed
- Self-created or generated sounds
- Sounds from legal repositories

## Contributing

Feel free to add more event types or improve the sound player!