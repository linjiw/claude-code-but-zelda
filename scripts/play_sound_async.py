#!/usr/bin/env python3
"""
Asynchronous sound player for Claude Code hooks
Plays sounds without blocking to maintain performance
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def play_sound_mac(file_path):
    """Play sound on macOS using afplay (non-blocking)"""
    subprocess.Popen(['afplay', file_path], 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL)

def play_sound_linux(file_path):
    """Play sound on Linux using various tools (non-blocking)"""
    players = ['aplay', 'paplay', 'ffplay', 'mpg123']
    for player in players:
        try:
            if player == 'ffplay':
                subprocess.Popen([player, '-nodisp', '-autoexit', file_path], 
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen([player, file_path],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            return
        except FileNotFoundError:
            continue

def play_sound_windows(file_path):
    """Play sound on Windows using PowerShell (non-blocking)"""
    ps_command = f'''
    Start-Job -ScriptBlock {{
        Add-Type -TypeDefinition @"
        using System.Media;
        public class Sound {{
            public static void Play(string file) {{
                var player = new SoundPlayer(file);
                player.Play();
            }}
        }}
"@
        [Sound]::Play("{file_path}")
    }}
    '''
    subprocess.Popen(['powershell', '-Command', ps_command],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)

def play_sound(sound_type):
    """Play a sound based on the event type (non-blocking)"""
    # Get the base directory
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
        # Silently fail - don't block operations
        return
    
    # Play sound based on platform (non-blocking)
    system = platform.system()
    try:
        if system == 'Darwin':  # macOS
            play_sound_mac(str(file_path))
        elif system == 'Linux':
            play_sound_linux(str(file_path))
        elif system == 'Windows':
            play_sound_windows(str(file_path))
    except Exception:
        # Silently fail - don't interrupt workflow
        pass

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        sys.exit(0)  # Exit silently if no argument
    
    sound_type = sys.argv[1]
    play_sound(sound_type)
    
    # Exit immediately after starting playback
    sys.exit(0)

if __name__ == "__main__":
    main()