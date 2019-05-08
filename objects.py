import pygame
from pygame.rect import Rect
from pygame import draw

class Window():
	def __init__(self, size, run = True):
		self.size = size
		self.run = run
		self.screen = pygame.display.set_mode(size)
		self.windows = [GamePlayWindow()]

class GamePlayWindow():
	def __init__(self):
		self.status = 'notStart'
		self.lastStatus = 'notStart'

	def gameplay(self, window, ball):
		if window.windows[0].status is 'startGame':
			ball.move()
		if ball.rect.bottom > 450:
			window.run = False
			print('Game over!')
		if ball.rect.left < 0 or ball.rect.right > 500:
			ball.speed[0] *= -1
		if ball.rect.top < 0:
			ball.speed[1] *= -1

class Ball():
	def __init__(self, x, y, width, height, image, speed):
		self.rect = Rect(x, y, width, height)
		self.speed = speed
		self.image = image

	def draw(self, window):
		window.blit(self.image, (self.rect.x, self.rect.y))

	def move(self):
		self.rect.x += self.speed[0]
		self.rect.y += self.speed[1]

	def unmove(self):
		self.rect.x -= self.speed[0]
		self.rect.y -= self.speed[1]

	def update(self, platform):
		self.rect.x = platform.rect.x + platform.rect.width / 2.0 - 15

class Block():
	def __init__(self, x, y, width, height):
		self.rect = Rect(x, y, width, height)
		self.color = (0, 255, 0)

	def draw(self, window):
		draw.rect(window, self.color, self.rect)

class Platform():
	def __init__(self, x, y, width, height, image, speed):
		self.rect = Rect(x, y, width, height)
		self.image = image
		self.speed = speed

	def draw(self, window):
		window.blit(self.image, (self.rect.x, self.rect.y))