"""
The Code for Kociemba was take from: https://github.com/hkociemba/RubiksCube-TwophaseSolver
"""
import solver

def fitness(cube_orientation):
	"""
	This function will evaluate the fitness score of the cube orientation.
	The fitness function is called the 3D manhattan distance.
	In the context of the Rubik's cube it is the minimum number of moves needed to solve the cube from the current position.
	This will be evaluated by the Kociemba two phase solver.
	"""
	
	# We need to change the cube orientation as "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
	# Our cube orientation sequence is as follows: 
	# yyyyyyyyyooooooooogggggggggwwwwwwwwwrrrrrrrrrbbbbbbbbb
	# Yellow on top red on left
	# [y]ellow = [U]P, [o]range = [R]ight, [g]reen = [F]ront, [w]hite = [D]own, [r]ed = [L]eft, [b]lue = [B]ack 
	
	cubestring = ""
		
	for i in range(len(cube_orientation)):
		# In the cube orientation if the color is yellow change it to U as yellow is on top
		if cube_orientation[i] == "y":
			cubestring = cubestring + "U"
		
		# In the cube orientation if the color is blue change it to B as blue is on back
		elif cube_orientation[i] == "b":
			cubestring = cubestring + "B"
		
		# In the cube orientation if the color is red change it to L as red is on left
		elif cube_orientation[i] == "r":
			cubestring = cubestring + "L"
		
		# In the cube orientation if the color is green change it to F as red is on front
		elif cube_orientation[i] == "g":
			cubestring = cubestring + "F"
		
		# In the cube orientation if the color is orange change it to R as orange is on right
		elif cube_orientation[i] == "o":
			cubestring = cubestring + "R"
		
		# In the cube orientation if the color is white change it to D as red is on down
		elif cube_orientation[i] == "w":
			cubestring = cubestring + "D"
	
	# Remove the last character of a solution as it is just a space and split it by space so we can count the moves
	solution = solver.solve(cubestring)[:-1].split(" ")
	
	# Return the length of the solution
	return len(solution)