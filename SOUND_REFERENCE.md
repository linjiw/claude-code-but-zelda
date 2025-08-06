# 🎮 Zelda Sound Effects Reference

## Current Sound Configuration

All sounds are now using authentic Zelda: Tears of the Kingdom audio tracks!

### Sound Mappings

| Event Type | Sound File | Zelda Track | Duration | Usage |
|------------|------------|-------------|----------|--------|
| **Success** | success.wav | 243. Cooking Success | 0:05 | Commands succeed, builds pass |
| **Major Achievement** | item_get.wav | 741. GetLarge | 0:06 | Task completion, major success |
| **Error** | error.wav | 237. Cooking Fail | 0:05 | Command failures, errors |
| **Warning** | warning.wav | 206. Assassin Appear | 0:03 | Alerts, blocked hooks |
| **Progress** | rupee.wav | 744. GetSmall | 0:02 | Quick updates, small wins |
| **Todo Complete** | todo_complete.wav | 740. GetHeart | 0:06 | Todo items marked done |
| **Tests Pass** | puzzle_solved.wav | 743. GetMedium | 0:05 | All tests passing |
| **Tests Fail** | damage.wav | 363. Game Over | 0:06 | Test failures |
| **Discovery** | secret.wav | 938. Location Open Main | 0:07 | New findings, secrets |
| **Menu/Start** | menu_select.wav | 167. ZonauBlockMaster Bridge | 0:07 | Starting actions |
| **Default** | default.wav | 010. ReadRiddle | 0:02 | Fallback notification |

## Hook Assignments

### Tool Success Hooks
- **Bash success** → Cooking Success
- **Edit success** → Cooking Success  
- **Write success** → Cooking Success
- **Read success** → Cooking Success

### Tool Error Hooks
- **Bash error** → Cooking Fail
- **Edit error** → Cooking Fail

### Special Hooks
- **TodoWrite** → GetHeart (todo complete)
- **User prompt** → ZonauBlockMaster Bridge (menu)
- **Assistant done** → Cooking Success

## Testing

Test individual sounds:
```bash
python3 scripts/play_sound.py success
python3 scripts/play_sound.py error
python3 scripts/play_sound.py warning
python3 scripts/play_sound.py todo_complete
```

Test all sounds in sequence:
```bash
./demo_sounds.sh
```

## File Locations

- **Custom sounds**: `/user-customized-sound/` (MP3 originals)
- **Active sounds**: `/sounds/` (Converted WAV files)
- **Backup**: `/sounds_backup_original/` (Original 8-bit sounds)

## Notes

- All sounds are from Zelda: Tears of the Kingdom
- File sizes range from 400KB to 1.3MB
- Format: 44.1kHz WAV for compatibility
- macOS uses `afplay` for playback