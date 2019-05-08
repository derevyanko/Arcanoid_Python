level_file = open('/level1', 'w')

for i in range(4):
	x =  30 + i * 110
	y = 10
	width = 100
	height = 40
	s = str(x) + ' ' + str(y) + ' ' + str(width) + ' ' + str(height) + '\n'
	level_file.write(s)

for i in range(4):
	x =  30 + i * 110
	y = 60
	width = 100
	height = 40
	s = str(x) + ' ' + str(y) + ' ' + str(width) + ' ' + str(height) + '\n'
	level_file.write(s)

level_file.close()