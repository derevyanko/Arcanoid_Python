def gameplay(window, ball):
	if window.windows[0].status is 'startGame':
		ball.move()
	if ball.rect.bottom > 450:
		window.run = False
		print('Game over!')
	if ball.rect.left < 0 or ball.rect.right > 500:
		ball.speed[0] *= -1
	if ball.rect.top < 0:
		ball.speed[1] *= -1