# animation.py
# using pygame for animation practice

from pygame_library import *
import pygame

def main():
    win = make_win(800, 600, "My Game")

    # Circle properties
    x, y = 100, 100
    dx, dy = 5, 3
    radius = 25

    def update_circ():
        nonlocal x, y, dx, dy
        pygame.draw.circle(win, (255, 255, 255), (x, y), radius)

        x += dx
        y += dy

        if x - radius <= 0 or x + radius >= 800:
            dx = -dx
        if y - radius <= 0 or y + radius >= 600:
            dy = -dy

    # Rectangle properties
    rx, ry = 300, 300
    rdx, rdy = 4, -3
    rw, rh = 60, 40

    def update_rec():
        nonlocal rx, ry, rdx, rdy
        pygame.draw.rect(win, (0, 255, 0), (rx, ry, rw, rh))

        rx += rdx
        ry += rdy

        if rx <= 0 or rx + rw >= 800:
            rdx = -rdx
        if ry <= 0 or ry + rh >= 600:
            rdy = -rdy

    # Both animations run together
    game_loop(win, 60, update_circ, update_rec)
main()
