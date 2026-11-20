import pygame

WIDTH, HEIGHT = 660, 400
X = [120, 330, 540]
Y = 314
COLORS = [(242, 128, 114), (251, 191, 83), (96, 190, 163), (113, 153, 232), (172, 130, 222)]


def run_game(moves, disks=3):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower of Hanoi")
    font = pygame.font.SysFont(None, 27)
    small = pygame.font.SysFont(None, 23)
    towers = [list(range(disks, 0, -1)), [], []]
    step = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    towers = [list(range(disks, 0, -1)), [], []]
                    step = 0
                if event.key == pygame.K_SPACE and step < len(moves):
                    source, target = moves[step]
                    if source not in "ABC" or target not in "ABC":
                        print("Move must use A, B, or C")
                        continue
                    s, t = "ABC".index(source), "ABC".index(target)
                    if not towers[s]:
                        print("Invalid move: source is empty")
                        continue
                    disk = towers[s][-1]
                    if towers[t] and towers[t][-1] < disk:
                        print("Invalid move: big disk cannot sit on a small disk")
                        continue
                    towers[t].append(towers[s].pop())
                    step += 1
        screen.fill((246, 249, 253))
        title = font.render("Tower of Hanoi", True, (30, 51, 74))
        screen.blit(title, (245, 24))
        hint = small.render("SPACE = Next Move     R = Reset", True, (65, 84, 104))
        screen.blit(hint, (207, 62))
        status = small.render(f"Move {step} / {len(moves)}", True, (38, 82, 119))
        screen.blit(status, (283, 94))
        pygame.draw.rect(screen, (57, 74, 94), (45, Y, 570, 11))
        for i, x in enumerate(X):
            pygame.draw.rect(screen, (105, 121, 145), (x - 6, 144, 12, Y - 144))
            label = font.render("ABC"[i], True, (30, 51, 74))
            screen.blit(label, label.get_rect(center=(x, 351)))
            for level, disk in enumerate(towers[i]):
                width = 52 + disk * 34
                rect = pygame.Rect(x - width // 2, Y - 31 * (level + 1), width, 28)
                pygame.draw.rect(screen, COLORS[(disk - 1) % len(COLORS)], rect, border_radius=6)
                number = small.render(str(disk), True, (30, 51, 74))
                screen.blit(number, number.get_rect(center=rect.center))
        if step == len(moves) and towers[2] == list(range(disks, 0, -1)):
            won = font.render("SOLVED!", True, (26, 120, 71))
            screen.blit(won, (495, 24))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()



# a list to store the moves made by the user
moves = []

# create a function name: hanoi(n, start, end, helper))
# n: number of disks
# start: the starting tower (A, B, or C)
# end: the ending tower (A, B, or C)
# helper: the helper tower (A, B, or C)

    # base case: if there is only one disk, move it from start to end

        # append the move to the moves list

        # return from the function


    # recursive case 1

    # recursive case 2



