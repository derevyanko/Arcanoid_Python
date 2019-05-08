import pygame
from pygame.rect import Rect
from function import *
from objects import *

clock = pygame.time.Clock()

window = Window((500, 450), True)
pygame.display.set_caption("Arcanoid")

ballImg = pygame.image.load("image/ball.png")
ballImg = pygame.transform.scale(ballImg, (30, 30))
platformImg = pygame.image.load("image/platform.png")
platformImg = pygame.transform.scale(platformImg, (100, 30))

ball = Ball(235, 370, 30, 30, ballImg, [2, -2])
platform = Platform(200, 400, 100, 30, platformImg, 3)

blocks = []
for i in range(4):
	block = Block(30 + i * 110, 10, 100, 40)
	blocks.append(block)

for i in range(4):
	block = Block(30 + i * 110, 60, 100, 40)
	blocks.append(block)

while window.run:
	clock.tick(60)

	get_events(window, platform, ball)

	if window.windows[0].status is 'startGame':
		window.windows[0].gameplay(window, ball)

		collisionsBlocks(blocks, platform, ball)

	draw_all(window, ball, platform, blocks)

pygame.quit()