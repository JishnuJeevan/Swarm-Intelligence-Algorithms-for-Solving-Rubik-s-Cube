import FitnessFunction as fit
import Scramble 
import math
import random
from scrambleGenerator import makeMove
import matplotlib.pyplot as plt
from os import system, name 
import time


def bubbleSort(possibleMoves): 
	"""
	This is a bubble sort function.
	This function takes all the moves applied to the cube and the fitness obtained when applying those moves,
	and sorts them in ascending order.
	I wrote this function as the inbuilt function like sort(), sorted() didn't give proper outputs.
	"""

	# Find the length of the array
	n = len(possibleMoves) 

	# Traverse through all array elements 
	for i in range(n-1): 

		# Last i elements are already in place 
		for j in range(0, n-i-1): 

			# traverse the array from 0 to n-i-1 
			# Swap if the element found is greater, than the next element 
			# We will have to compare the values i.e. the fitness values
			if possibleMoves[j][1] > possibleMoves[j+1][1] : 
				possibleMoves[j], possibleMoves[j+1] = possibleMoves[j+1], possibleMoves[j] 


def convert2Scramble(scramble):
	"""
	This will take a string "F F' F2"and will convert it into the form [['F',''],['F',"'"],['F','2']].
	We need to give it in the above format for the scrambling to work
	"""
	# Create an empty array to store the moves
	properScramble = []

	# Split based on the space between characters
	moves = scramble.split(" ")
	
	# Delete the last element as it is a space
	del moves[-1]	

	# Take every moves
	for m in moves:
		subMoves = ["", ""]
		if m == "F'" or m == "B'" or m == "R'" or m == "L'" or m == "U'" or m == "D'" or m == "F2" or m == "B2" or m == "R2" or m == "L2" or m == "U2" or m == "D2":
			subMoves[0] = m[0]
			subMoves[1] = m[1]
		else:
			subMoves[0] = m
			subMoves[1] = ""

		properScramble.append(subMoves)

	# Return the proper scramble format
	return properScramble


def FindAllPossibleMoves(legal_moves, AllAppliedMoves, possibleMoveTree):
	"""
	This function will return all the possible moves that can be applied to the cube,
	along with the fitness value for each moves.
	The output will be in the format [[U, 18], [U', 18], ..].
	This will be appended to an array called the possibleMoveTree which will hold the possible moves at each depth.
	"""
	
	# This will hold all the possible moves from the current state along with its fitness values
	# This will be an array with a list [moves, fitness]
	possibleMoves = []
		
	# Take each possible move from the list of legal moves
	for i in range(len(legal_moves)):
		
		# Apply that move to the cube
		properScramble = convert2Scramble(AllAppliedMoves + legal_moves[i] + " ")
		
		# Find the length of the scramble
		noofMmoves = len(properScramble)	
		
		# Make that scramble and get the orientation
		scramble, cube_orientation = Scramble.scramble(True, properScramble, noofMmoves)
		
		# Now find the fitness value for the cube orientation
		fitnessValue = fit.fitness(cube_orientation)
		
		# Now add the move and its fitnessValue to the dictionary
		possibleMoves.append([legal_moves[i], fitnessValue])
	
	# Now we are going to sort the list of moves and its fitness function.
	# Now I am going to sort this using bubble sort as the pre defined sort function in python can't sort it properly.		
	bubbleSort(possibleMoves)
		
	# Now we are going to append it to the list that holds the possible moves at each depth
	possibleMoveTree.append(possibleMoves)	
	
	# Return the possible move tree
	return possibleMoveTree


def GREEDY(iterations, flag, scramble):
	"""
	This function uses a greedy approach with backtracking to find the shortest path to the solved state.
	It works as follows:
	1. Find the fitness function of the current state of the cube.
	2. Apply all the 18 legal moves to the cube and find the fitness value of the next possible legal states.
	3. Sort the state and the moves in ascending order of fitness value.
	4. Apply the move that gives minimum fitness value.
	5. If the fitness value of all 18 moves is greater than previous state undo the move applied to the previous state
	6. Repeat steps 1 - 5 till the state is solved state.	
	"""
	
	# Problem definition for the greedy tree search
	# This returns the scramble and the orientation of the stickers in the cube
		
	# If it is a random scramble
	if flag == False:
		# Problem definition
		scramble, cube_orientation = Scramble.scramble(flag,scramble,0)	# This returns the scramble and the orientation of the stickers in the cube
	
	# Else if it is a manual scramble
	else:
		# Now apply the move to the cube
		properScramble = convert2Scramble(scramble)
		
		# Find the length of the scramble
		noofMmoves = len(properScramble)	
		
		# Make that scramble and get the orientation
		scramble, cube_orientation = Scramble.scramble(flag, properScramble, noofMmoves)
	
	# Save the scramble used
	originalScramble = scramble
	
	# Save the initial cube orientation
	initialOrientation = cube_orientation
	
	# Original Fitnees score
	originalFitness = fit.fitness(cube_orientation)
	
	# Print the initial orientation
	print("Scramble : ",originalScramble)
	print("Initial cube orientation: ", initialOrientation)
	print("Initial fitness : ",originalFitness)
	print("\n")
	
	# We are going to create a few data structures to hold a set of ingormations
	
	# A data structure to hold the legal moves available  i.e. U,U',U2,...,R,R',R2.
	# Since Kociemba works on half turn metric where two turns of the side are counted as one move we will use half turn metric.
	legal_moves = ["U", "U'", "U2", "D", "D'","D2", 
				   "L","L'", "L2", "R", "R'", "R2",
				   "F","F'", "F2", "B", "B'", "B2",				   
				  ]	
	
	# You see the Kociemba has a problem. Sometimes it can give two different solution to the same problem. 
	# So we need to make sure that it doesn't evaluate the same position twice. 
	# So we use this data structure to hold the evaluated scores.
	# This list will hold the orientation of the cube.
	orientations = []
	orientations.append(initialOrientation)	# This is the scrambled position
	
	# This will hold the fitness value at each depth for each orientation
	fitnessValues = []
	fitnessValues.append(originalFitness)	# This is the fitness of the scrambled position
	
	# This list will hold the moves applied to the cube and the fitness values
	movesApplied = []
	
	# This varaible will hold all the moves applied to the cube.
	# This is just used for plotting. Has no other function.
	movesAppliedAll = []
	
	# This will hold the possible moves at each depth
	possibleMoveTree = []
	
	# This variable will hold the moves that are applied to the cube including the scramble
	# Initially only the scramble has been applied to the cube
	AllAppliedMoves = originalScramble
	
	# This variable is used to hold the maximum depth that the algorithm went to find the solution
	maxDepth = 0
	
	# This variable is used to store the values for plotting a graph of depth vs fitness
	# X holds the depth and Y holds the fitness
	xDepth = []
	xDepth.append(len(possibleMoveTree))	# We will append depth 0 i.e. scrambled state
	yFitness = []	
	yFitness.append(fitnessValues[-1])	# We will append the fitness of depth 0 i.e. scrambled state
	
	# This set of variable are used to hold all the fitness values reached in the same depth.
	xDepthAll = []
	xDepthAll.append(len(possibleMoveTree))
	yFitnessAll = []	# This will hold all the fitness values reached at a depth
	yFitnessAll.append(fitnessValues[-1])
	
	# This variable will hold the iteration and also fitness at each iteration
	xIter = []
	yFitnessIter = []	# This is used to hold the fitness reached at each iteration
		
	# This variable is used to check if the solution has been found
	# This will be set to true if it could not be found.
	flag = False
	
	# We will set an iteration limit. 
	# If the program execution exceded the limit, we will break out of the loop.
	iteration_limit = iterations
	iter = 0	# Iteration starts from 0
	
	start_time = time.time()	# This is were the execution begins
	while(True):
		
		print("\n")
		print("Iteration : ",iter)
		
		# Continue the while loop till the cube is solved
		if orientations[-1] == "yyyyyyyyyooooooooogggggggggwwwwwwwwwrrrrrrrrrbbbbbbbbb":
			break
		
		# Call the possible move function.
		# This is used to find all the possible moves that can be applied from the given state.
		possibleMoveTree = FindAllPossibleMoves(legal_moves, AllAppliedMoves, possibleMoveTree)
		
		# We need to do backtracking till we get a condition where we dont need to backtrack
		while(True):
			
			print("\n")
			print("Total Depth : ", len(possibleMoveTree))
			
			# We need to check a condition that can happen sometime. 
			# The scrambled cube has a fitness value of lets say 8.
			# And all the possible 18 moves give fitness value greater than 8. 
			# This means that we cannot apply a move to the cube. 
			# In this case we will just select the first move available and see where it goes. 
			
			# This should only be done in depth 1. 
			if len(possibleMoveTree) == 1:
				count = 0
				for i in range(len(possibleMoveTree[-1])):
					if possibleMoveTree[-1][i][1] > fitnessValues[-1]:
						count +=1
				
				# If all the possible moves have fitness greater than the scrambled state at depth 1.
				# Just apply the first minimum move and see where it leads.
				if count == len(possibleMoveTree[-1]):
					print("No possible moves give fitness less than previous level.")
					print("So we take the ones we have now.")
				
					# Now we will select the move from the last depth
					move = possibleMoveTree[-1].pop(0) # This will be an array [move, fitness]
					
					# Now we have got the move, now apply the move to the cube
					properScramble = convert2Scramble(AllAppliedMoves + move[0] + " ")
			
					# Find the length of the scramble
					noofMmoves = len(properScramble)	
					
					# Make that scramble and get the orientation when the move is applied
					scramble, new_orientation = Scramble.scramble(True, properScramble, noofMmoves)
					
					newFitness = move[1]	# We have already applied the move and found the fitness value. So we just have to take that from [move, fitness]
					oldFitness = fitnessValues[-1]	# To prevent getting a different fitness value we take the stored fitness value.
					
					# Save the cube orientation
					orientations.append(new_orientation)
					fitnessValues.append(newFitness)
					print("Orientation : ", new_orientation, end = " ")
					print("Move applied : ", move[0], end = " ")
					print("New Fitnees : ", newFitness, end = " ")
					print("Old Fitnees :", oldFitness)
					print("Fitnees Stack : ",fitnessValues)
					
					# Now save the values to plot the graph 
					# This graph is used to show all the nodes that the algorithm visited in each depth
					xDepth.append(len(possibleMoveTree))
					yFitness.append(newFitness)
					xDepthAll.append(len(possibleMoveTree))
					yFitnessAll.append(newFitness)
					
					# This graph is used to show the fitness value at each depth.
					xIter.append(iter)
					yFitnessIter.append(newFitness)
					
					# Save the move applied
					movesApplied.append(move[0])
					
					# This is just for plotting
					movesAppliedAll.append(move[0])
					
					# Save it to all the moves applied
					AllAppliedMoves = AllAppliedMoves + move[0] + " "
					
					# Break out of this loop as we have applied the move.
					# Break out of the inner while loop.
					break
			
			# Update the maximum depth
			if len(possibleMoveTree) > maxDepth:
				maxDepth = len(possibleMoveTree)
			
			# Print the depth reached and branches at each depth.
			for i in range(len(possibleMoveTree)):				
				print("Depth : ", i+1 , end = " ")
				print("Branches : ", len(possibleMoveTree[i]), end = " ")
				for j in range(len(possibleMoveTree[i])):
					print("|",possibleMoveTree[i][j][0],possibleMoveTree[i][j][1],end = " ")
				print("\n")
			print("\n")
			
			# Now we will take the move that gave the smallest fitness value.		
			# From the last depth take the first move in the list (along with fitness value)
			
			# But we need to make sure that there are branches in the last depth
			while (len(possibleMoveTree[-1]) == 0):
				print("Branch empty, so backtracking")
				
				# Remove the cube orientation
				orientations.pop(-1)
				
				# Remove the fitness value
				fitnessValues.pop(-1)		
				
				# Remove the last move applied
				movesApplied.pop(-1)
				
				# Split it by space, we get a list
				AllMoves = AllAppliedMoves.split(" ")
				
				# Copy it to another list, except the last element. The last element is space and the second last is the move applied.
				AllMoves = AllMoves[:-2]
				
				# Convret the list to string 
				AllAppliedMoves = " ".join([str(elem) for elem in AllMoves]) 
				
				# Add space at the end
				AllAppliedMoves = AllAppliedMoves + " "
				
				# Delete the last depth of the tree as it will be just an empty list.
				arr = possibleMoveTree.pop(-1)			
				
				# Now remove the graph values as we are undoing the applied move
				xDepth.pop(-1)
				yFitness.pop(-1)	# We won't remove yFitnessAll as we need that variable to print all fitness value reached at a certain depth.
				
				# If the branches of depth 1 are empty then the possible move tree is also empty.
				# So break out of this while loop
				if len(possibleMoveTree) == 0:
					flag = True
					break
			
			# Now if there are no more branches to search then sadly the algorithm could not find the solution.
			# So break out of the inner while loop. No need to continue further as there are no more moves left.
			if len(possibleMoveTree) == 0:
					flag = True
					break
			
			# Now we will select the move from the last depth
			move = possibleMoveTree[-1].pop(0) # This will be an array [move, fitness]
			
			# Now we have got the move. But we need to check if its fitness is less than previous state.
			# Now apply the move to the cube
			properScramble = convert2Scramble(AllAppliedMoves + move[0] + " ")
	
			# Find the length of the scramble
			noofMmoves = len(properScramble)	
			
			# Make that scramble and get the orientation when the move is applied
			scramble, new_orientation = Scramble.scramble(True, properScramble, noofMmoves)
			
			# Here we will compare the fitness value of previous state with fitness value when a single move is applied.
			# If the finess value of new state is greater than previous state then we need to select a new move.
			newFitness = move[1]	# We have already applied the move and found the fitness value. So we just have to take that from [move, fitness]
			oldFitness = fitnessValues[-1]	# To prevent getting a different fitness value we take the stored fitness value.
			if newFitness > oldFitness:
				print(newFitness, ">", oldFitness)
				continue
			
			# We need to make sure that a cycle isn't produced.
			# If the new orientation is already reached state then there is a chance that a cycle will be produced.
			# So we will skip the move applied so that we don't reach that state and cause a cycle.
			elif new_orientation in orientations:
				print("Cycle.")
				continue
			
			# If the fitness value is less than previous level, we can apply that move 
			# And we are sure that it won't produce a cycle.
			else:
				
				# Save the cube orientation
				orientations.append(new_orientation)
				fitnessValues.append(newFitness)
				print("Orientation : ", new_orientation, end = " ")
				print("Move applied : ", move[0], end = " ")
				print("New Fitnees : ", newFitness, end = " ")
				print("Old Fitnees :", oldFitness)
				print("Fitnees Stack : ",fitnessValues)
				
				# Now save the values to plot the graph 
				# This graph is used to show all the nodes that the algorithm visited in each depth
				xDepth.append(len(possibleMoveTree))
				yFitness.append(newFitness)
				xDepthAll.append(len(possibleMoveTree))
				yFitnessAll.append(newFitness)
				
				# This graph is used to hold the fitness value at each iteration
				xIter.append(iter)
				yFitnessIter.append(newFitness)
				
				# Save the move applied
				movesApplied.append(move[0])
				
				# For plotting
				movesAppliedAll.append(move[0])
				
				# Save it to all the moves applied
				AllAppliedMoves = AllAppliedMoves + move[0] + " "
				
				# Break out of this loop
				break
		
		# Now if there are no more branches to search then sadly the algorithm could not find the solution.
		# So break out of the outer while loop. No need to continue further as there are no more moves left.
		if len(possibleMoveTree) == 0:
			flag = True
			break
		
		# Increment the iteration
		iter+=1
				
		# If the program execution exceded iteration limit we will exit the program
		if iter == iteration_limit:
			flag = True
			print("Iteration Limit of : ",iteration_limit, " exceeded.")
			break
		
	end_time = time.time()	# This is where the entire PSO loop finishes execution
	total_time = end_time - start_time	# This is the total time needed for the loop execution
	
	# Print the initial cube orientation
	print("\n")
	print("Cube orientation: Yellow on top and green on front.")
	print("Reading order goes: Up, Right, Front, Down, Left, Back.")
	print("Scramble: ", originalScramble)
	print("Initial cube orientation : ",initialOrientation)
		
	if flag == True:
		print("Solution could not be found.")
	
	else:
		print("Solution Was Found.")
	
	# Convert the list to string
	solution = " ".join([str(elem) for elem in movesApplied]) 
	print("\n")
	print("Fitnees Stack : ",fitnessValues)
	print("Solution : ", solution)
	print("Length : ",len(movesApplied))
	print("Total Time : ", total_time)
	print("Iteration : ",iter)
	print("Maximum Depth the algorithm went : ", maxDepth)
	print("Minimum Fitnees The Algorithm Reached : ",min(yFitnessAll))
	print("Original Fitnees : ",originalFitness)
	
	# Create two sub plots
	fig, ax = plt.subplots(2)
	
	# Make sure both graphs have grids
	ax[0].grid(True)
	ax[1].grid(True)
	
	# We will plot the fitness at each depth
	ax[0].scatter(xDepthAll,yFitnessAll,c="green",marker = 'o')
	
	# Now we will annotate the point with moves 
	for x, y, m in zip(xDepthAll, yFitnessAll, movesAppliedAll):
		ax[0].annotate(m,(x,y),color = "black", fontsize = 8)	

	# This will plot the path took at each depth.
	ax[0].plot(xDepth, yFitness, c="red", marker='.', linestyle=':')	
	
	# Now we will annotate the point with moves 
	for x, y, m in zip(xDepth, yFitness, movesApplied):
		ax[0].annotate(m,(x,y),(x,y+0.2), color="red", fontsize = 10)
	
	# Now plot iteration vs fitness
	ax[1].plot(xIter,yFitnessIter,marker="o")
	
	# Set the label and title for graph "Depth vs Fitnees"
	ax[0].set(xlabel='Depth', ylabel='Fitnees')
	ax[0].set_title('Depth vs Fitness')	# giving a title to my graph  
	
	# Set the label and title for graph "Iteration vs Fitnees"
	ax[1].set(xlabel='Iteration', ylabel='Fitnees')
	ax[1].set_title('Iteration vs Fitness')	# giving a title to my graph  
	fig.tight_layout()
	plt.show()


# Main program
if __name__ == "__main__":
	print("\n")
	print("Greedy Tree Search Algorithm")
	iterations = int(input("Enter the number of iterations : "))
	randomOrManual = input("Type M for manual scramble or R for random scrabmle : ")
	if randomOrManual == "R":
		flag = False
		scramble = ""
	elif randomOrManual == "M":
		flag = True
		scramble = input("Type scramble : ")
		
	# Function call
	# Add space to the scramble entered by the user, implementation reason.
	GREEDY(iterations, flag, scramble+" ")	# Calling the ACO algorithm	