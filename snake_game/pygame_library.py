# pygame_library.py
# hutton personal library for pygame 

import pygame
pygame.init()

def make_win(width, height, caption):
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return win

def game_loop(win, fps, *update_funcs):
    """
    Helper function for main game loop. 
    win is pygame window, fps is frames per second, 
    update_func handles drawing and game logic
    """
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        win.fill((0,0,0))
        for func in update_funcs:
            func()
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()