level_file = open('level1', 'w')

for i in range(5):
	x =  5 + i * 100
	y = 90
	width = 95
	height = 30
	s = str(x) + ' ' + str(y) + ' ' + str(width) + ' ' + str(height) + '\n'
	level_file.write(s)

for i in range(5):
	x =  5 + i * 100
	y = 121
	width = 95
	height = 30
	s = str(x) + ' ' + str(y) + ' ' + str(width) + ' ' + str(height) + '\n'
	level_file.write(s)

level_file.close()