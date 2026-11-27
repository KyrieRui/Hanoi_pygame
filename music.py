
import pygame
import asyncio
import random
import math
from array import array

# =====================================
# STUDENT CODE
# =====================================

def generate_pitches(amount):

    tune = []

    for i in range(amount):

        pitch = random.randint(2, 8) * 100

        tune.append(pitch)

    return tune


def find_minimum(tune, start):

    lowest_index = start

    for i in range(start + 1, len(tune)):

        if tune[i] < tune[lowest_index]:

            lowest_index = i

    return lowest_index


def swap_notes(tune, a, b):

    temp = tune[a]

    tune[a] = tune[b]

    tune[b] = temp


def selection_sort(tune, start=0):

    for position in range(start, len(tune) - 1):

        lowest_index = find_minimum(tune, position)

        swap_notes(tune, position, lowest_index)


# =====================================
# TEACHER CODE
# =====================================

pygame.init()

audio_ready = False

try:
    pygame.mixer.init(44100, -16, 1)

    audio_ready = pygame.mixer.get_init() is not None

except pygame.error:
    print("Audio unavailable. Visual mode is still working.")


screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Dancing Notes")

font = pygame.font.Font(None, 25)
title_font = pygame.font.Font(None, 38)

BACKGROUND = (20, 32, 51)
BLUE = (96, 165, 250)
GREEN = (52, 211, 153)
YELLOW = (250, 204, 21)
PURPLE = (192, 132, 252)
WHITE = (255, 255, 255)

tune = [440, 294, 523, 330, 392, 262, 494, 349]

start = 0
minimum = -1
active = -1

status = "Ready"

buttons = {}

labels = [
    "Generate",
    "Find Min",
    "Swap",
    "Sort All",
    "Play"
]

for i in range(len(labels)):

    buttons[labels[i]] = pygame.Rect(
        20 + i * 155, 440, 145, 40
    )


def draw_text(text, x, y, colour=WHITE):

    image = font.render(str(text), True, colour)

    screen.blit(image, (x, y))


def draw_screen():

    screen.fill(BACKGROUND)

    title = title_font.render(
        "Dancing Notes", True, WHITE
    )

    screen.blit(title, (20, 15))

    draw_text(status, 20, 60)

    if len(tune) > 0:

        spacing = 740 / len(tune)

        for i in range(len(tune)):

            pitch = tune[i]

            x = int(30 + i * spacing)

            height = int(pitch * 0.35)

            y = 390 - height

            colour = BLUE

            if i < start:
                colour = GREEN

            if i == minimum:
                colour = YELLOW

            if i == active:
                colour = PURPLE

            pygame.draw.rect(
                screen,
                colour,
                (x, y, int(spacing - 12), height),
                border_radius=5
            )

            draw_text(pitch, x + 8, y - 23)

            draw_text(i, x + 15, 400)

    for name in buttons:

        rect = buttons[name]

        pygame.draw.rect(
            screen,
            (51, 65, 85),
            rect,
            border_radius=5
        )

        text = font.render(name, True, WHITE)

        screen.blit(
            text,
            text.get_rect(center=rect.center)
        )

    pygame.display.flip()


async def play_note(pitch, duration=0.25):

    if audio_ready:

        rate, audio_format, channels = pygame.mixer.get_init()

        samples = array("h")

        total = int(rate * duration)

        for i in range(total):

            wave = math.sin(
                2 * math.pi * pitch * i / rate
            )

            fade = min(
                1,
                i / max(1, rate * 0.005),
                (total - 1 - i) / max(1, rate * 0.005)
            )

            sample = int(6000 * wave * fade)

            for channel in range(channels):
                samples.append(sample)

        try:
            sound = pygame.mixer.Sound(
                buffer=samples.tobytes()
            )

            sound.play()

        except pygame.error:
            print("Could not play this note.")

    await asyncio.sleep(duration + 0.05)


async def main():

    global tune
    global start
    global minimum
    global active
    global status

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse = event.pos

                if buttons["Generate"].collidepoint(mouse):

                    tune = generate_pitches(8)

                    start = 0
                    minimum = -1

                    status = "Generated random pitches"

                elif buttons["Find Min"].collidepoint(mouse):

                    if start < len(tune) - 1:

                        minimum = find_minimum(tune, start)

                        status = (
                            "Minimum: "
                            + str(tune[minimum])
                            + " at index "
                            + str(minimum)
                        )

                elif buttons["Swap"].collidepoint(mouse):

                    if minimum >= 0:

                        swap_notes(tune, start, minimum)

                        start += 1
                        minimum = -1

                        if start >= len(tune) - 1:

                            start = len(tune)

                            status = "Sorting complete"

                        else:

                            status = "One round complete"

                elif buttons["Sort All"].collidepoint(mouse):

                    selection_sort(tune, start)

                    start = len(tune)
                    minimum = -1

                    status = "Selection Sort complete"

                elif buttons["Play"].collidepoint(mouse):

                    status = "Playing melody"

                    for i in range(len(tune)):

                        active = i

                        draw_screen()

                        await play_note(tune[i])

                    active = -1

                    status = "Playback complete"

        draw_screen()

        await asyncio.sleep(0.016)

    pygame.quit()


asyncio.run(main())
