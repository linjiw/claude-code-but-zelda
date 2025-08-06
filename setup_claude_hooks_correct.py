#!/usr/bin/env python3
"""
Setup Claude Code hooks with the CORRECT configuration
Based on actual user feedback and Claude Code's expected format
"""

import json
import os
from pathlib import Path

def setup_hooks():
    """Configure Claude hooks in the correct location with correct format"""
    
    # Claude uses ~/.claude/settings.json (NOT ~/.config/claude/)
    claude_dir = Path.home() / '.claude'
    settings_path = claude_dir / 'settings.json'
    
    # Our hook scripts directory
    hooks_dir = Path(__file__).parent / 'hooks'
    
    # Create directory if it doesn't exist
    claude_dir.mkdir(exist_ok=True)
    
    # Read existing settings or create new
    if settings_path.exists():
        with open(settings_path) as f:
            settings = json.load(f)
        # Backup
        backup_path = settings_path.with_suffix('.json.backup_hooks')
        with open(backup_path, 'w') as f:
            json.dump(settings, f, indent=2)
        print(f"Backed up to: {backup_path}")
    else:
        settings = {}
    
    # Based on user feedback, hooks might need to be direct commands
    # Let's try both approaches: command-based and path-based
    
    # Approach 1: Direct command execution (like the PowerShell example)
    success_cmd = f'/bin/bash -c "python3 {hooks_dir}/on_success.py 2>/dev/null &"'
    error_cmd = f'/bin/bash -c "python3 {hooks_dir}/on_error.py 2>/dev/null &"'
    
    # Create simple Python scripts for direct execution
    success_script = hooks_dir / 'on_success.py'
    error_script = hooks_dir / 'on_error.py'
    
    # Write Python hook scripts
    success_script.write_text(f'''#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path
sound_path = Path("{hooks_dir.parent}") / "sounds" / "success.wav"
subprocess.Popen(["afplay", str(sound_path)], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL)
sys.exit(0)
''')
    
    error_script.write_text(f'''#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path
sound_path = Path("{hooks_dir.parent}") / "sounds" / "error.wav"
subprocess.Popen(["afplay", str(sound_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
sys.exit(0)
''')
    
    os.chmod(success_script, 0o755)
    os.chmod(error_script, 0o755)
    
    # Try different hook configuration formats
    # Format 1: Similar to user feedback structure
    settings['hooks'] = {
        'notification': {
            'command': f'python3 {success_script}'
        },
        'stop': {
            'command': f'python3 {error_script}'
        },
        # Format 2: Tool-based (might work)
        'onSuccess': str(hooks_dir / 'on_success.sh'),
        'onError': str(hooks_dir / 'on_error.sh'),
        # Format 3: Event-based
        'on-success': str(hooks_dir / 'on_success.sh'),
        'on-error': str(hooks_dir / 'on_error.sh')
    }
    
    # Also try adding as top-level settings
    settings['sound-on-success'] = True
    settings['sound-on-error'] = True
    settings['success-sound'] = str(hooks_dir.parent / 'sounds' / 'success.wav')
    settings['error-sound'] = str(hooks_dir.parent / 'sounds' / 'error.wav')
    
    # Write settings
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"✅ Updated Claude settings at: {settings_path}")
    print("\n📝 Created hook formats:")
    print("  1. notification/stop commands")
    print("  2. onSuccess/onError paths")
    print("  3. on-success/on-error paths")
    print("  4. Direct sound file paths")
    
    print("\n🔍 Testing hook directly:")
    os.system(f"python3 {success_script}")
    
    print("\n⚠️  IMPORTANT: Claude Code might need to be fully restarted")
    print("  1. Close ALL Claude Code windows/sessions")
    print("  2. Run: pkill -f claude")
    print("  3. Start fresh: claude")
    
    return settings_path

if __name__ == "__main__":
    settings_path = setup_hooks()
    
    print("\n📋 Next steps:")
    print("  1. Fully restart Claude Code")
    print("  2. Test with: ls (should hear success)")
    print("  3. Test with: cat /fake (should hear error)")
    print("\nIf still not working, Claude Code might not support custom hooks.")
    print("Check Claude Code documentation or support for hook configuration.")