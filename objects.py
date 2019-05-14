import pygame
from pygame.rect import Rect
from pygame import draw
from math import fabs

class Window():
	def __init__(self, size, run = True):
		self.run = run
		self.status = 'startWindow'
		self.windows = {'gameplay': GamePlayWindow(size), 'startWindow': StartWindow(size)}
		self.caption = pygame.display.set_caption("Arcanoid")

class Text():
	def __init__(self, text, coords):
		self.text = text
		self.coords = coords

class Texts():
	def __init__(self, texts):
		self.texts = texts
		self.pointer = 0

class StartWindow():
	def __init__(self, size):
		self.size = size
		self.texts = Texts([Text('Уровни', (215, 200)), Text('Результаты', (190, 250)), 
			Text('Выход', (215, 300))])
		self.screen = pygame.display.set_mode(size)

	def draw(self, window, text_render):
		self.get_events(window)
		window.windows[window.status].screen.fill((0, 0, 0))
		first_coords = self.texts.texts[0].coords
		second_coords = self.texts.texts[1].coords
		third_coords = self.texts.texts[2].coords
		if self.texts.pointer == 0:
			first_text = text_render.render(self.texts.texts[0].text, 5, (0, 0, 0))
			second_text = text_render.render(self.texts.texts[1].text, 5, (255, 255, 255))
			third_text = text_render.render(self.texts.texts[2].text, 5, (255, 255, 255))
			rect_text = first_text.get_rect()

			surf = pygame.Surface((rect_text.width, rect_text.height))
			surf.fill((255, 255, 255))

			window.windows[window.status].screen.blit(surf, first_coords)
			window.windows[window.status].screen.blit(first_text, first_coords)
			window.windows[window.status].screen.blit(second_text, second_coords)
			window.windows[window.status].screen.blit(third_text, third_coords)
		elif self.texts.pointer == 1:
			first_text = text_render.render(self.texts.texts[0].text, 5, (255, 255, 255))
			second_text = text_render.render(self.texts.texts[1].text, 5, (0, 0, 0))
			third_text = text_render.render(self.texts.texts[2].text, 5, (255, 255, 255))
			rect_text = second_text.get_rect()

			surf = pygame.Surface((rect_text.width, rect_text.height))
			surf.fill((255, 255, 255))

			window.windows[window.status].screen.blit(surf, second_coords)
			window.windows[window.status].screen.blit(first_text, first_coords)
			window.windows[window.status].screen.blit(second_text, second_coords)
			window.windows[window.status].screen.blit(third_text, third_coords)
		else:
			first_text = text_render.render(self.texts.texts[0].text, 5, (255, 255, 255))
			second_text = text_render.render(self.texts.texts[1].text, 5, (255, 255, 255))
			third_text = text_render.render(self.texts.texts[2].text, 5, (0, 0, 0))
			rect_text = third_text.get_rect()

			surf = pygame.Surface((rect_text.width, rect_text.height))
			surf.fill((255, 255, 255))

			window.windows[window.status].screen.blit(surf, third_coords)
			window.windows[window.status].screen.blit(first_text, first_coords)
			window.windows[window.status].screen.blit(second_text, second_coords)
			window.windows[window.status].screen.blit(third_text, third_coords)

		pygame.display.update()

	def get_events(self, window):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					if event.key == pygame.K_UP:
						self.texts.pointer -= 1
						if self.texts.pointer < 0:
							self.texts.pointer = 2
					else:
						self.texts.pointer += 1
					self.texts.pointer %= 3
				elif event.key == pygame.K_RETURN:
					if self.texts.pointer == 0:
						window.status = 'gameplay'
					elif self.texts.pointer == 1:
						pass
					else:
						window.run = False

class LevelsWindow():
	def __init__(self, size):
		self.size = size()
		self.screen = pygame.display.set_mode(size)

class GamePlayWindow():
	def __init__(self, size):
		self.status = 'notStart'
		self.lastStatus = 'notStart'
		self.size = size
		self.surf = pygame.Surface((500, 50))
		self.surfSize = (500, 50)
		self.surfX = 0
		self.surfY = 0
		self.score = 0
		self.surfTexts = [Text('Очки: ', (130, 15)), Text('Время: ', (250, 15))]
		self.texts = {'pauseGame': Texts([Text('Продолжить', (190, 200)), Text('Начать заново', (180, 250)), Text('Выход в меню', (180, 300))]), 
			'winWindow': Texts([Text('Начать заново', (180, 200)), Text('Выход в меню', (180, 250))]), 
			'gameOver': Texts([Text('Начать заново', (180, 200)), Text('Выход в меню', (180, 250))])}
		self.screen = pygame.display.set_mode(size)

	def gamePlay(self, window, ball, platform, blocks, text_render):
		self.get_eventsGamePlay(window, platform, ball)
		if window.windows['gameplay'].status is 'startGame':
			ball.move()
		if ball.rect.bottom > self.size[1]:
			self.score = 0
			self.load_level('level' + '1', blocks)
			self.status = 'gameOver'
			print('Game over!')
		if ball.rect.left < 0 or ball.rect.right > self.size[0]:
			ball.speed[0] *= -1
		if ball.rect.top < 0 + self.surfSize[1]:
			ball.speed[1] *= -1
		ball.collisionsBlocks(blocks, platform, window)
		if len(blocks) is 0:
			window.windows[window.status].status = 'winWindow'
		window.windows['gameplay'].drawGame(window, ball, platform, blocks, text_render)

	def gamePause(self, window, text_render, ball, platform, blocks):
		self.get_eventsPauseGame(window, ball, platform, blocks)
		window.windows['gameplay'].drawPause(window, text_render)

	def winWindow(self, window, text_render, ball, platform, blocks):
		self.get_eventsWinWindow(window, ball, platform, blocks)
		window.windows['gameplay'].drawWinWindow(window, text_render)

	def gameOverWindow(self, window, text_render, ball, platform, blocks):
		self.get_eventsGameOverWindow(window, ball, platform, blocks)
		window.windows['gameplay'].drawGameOverWindow(window, text_render)

	def drawGameOverWindow(self, window, text_render):
		window.windows[window.status].screen.fill((0, 0, 0))
		first_coords = self.texts['gameOver'].texts[0].coords
		second_coords = self.texts['gameOver'].texts[1].coords
		if self.texts['gameOver'].pointer == 0:
			first_text = text_render.render(self.texts['gameOver'].texts[0].text, 5, (0, 0, 0))
			second_text = text_render.render(self.texts['gameOver'].texts[1].text, 5, (255, 255, 255))
			rect_text = first_text.get_rect()

			surf = pygame.Surface((rect_text.width, rect_text.height))
			surf.fill((255, 255, 255))

			window.windows[window.status].screen.blit(surf, first_coords)
			window.windows[window.status].screen.blit(first_text, first_coords)
			window.windows[window.status].screen.blit(second_text, second_coords)
		else:
			first_text = text_render.render(self.texts['gameOver'].texts[0].text, 5, (255, 255, 255))
			second_text = text_render.render(self.texts['gameOver'].texts[1].text, 5, (0, 0, 0))
			rect_text = second_text.get_rect()

			surf = pygame.Surface((rect_text.width, rect_text.height))
			surf.fill((255, 255, 255))

			window.windows[window.status].screen.blit(surf, second_coords)
			window.windows[window.status].screen.blit(first_text, first_coords)
			window.windows[window.status].screen.blit(second_text, second_coords)

		pygame.display.update()

	def drawWinWindow(self, window, text_render):
		window.windows[window.status].screen.fill((0, 0, 0))
		first_coords = self.texts['winWindow'].texts[0].coords
		second_coords = self.texts['winWindow'].texts[1].coords
		if self.texts['winWindow'].pointer == 0:
			first_text = text_render.render(self.texts['winWindow'].texts[0].text, 5, (0, 0, 0))
			second_text = text_render.render(self.texts['winWindow'].texts[1].text, 5, (255, 255, 255))
			rect_text = first_text.get_rect()

			surf = pygame.Surface((rect_text.width, rect_text.height))
			surf.fill((255, 255, 255))

			window.windows[window.status].screen.blit(surf, first_coords)
			window.windows[window.status].screen.blit(first_text, first_coords)
			window.windows[window.status].screen.blit(second_text, second_coords)
		else:
			first_text = text_render.render(self.texts['winWindow'].texts[0].text, 5, (255, 255, 255))
			second_text = text_render.render(self.texts['winWindow'].texts[1].text, 5, (0, 0, 0))
			rect_text = second_text.get_rect()

			surf = pygame.Surface((rect_text.width, rect_text.height))
			surf.fill((255, 255, 255))

			window.windows[window.status].screen.blit(surf, second_coords)
			window.windows[window.status].screen.blit(first_text, first_coords)
			window.windows[window.status].screen.blit(second_text, second_coords)

		pygame.display.update()

	def drawGame(self, window, ball, platform, blocks, text_render):
		window.windows[window.status].screen.fill((0, 0, 0))
		window.windows[window.status].surf.fill((255, 255, 255))
		window.windows[window.status].screen.blit(window.windows[window.status].surf,
			(window.windows[window.status].surfX, window.windows[window.status].surfY))

		score_text = window.windows[window.status].surfTexts[0].text + str(window.windows[window.status].score)
		score_text = text_render.render(score_text, 5, (0, 0, 0))
		score_coords = window.windows[window.status].surfTexts[0].coords

		window.windows[window.status].screen.blit(score_text, score_coords)
		ball.draw(window.windows[window.status].screen)
		platform.draw(window.windows[window.status].screen)
		for el in blocks:
			el.draw(window.windows[window.status].screen)
		pygame.display.update()

	def drawPause(self, window, text_render):
		window.windows[window.status].screen.fill((0, 0, 0))
		first_coords = self.texts['pauseGame'].texts[0].coords
		second_coords = self.texts['pauseGame'].texts[1].coords
		third_coords = self.texts['pauseGame'].texts[2].coords
		if self.texts['pauseGame'].pointer == 0:
			first_text = text_render.render(self.texts['pauseGame'].texts[0].text, 5, (0, 0, 0))
			second_text = text_render.render(self.texts['pauseGame'].texts[1].text, 5, (255, 255, 255))
			third_text = text_render.render(self.texts['pauseGame'].texts[2].text, 5, (255, 255, 255))
			rect_text = first_text.get_rect()

			surf = pygame.Surface((rect_text.width, rect_text.height))
			surf.fill((255, 255, 255))

			window.windows[window.status].screen.blit(surf, first_coords)
			window.windows[window.status].screen.blit(first_text, first_coords)
			window.windows[window.status].screen.blit(second_text, second_coords)
			window.windows[window.status].screen.blit(third_text, third_coords)
		elif self.texts['pauseGame'].pointer == 1:
			first_text = text_render.render(self.texts['pauseGame'].texts[0].text, 5, (255, 255, 255))
			second_text = text_render.render(self.texts['pauseGame'].texts[1].text, 5, (0, 0, 0))
			third_text = text_render.render(self.texts['pauseGame'].texts[2].text, 5, (255, 255, 255))
			rect_text = second_text.get_rect()

			surf = pygame.Surface((rect_text.width, rect_text.height))
			surf.fill((255, 255, 255))

			window.windows[window.status].screen.blit(surf, second_coords)
			window.windows[window.status].screen.blit(first_text, first_coords)
			window.windows[window.status].screen.blit(second_text, second_coords)
			window.windows[window.status].screen.blit(third_text, third_coords)
		else:
			first_text = text_render.render(self.texts['pauseGame'].texts[0].text, 5, (255, 255, 255))
			second_text = text_render.render(self.texts['pauseGame'].texts[1].text, 5, (255, 255, 255))
			third_text = text_render.render(self.texts['pauseGame'].texts[2].text, 5, (0, 0, 0))
			rect_text = third_text.get_rect()

			surf = pygame.Surface((rect_text.width, rect_text.height))
			surf.fill((255, 255, 255))

			window.windows[window.status].screen.blit(surf, third_coords)
			window.windows[window.status].screen.blit(first_text, first_coords)
			window.windows[window.status].screen.blit(second_text, second_coords)
			window.windows[window.status].screen.blit(third_text, third_coords)

		pygame.display.update()

	def get_eventsGameOverWindow(self, window, ball, platform, blocks):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					if event.key == pygame.K_UP:
						self.texts['gameOver'].pointer -= 1
					else:
						self.texts['gameOver'].pointer += 1
					self.texts['gameOver'].pointer = fabs(self.texts['gameOver'].pointer)
					self.texts['gameOver'].pointer %= 2
				elif event.key == pygame.K_RETURN:
					if self.texts['gameOver'].pointer == 0:
						window.windows[window.status].lastStatus = 'notStart'
						window.windows[window.status].status = 'notStart'
						ball.rect.x = 235
						ball.rect.y = 420
						platform.rect.x = 200
						platform.rect.y = 450
					else:
						window.windows[window.status].lastStatus = 'notStart'
						window.windows[window.status].status = 'notStart'
						window.status = 'startWindow'
						ball.rect.x = 235
						ball.rect.y = 420
						platform.rect.x = 200
						platform.rect.y = 450

	def get_eventsWinWindow(self, window, ball, platform, blocks):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					if event.key == pygame.K_UP:
						self.texts['winWindow'].pointer -= 1
					else:
						self.texts['winWindow'].pointer += 1
					self.texts['winWindow'].pointer = fabs(self.texts['winWindow'].pointer)
					self.texts['winWindow'].pointer %= 2
				elif event.key == pygame.K_RETURN:
					if self.texts['winWindow'].pointer == 0:
						window.windows[window.status].lastStatus = 'notStart'
						window.windows[window.status].status = 'notStart'
						ball.rect.x = 235
						ball.rect.y = 420
						platform.rect.x = 200
						platform.rect.y = 450
					else:
						window.windows[window.status].lastStatus = 'notStart'
						window.windows[window.status].status = 'notStart'
						window.status = 'startWindow'
						ball.rect.x = 235
						ball.rect.y = 420
						platform.rect.x = 200
						platform.rect.y = 450

					self.score = 0
					self.load_level('level' + '1', blocks)

	def get_eventsPauseGame(self, window, ball, platform, blocks):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					if window.windows[window.status].status is 'pauseGame':
						if window.windows[window.status].lastStatus is 'startGame':
							window.windows[window.status].status = 'startGame'
						else:
							window.windows[window.status].status = 'notStart'
						window.windows[window.status].lastStatus = 'pauseGame'
				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					if event.key == pygame.K_UP:
						self.texts['pauseGame'].pointer -= 1
						if self.texts['pauseGame'].pointer < 0:
							self.texts['pauseGame'].pointer = 2
					else:
						self.texts['pauseGame'].pointer += 1
					self.texts['pauseGame'].pointer %= 3
				elif event.key == pygame.K_RETURN:
					if self.texts['pauseGame'].pointer == 0:
						if window.windows[window.status].lastStatus is 'startGame':
							window.windows[window.status].status = 'startGame'
						else:
							window.windows[window.status].status = 'notStart'
						window.windows[window.status].lastStatus = 'pauseGame'
					elif self.texts['pauseGame'].pointer == 1:
						window.windows[window.status].lastStatus = 'notStart'
						window.windows[window.status].status = 'notStart'
						ball.rect.x = 235
						ball.rect.y = 420
						platform.rect.x = 200
						platform.rect.y = 450
						self.load_level('level' + '1', blocks)
						self.score = 0
					else:
						window.windows[window.status].lastStatus = 'notStart'
						window.windows[window.status].status = 'notStart'
						window.windows[window.status].score = 0
						window.status = 'startWindow'
						self.load_level('level' + '1', blocks)
						self.score = 0
						ball.rect.x = 235
						ball.rect.y = 420
						platform.rect.x = 200
						platform.rect.y = 450

	def get_eventsGamePlay(self, window, platform, ball):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				window.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					if window.windows[window.status].status is 'pauseGame':
						if window.windows[window.status].lastStatus is 'startGame':
							window.windows[window.status].status = 'startGame'
						else:
							window.windows[window.status].status = 'notStart'
						window.windows[window.status].lastStatus = 'pauseGame'
					elif window.windows[window.status].status is 'startGame' or 'notStart':
						window.windows[window.status].lastStatus = window.windows[window.status].status
						window.windows[window.status].status = 'pauseGame'
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
					ball.objectCollision(platform)
				if window.windows[window.status].status is 'notStart':
					ball.update(platform)
			if keys[pygame.K_LEFT] and platform.rect.left + platform.speed > 0:
				platform.rect.x -= platform.speed
				if platform.rect.colliderect(ball.rect):
					platform.rect.x += platform.speed
					ball.objectCollision(platform)
				if window.windows[window.status].status is 'notStart':
					ball.update(platform)

	def load_level(self, name_file, blocks):
		path = 'levels/' + name_file
		level = open(path, 'r')
		blocks.clear()

		for line in level.readlines():
			line = line.split()
			block = Block(int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]))
			blocks.append(block)

class Ball():
	def __init__(self, x, y, width, height, image, speed):
		self.rect = Rect(x, y, width, height)
		self.speed = speed
		self.image = image

	def objectCollision(self, obj):
		self.rect.x += self.speed[0]
		if self.rect.colliderect(obj.rect):
			self.rect.x -= self.speed[0]
			self.speed[0] *= -1
			self.rect.y += self.speed[1]
			return

		self.rect.y += self.speed[1]
		if self.rect.colliderect(obj.rect):
			self.rect.y -= self.speed[1]
			self.speed[1] *= -1

	def collisionsBlocks(self, blocks, platform, window):
		collisBlock = self.rect.collidelist(blocks)
		collisPlatform = self.rect.colliderect(platform.rect)
		if collisBlock is not -1:
			block = blocks[collisBlock]
			self.unmove()
			self.objectCollision(block)
			block.health -= 1
			if block.health == 0:
				window.windows[window.status].score += 1
				del blocks[collisBlock]
			else:
				block.image = pygame.image.load('image/blocks/' + str(block.health) + '.png')
				block.image = pygame.transform.scale(block.image, (block.rect.width, block.rect.height))
		if collisPlatform:
			self.unmove()
			self.objectCollision(platform)

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
	def __init__(self, x, y, width, height, health):
		self.rect = Rect(x, y, width, height)
		self.health = health
		self.image = pygame.image.load('image/blocks/' + str(health) + '.png')
		self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

	def draw(self, window):
		window.blit(self.image, (self.rect.x, self.rect.y))

class Platform():
	def __init__(self, x, y, width, height, image, speed):
		self.rect = Rect(x, y, width, height)
		self.image = image
		self.speed = speed

	def draw(self, window):
		window.blit(self.image, (self.rect.x, self.rect.y))