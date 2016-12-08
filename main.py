import pygame
from gameplay import *

restartVar = True
pygame.init()
gameStart = True
x = Gameplay(32,30,20)
x.gameLoop()
pygame.quit()
quit()
