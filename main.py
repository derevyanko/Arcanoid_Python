import pygame
from pygame.rect import Rect
from functions import *
from objects import *

clock = pygame.time.Clock()

window = Window((500, 450), True)

ballImg = pygame.image.load("image/ball.png")
ballImg = pygame.transform.scale(ballImg, (30, 30))
platformImg = pygame.image.load("image/platform.png")
platformImg = pygame.transform.scale(platformImg, (100, 30))

ball = Ball(235, 370, 30, 30, ballImg, [2, -2])
platform = Platform(200, 400, 100, 30, platformImg, 3)

blocks = load_level('level' + '1')

while window.run:
	clock.tick(60)

	get_events(window, platform, ball)

	window.windows[window.status].gameplay(window, ball, platform, pygame.event.get())

	collisionsBlocks(blocks, platform, ball)

	draw_all(window, ball, platform, blocks)

pygame.quit()