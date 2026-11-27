import pygame, asyncio, math, random
from array import array

pygame.init()
pygame.mixer.init(44100, -16, 1)
audio_ready = pygame.mixer.get_init() is not None

async def play_note(pitch, duration=0.3):
    if audio_ready:
        rate, _, channels = pygame.mixer.get_init()
        samples = array("h")
        total = int(rate * duration)
        for i in range(total):
            wave = math.sin(2 * math.pi * pitch * i / rate)
            fade = min(1, i / max(1, rate * 0.005), (total-1-i) / max(1, rate * 0.005))
            sample = int(6000 * wave * fade)
            for _ in range(channels): samples.append(sample)
        pygame.mixer.Sound(buffer=samples.tobytes()).play()
    await asyncio.sleep(duration + 0.05)

def generate_pitches(amount):
    tune = []
    for _ in range(amount):
        tune.append(random.randint(2, 8) * 100)
    return tune

# TODO: Implement the following functions
# find_minimum(tune, start): Find the index of the minimum pitch in the tune starting from 'start'.
def find_minimum(tune, start): ...

# swap_notes(tune, a, b): Swap the notes at indices 'a' and 'b' in the tune.
def swap_notes(tune, a, b): ...

# selection_sort(tune, start=0): Sort the tune in ascending order using the selection sort algorithm.
def selection_sort(tune, start=0): ...

async def main():
    tune = generate_pitches(8)
    print("随机旋律:", tune)
    for pitch in tune: await play_note(pitch)

    await asyncio.sleep(0.6)
    selection_sort(tune)

    print("排序后:", tune)
    for pitch in tune: await play_note(pitch)
    pygame.quit()

asyncio.run(main())