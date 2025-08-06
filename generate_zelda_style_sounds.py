#!/usr/bin/env python3
"""
Generate Zelda-inspired (but original) 8-bit style sounds
These are legally safe alternatives that evoke the same feeling
"""

import wave
import struct
import math
import random

def generate_adsr_envelope(num_samples, attack=0.01, decay=0.1, sustain=0.7, release=0.19):
    """Generate ADSR envelope for more realistic sound"""
    envelope = []
    attack_samples = int(num_samples * attack)
    decay_samples = int(num_samples * decay)
    sustain_samples = int(num_samples * sustain)
    release_samples = int(num_samples * release)
    
    # Attack
    for i in range(attack_samples):
        envelope.append(i / attack_samples)
    
    # Decay
    for i in range(decay_samples):
        envelope.append(1.0 - (i / decay_samples) * 0.3)
    
    # Sustain
    for i in range(sustain_samples):
        envelope.append(0.7)
    
    # Release
    for i in range(release_samples):
        envelope.append(0.7 * (1.0 - i / release_samples))
    
    return envelope

def generate_square_wave(frequency, duration, sample_rate=44100):
    """Generate 8-bit style square wave"""
    num_samples = int(sample_rate * duration)
    samples = []
    envelope = generate_adsr_envelope(num_samples)
    
    for i in range(num_samples):
        t = float(i) / sample_rate
        # Square wave
        value = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
        # Apply envelope
        value = value * envelope[min(i, len(envelope)-1)]
        samples.append(int(32767 * value * 0.3))  # Reduce volume
    
    return samples

def generate_arpeggio(notes, note_duration, sample_rate=44100):
    """Generate rapid note sequence (arpeggio) like classic Zelda sounds"""
    samples = []
    for note in notes:
        note_samples = generate_square_wave(note, note_duration, sample_rate)
        samples.extend(note_samples)
    return samples

def save_wav(filename, samples, sample_rate=44100):
    """Save samples to WAV file"""
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for sample in samples:
            wav_file.writeframes(struct.pack('<h', sample))

def main():
    print("🎮 Generating Zelda-inspired 8-bit sounds...")
    print("=" * 50)
    
    # Success/Item Get - Rising arpeggio
    print("✨ Creating 'item_get.wav' - Rising triumphant arpeggio")
    notes = [523, 659, 784, 1047]  # C5, E5, G5, C6
    samples = generate_arpeggio(notes, 0.1)
    save_wav('sounds/item_get.wav', samples)
    
    # Secret Found - Classic two-note discovery
    print("🗝️  Creating 'secret.wav' - Discovery sound")
    notes = [392, 494, 587, 784]  # G4, B4, D5, G5
    samples = generate_arpeggio(notes, 0.08)
    save_wav('sounds/secret.wav', samples)
    
    # Success - Quick victory fanfare
    print("✅ Creating 'success.wav' - Quick success sound")
    notes = [523, 659, 523, 784]  # C5, E5, C5, G5
    samples = generate_arpeggio(notes, 0.06)
    save_wav('sounds/success.wav', samples)
    
    # Error/Damage - Descending notes
    print("❌ Creating 'error.wav' - Error/damage sound")
    notes = [440, 349, 294]  # A4, F4, D4
    samples = generate_arpeggio(notes, 0.1)
    save_wav('sounds/error.wav', samples)
    save_wav('sounds/damage.wav', samples)
    
    # Rupee/Progress - Quick high ping
    print("💎 Creating 'rupee.wav' - Quick collection sound")
    samples = generate_square_wave(880, 0.1)  # A5
    save_wav('sounds/rupee.wav', samples)
    
    # Menu Select - Simple beep
    print("📝 Creating 'menu_select.wav' - Menu navigation")
    samples = generate_square_wave(587, 0.08)  # D5
    save_wav('sounds/menu_select.wav', samples)
    
    # Puzzle Solved - Victory sequence
    print("🏆 Creating 'puzzle_solved.wav' - Puzzle completion")
    notes = [392, 494, 587, 784, 987]  # G4, B4, D5, G5, B5
    samples = generate_arpeggio(notes, 0.08)
    save_wav('sounds/puzzle_solved.wav', samples)
    
    # Warning - Alternating tones
    print("⚠️  Creating 'warning.wav' - Warning alert")
    warning_samples = []
    for _ in range(3):
        warning_samples.extend(generate_square_wave(440, 0.1))
        warning_samples.extend([0] * 2000)  # Silence
    save_wav('sounds/warning.wav', warning_samples)
    
    # Default beep
    print("🔊 Creating 'default.wav' - Default notification")
    samples = generate_square_wave(440, 0.2)
    save_wav('sounds/default.wav', samples)
    
    print("\n✅ All sounds generated successfully!")
    print("\nThese are original 8-bit style sounds inspired by classic games.")
    print("They're legally safe to use and evoke that retro gaming feeling!")
    print("\nTest them with: ./demo_sounds.sh")

if __name__ == "__main__":
    main()