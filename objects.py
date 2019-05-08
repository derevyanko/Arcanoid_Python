import pygame
from pygame.rect import Rect
from pygame import draw
# from functions import *

class Window():
	def __init__(self, size, run = True):
		self.run = run
		self.status = 'gameplay'
		self.windows = {'gameplay': GamePlayWindow(size), 'pause': PauseWindow(size)}
		self.caption = pygame.display.set_caption("Arcanoid")

class GamePlayWindow():
	def __init__(self, size):
		self.status = 'notStart'
		self.lastStatus = 'notStart'
		self.size = size
		self.screen = pygame.display.set_mode(size)

	def gameplay(self, window, ball, platform):
		self.get_eventsGamePlay(window, platform, ball)
		if window.windows['gameplay'].status is 'startGame':
			ball.move()
		if ball.rect.bottom > 450:
			window.run = False
			print('Game over!')
		if ball.rect.left < 0 or ball.rect.right > 500:
			ball.speed[0] *= -1
		if ball.rect.top < 0:
			ball.speed[1] *= -1

	def get_eventsGamePlay(self, window, platform, ball, events):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					if window.windows[window.status].status is 'pauseGame':
						if window.windows[window.status].lastStatus is 'startGame':
							window.windows[window.status].status = 'startGame'
						else:
							window.windows[window.status].status = 'notStart'
						window.windows[window.status].lastStatus = 'pauseGame'
						window.status = 'gameplay'
					elif window.windows[window.status].status is 'startGame' or 'notStart':
						window.windows[window.status].lastStatus = window.windows[window.status].status
						window.windows[window.status].status = 'pauseGame'
						window.status = 'pause'
				elif event.key == pygame.K_SPACE and window.windows[window.status].status is not 'pauseGame':
					if window.windows[window.status].status is not 'startGame':
						window.windows[window.status].status = 'startGame'
						window.windows[window.status].lastStatus = 'notStart'

		keys = pygame.key.get_pressed()
		if window.windows[window.status].status is not 'pauseGame':
			if keys[pygame.K_RIGHT] and platform.rect.right + platform.speed < 500:
				platform.rect.x += platform.speed
				if platform.rect.colliderect(ball.rect):
					platform.rect.x -= platform.speed
					objectCollision(platform, ball)
				if window.windows[window.status].status is 'notStart':
					ball.update(platform)
			if keys[pygame.K_LEFT] and platform.rect.left + platform.speed > 0:
				platform.rect.x -= platform.speed
				if platform.rect.colliderect(ball.rect):
					platform.rect.x += platform.speed
					objectCollision(platform, ball)
				if window.windows[window.status].status is 'notStart':
					ball.update(platform)

class PauseWindow():
	def __init__(self, size):
		self.status = 'no'
		self.size = size
		self.screen = pygame.display.set_mode(size)

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