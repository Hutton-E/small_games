# pygame practice

import pygame, os
os.chdir("/Users/huttonedney/Desktop/graphics interest")
pygame.init()
width, height = 500, 500
def main():
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My Game")
    image = pygame.image.load("sunny.png")
    image = pygame.transform.scale(image, (width, height))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill((255, 255, 255)) 
        win.blit(image, (0,0))
        pygame.display.update()

    pygame.quit()

main()
