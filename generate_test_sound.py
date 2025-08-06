#!/usr/bin/env python3
"""
Generate simple test beep sounds as placeholders
These will work for testing until real Zelda sounds are added
"""

import wave
import struct
import math

def generate_beep(filename, frequency=440, duration=0.2, sample_rate=44100):
    """Generate a simple beep sound file"""
    # Calculate number of samples
    num_samples = int(sample_rate * duration)
    
    # Generate sine wave samples
    samples = []
    for i in range(num_samples):
        t = float(i) / sample_rate
        value = int(32767 * math.sin(2 * math.pi * frequency * t))
        samples.append(struct.pack('<h', value))
    
    # Write WAV file
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)   # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(samples))
    
    print(f"Generated {filename} ({frequency}Hz, {duration}s)")

def main():
    """Generate different beep sounds for each event type"""
    sound_configs = {
        'sounds/success.wav': (523, 0.3),      # C5 - higher pitch for success
        'sounds/item_get.wav': (659, 0.4),     # E5 - triumphant
        'sounds/error.wav': (220, 0.3),        # A3 - lower pitch for error
        'sounds/warning.wav': (330, 0.2),      # E4 - medium pitch
        'sounds/menu_select.wav': (440, 0.1),  # A4 - quick beep
        'sounds/rupee.wav': (880, 0.1),        # A5 - very high and quick
        'sounds/puzzle_solved.wav': (698, 0.5), # F5 - long success
        'sounds/damage.wav': (185, 0.3),       # F#3 - low error
        'sounds/secret.wav': (784, 0.4),       # G5 - discovery sound
        'sounds/default.wav': (440, 0.2),      # A4 - standard beep
    }
    
    for filepath, (freq, dur) in sound_configs.items():
        generate_beep(filepath, freq, dur)
    
    print("\nTest sounds generated! These are placeholders.")
    print("Replace with real Zelda sounds for the authentic experience.")

if __name__ == "__main__":
    main()