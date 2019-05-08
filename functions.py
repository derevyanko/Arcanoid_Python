import pygame
from objects import Block

def collisionsBlocks(blocks, platform, ball):
	collisBlock = ball.rect.collidelist(blocks)
	collisPlatform = ball.rect.colliderect(platform.rect)
	if collisBlock is not -1:
		ball.unmove()
		objectCollision(blocks[collisBlock], ball)
		del blocks[collisBlock]
	if collisPlatform:
		ball.unmove()
		objectCollision(platform, ball)

def objectCollision(obj, ball):
	ball.rect.x += ball.speed[0]
	if ball.rect.colliderect(obj.rect):
		ball.rect.x -= ball.speed[0]
		ball.speed[0] *= -1
		ball.rect.y += ball.speed[1]
		return

	ball.rect.y += ball.speed[1]
	if ball.rect.colliderect(obj.rect):
		ball.rect.y -= ball.speed[1]
		ball.speed[1] *= -1

def get_events(window, platform, ball):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			window.run = False
	# 	elif event.type == pygame.KEYDOWN:
	# 		if event.key == pygame.K_ESCAPE:
	# 			if window.windows[window.status].status is 'pauseGame':
	# 				if window.windows[window.status].lastStatus is 'startGame':
	# 					window.windows[window.status].status = 'startGame'
	# 				else:
	# 					window.windows[window.status].status = 'notStart'
	# 				window.windows[window.status].lastStatus = 'pauseGame'
	# 				window.status = 'gameplay'
	# 			elif window.windows[window.status].status is 'startGame' or 'notStart':
	# 				window.windows[window.status].lastStatus = window.windows[window.status].status
	# 				window.windows[window.status].status = 'pauseGame'
	# 				window.status = 'pause'
	# 		elif event.key == pygame.K_SPACE and window.windows[window.status].status is not 'pauseGame':
	# 			if window.windows[window.status].status is not 'startGame':
	# 				window.windows[window.status].status = 'startGame'
	# 				window.windows[window.status].lastStatus = 'notStart'

	# keys = pygame.key.get_pressed()
	# if window.windows[window.status].status is not 'pauseGame':
	# 	if keys[pygame.K_RIGHT] and platform.rect.right + platform.speed < 500:
	# 		platform.rect.x += platform.speed
	# 		if platform.rect.colliderect(ball.rect):
	# 			platform.rect.x -= platform.speed
	# 			objectCollision(platform, ball)
	# 		if window.windows[window.status].status is 'notStart':
	# 			ball.update(platform)
	# 	if keys[pygame.K_LEFT] and platform.rect.left + platform.speed > 0:
	# 		platform.rect.x -= platform.speed
	# 		if platform.rect.colliderect(ball.rect):
	# 			platform.rect.x += platform.speed
	# 			objectCollision(platform, ball)
	# 		if window.windows[window.status].status is 'notStart':
	# 			ball.update(platform)

def draw_all(window, ball, platform, blocks):
	window.windows[window.status].screen.fill((0, 0, 0))
	ball.draw(window.windows[window.status].screen)
	platform.draw(window.windows[window.status].screen)
	for el in blocks:
		el.draw(window.windows[window.status].screen)
	pygame.display.update()

def load_level(name_file):
	path = 'levels/' + name_file
	level = open(path, 'r')
	blocks = []
	
	for line in level.readlines():
		line = line.split()
		block = Block(int(line[0]), int(line[1]), int(line[2]), int(line[3]))
		blocks.append(block)

	return blocks