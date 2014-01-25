import pygame
import sys
from pygame.locals import *
import time
import game_logic

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption("Mind-four-letter-word")
    clock = pygame.time.Clock()
    game = game_logic.Game()
    game.load_level("level2")
    left, right, space = 0, 0, 0
    while 1:
        clock.tick(60)
        click = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
                elif event.key == K_RIGHT:
                    right = 1
                elif event.key == K_LEFT:
                    left = 1
                elif event.key == K_SPACE:
                    space = 1
            elif event.type == pygame.KEYUP:
                if event.key == K_RIGHT:
                    right = 0
                elif event.key == K_LEFT:
                    left = 0
                elif event.key == K_SPACE:
                    space = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = 1
            if event.type == pygame.QUIT:
                sys.exit(0)
        screen.fill((0,0,0))
        game.update(screen, left, right, space, click, pygame.mouse.get_pos())
        pygame.display.flip()

if __name__ == "__main__":
    main()
