import scrambleGenerator as sg

def scramble(flag, properScramble, noofMoves):
	"""
	This function will scramble the cube randomly and will return the colors on each cubelets
	"""
	
	# This part means to just scramble the cube
	if flag == False:
		s, cube = sg.generate()
	
	# This part means to apply moves to the cube
	else:
		cube = sg.makeMove(properScramble, noofMoves)
		s = properScramble
	
	# The fitness function will only evaluate the fitness of the cube if the colors in each individual stickers are given to it.
	# So we will map each individual sticker to a color
	cubelets = [
				cube[0][0], cube[0][1], cube[0][2], cube[0][7], 'y', cube[0][3], cube[0][6], cube[0][5], cube[0][4],
				cube[3][0], cube[3][1], cube[3][2], cube[3][7], 'o', cube[3][3], cube[3][6], cube[3][5], cube[3][4],
				cube[2][0], cube[2][1], cube[2][2], cube[2][7], 'g', cube[2][3], cube[2][6], cube[2][5], cube[2][4],
				cube[5][0], cube[5][1], cube[5][2], cube[5][7], 'w', cube[5][3], cube[5][6], cube[5][5], cube[5][4],
				cube[1][0], cube[1][1], cube[1][2], cube[1][7], 'r', cube[1][3], cube[1][6], cube[1][5], cube[1][4],						
				cube[4][0], cube[4][1], cube[4][2], cube[4][7], 'b', cube[4][3], cube[4][6], cube[4][5], cube[4][4]											
			]
			
	# We will be converting the list to string
	cube_orientation = ''.join([str(elem) for elem in cubelets]) 
	scramble = ""
	for array in s:
		for elem in array:
			scramble = scramble + elem
		scramble = scramble + " "
		
	return scramble, cube_orientation