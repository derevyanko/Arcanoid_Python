import pygame
from objects import *

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
my_font = pygame.font.Font(None, 32)

window = Window((500, 500), True)

ballImg = pygame.image.load("image/ball.png")
ballImg = pygame.transform.scale(ballImg, (30, 30))
platformImg = pygame.image.load("image/platform.png")
platformImg = pygame.transform.scale(platformImg, (100, 30))

ball = Ball(235, 435, 30, 30, ballImg, [2, -3])
platform = Platform(200, 465, 90, 30, platformImg, 3)

blocks = []
window.windows['gameplay'].load_level('level' + '1', blocks)

while window.run:
	clock.tick(60)

	if window.status is 'gameplay':
		if window.windows['gameplay'].status is 'pauseGame':
			window.windows['gameplay'].gamePause(window, my_font, ball, platform, blocks)
		elif window.windows['gameplay'].status is 'winWindow':
			window.windows['gameplay'].winWindow(window, my_font, ball, platform, blocks)
		elif window.windows['gameplay'].status is 'gameOver':
			window.windows['gameplay'].gameOverWindow(window, my_font, ball, platform, blocks)
		else:
			window.windows['gameplay'].gamePlay(window, ball, platform, blocks, my_font)
	if window.status is 'startWindow':
		window.windows['startWindow'].draw(window, my_font)

pygame.quit()