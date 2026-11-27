import pygame
import math
import asyncio
from array import array

pygame.mixer.init(44100, -16, 1)

async def play_note(pitch, duration=0.3):

    samples = array("h")

    for i in range(int(44100 * duration)):
        wave = math.sin(2 * math.pi * pitch * i / 44100)
        samples.append(int(8000 * wave))

    sound = pygame.mixer.Sound(buffer=samples)
    sound.play()

    await asyncio.sleep(duration + 0.05)


async def main():

    await play_note(440)
    await play_note(330)
    await play_note(523)


asyncio.run(main())