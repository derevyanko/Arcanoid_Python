import pygame

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
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if window.windows[0].status is 'pauseGame':
					if window.windows[0].lastStatus is 'startGame':
						window.windows[0].status = 'startGame'
					else:
						window.windows[0].status = 'notStart'
					window.windows[0].lastStatus = 'pauseGame'
				elif window.windows[0].status is 'startGame' or 'notStart':
					window.windows[0].lastStatus = window.windows[0].status
					window.windows[0].status = 'pauseGame'
			elif event.key == pygame.K_SPACE and window.windows[0].status is not 'pauseGame':
				if window.windows[0].status is not 'startGame':
					window.windows[0].status = 'startGame'
					window.windows[0].lastStatus = 'notStart'

	keys = pygame.key.get_pressed()
	if window.windows[0].status is not 'pauseGame':
		if keys[pygame.K_RIGHT] and platform.rect.right + platform.speed < 500:
			platform.rect.x += platform.speed
			if platform.rect.colliderect(ball.rect):
				platform.rect.x -= platform.speed
				objectCollision(platform, ball)
			if window.windows[0].status is 'notStart':
				ball.update(platform)
		if keys[pygame.K_LEFT] and platform.rect.left + platform.speed > 0:
			platform.rect.x -= platform.speed
			if platform.rect.colliderect(ball.rect):
				platform.rect.x += platform.speed
				objectCollision(platform, ball)
			if window.windows[0].status is 'notStart':
				ball.update(platform)

def draw_all(window, ball, platform, blocks):
	window.screen.fill((0, 0, 0))
	ball.draw(window.screen)
	platform.draw(window.screen)
	for el in blocks:
		el.draw(window.screen)
	pygame.display.update()