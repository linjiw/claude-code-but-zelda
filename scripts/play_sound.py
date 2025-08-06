#!/usr/bin/env python3
"""
Cross-platform sound player for Claude Code hooks
Plays sound effects for different events
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def play_sound_mac(file_path):
    """Play sound on macOS using afplay"""
    subprocess.run(['afplay', file_path], check=False)

def play_sound_linux(file_path):
    """Play sound on Linux using various tools"""
    # Try different Linux audio players in order of preference
    players = ['aplay', 'paplay', 'ffplay', 'mpg123']
    for player in players:
        try:
            if player == 'ffplay':
                subprocess.run([player, '-nodisp', '-autoexit', file_path], 
                             check=False, stderr=subprocess.DEVNULL)
            else:
                subprocess.run([player, file_path], check=False)
            return
        except FileNotFoundError:
            continue
    print(f"No audio player found. Install aplay, paplay, or ffplay", file=sys.stderr)

def play_sound_windows(file_path):
    """Play sound on Windows using PowerShell"""
    ps_command = f'''
    Add-Type -TypeDefinition @"
    using System.Media;
    public class Sound {{
        public static void Play(string file) {{
            var player = new SoundPlayer(file);
            player.PlaySync();
        }}
    }}
"@
    [Sound]::Play("{file_path}")
    '''
    subprocess.run(['powershell', '-Command', ps_command], check=False)

def play_sound(sound_type):
    """Play a sound based on the event type"""
    # Get the base directory (parent of scripts folder)
    base_dir = Path(__file__).parent.parent
    sounds_dir = base_dir / 'sounds'
    
    # Map event types to sound files
    sound_map = {
        'success': 'success.wav',
        'complete': 'item_get.wav',
        'error': 'error.wav',
        'warning': 'warning.wav',
        'start': 'menu_select.wav',
        'progress': 'rupee.wav',
        'test_pass': 'puzzle_solved.wav',
        'test_fail': 'damage.wav',
        'todo_complete': 'secret.wav'
    }
    
    # Get the sound file
    sound_file = sound_map.get(sound_type, 'default.wav')
    file_path = sounds_dir / sound_file
    
    # Check if file exists
    if not file_path.exists():
        print(f"Sound file not found: {file_path}", file=sys.stderr)
        return
    
    # Play sound based on platform
    system = platform.system()
    try:
        if system == 'Darwin':  # macOS
            play_sound_mac(str(file_path))
        elif system == 'Linux':
            play_sound_linux(str(file_path))
        elif system == 'Windows':
            play_sound_windows(str(file_path))
        else:
            print(f"Unsupported platform: {system}", file=sys.stderr)
    except Exception as e:
        print(f"Error playing sound: {e}", file=sys.stderr)

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: play_sound.py <sound_type>")
        print("Sound types: success, complete, error, warning, start, progress, test_pass, test_fail, todo_complete")
        sys.exit(1)
    
    sound_type = sys.argv[1]
    play_sound(sound_type)

if __name__ == "__main__":
    main()