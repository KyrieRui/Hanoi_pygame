import pygame
import math
import array
import random

pygame.mixer.init(frequency=44100, size=-16, channels=1)

def play_note(midi_note, duration=0.35):
    freq = 440 * (2 ** ((midi_note - 69) / 12))  # MIDI to Hz
    sample_rate = 44100
    frames = int(sample_rate * duration)
    
    wave = array.array('h', [
        int(32767 * math.sin(2 * math.pi * freq * i / sample_rate))
        for i in range(frames)
    ])
    
    sound = pygame.mixer.Sound(buffer=wave)
    sound.play()
    pygame.time.wait(int(duration * 1000))

# a random Melody
tune = [random.randint(48, 72) for _ in range(6)]
print("🎵 random Melody:", tune)
for note in tune:
    play_note(note, 0.3)

pygame.time.wait(600)

# sort
for j in range(len(tune) - 1):
    min_idx = j
    for i in range(j + 1, len(tune)):
        if tune[i] < tune[min_idx]:
            min_idx = i
    tune[min_idx], tune[j] = tune[j], tune[min_idx]
    print(f"Number{j+1} Round: {tune}")

print("🎼 Melody after sort:", tune)
for note in tune:
    play_note(note, 0.4)