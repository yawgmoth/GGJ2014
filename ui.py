import pygame
import sys
from pygame.locals import *
import time
import game_logic

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()
    game = game_logic.Game()
    game.load_level("level0")
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
            if event.type == pygame.QUIT:
                sys.exit(0)
        screen.fill((0,0,0))
        game.update(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
