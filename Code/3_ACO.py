import FitnessFunction as fit
import Scramble 
import math
import random
from scrambleGenerator import makeMove
import matplotlib.pyplot as plt
from os import system, name 
import time
import sys


def convert2Scramble(scramble):
	"""
	This will take a string "F F' F2"and will convert it into the form [['F',''],['F',"'"],['F','2']].
	We need to give it in the above format for the scrambling to work
	"""
	# Create an empty array to store the moves
	properScramble = []

	# Split based on the space between characters
	moves = scramble.split(" ")
	#print("Moves : ",moves)
	
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
	
	
# Function definition
def ACO(iterations, ants, al, be, flag, scramble):
	
	# Problem definition for the ACO
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
	
	# Save the scramble used, we might want to show it later
	originalScramble = scramble
	
	# Save the initial cube orientation, we might want to show it later
	initialOrientation = cube_orientation
	
	# Original Fitnees score, we might want to show it later.
	originalFitness = fit.fitness(cube_orientation)
	
	# Print the initial orientation
	print("Scramble : ",originalScramble)
	print("Initial cube orientation: ", cube_orientation)
	print("Initial Fitnees : ",originalFitness)
	print("\n")
	
	# Parameters of the Ant colony optimization
	maxIter = iterations	# Maximum number of iterations
	nPop = ants	# Maximum population size i.e th total number of particles
	
	# Varaible declarartion. We need to create data structures to hold certain varaible values
	
	# A data structure to hold the legal moves available  i.e. U,U',U2,...,R,R',R2.
	# Since Kociemba works on half turn metric where two turns of the side are counted as one move we will use half turn metric.
	legal_moves = ["U", "U'", "U2", "D", "D'","D2", "L","L'", "L2", "R", "R'", "R2", "F","F'", "F2", "B", "B'", "B2"]	
	
	# This datastructure will hold all the moves applied from the solved state, starting with the scramble
	ant_AllMoves = []	
	
	# A data structure to hold the position of each particle i.e which orientation they are in
	ant_Orientation = []
	
	# A data structure to hold the moves that made the particle to reach this position
	ant_OrientationMoves = [] 
	
	# This varaible will hold the fitness value for each at
	ant_fitness = []
	
	# This list is used to hold all the particles that found the solved state and other information like the iteration it found the solution, length etc.
	solution = []	
	
	# This dictionary will hold all the states visited by the ant and the pheromone from values from each state
	# Initially only the scrambled state has been visited, and the pheromone value for each edge from the scramble state is 0.000001
	# If we set it to 0 then the probability value will become either infinity or 0. This can mess up the calculation.
	# So we are setting it to a value close it 0 but negligable
	# But as ants pass through this state the pheromone values will change.
	pheromoneDict = {}
	pheromoneDict[cube_orientation]={"U":0.000001,"U'":0.000001,"U2":0.000001,
									 "D":0.000001,"D'":0.000001,"D2":0.000001,
									 "L":0.000001,"L'":0.000001,"L2":0.000001,
									 "R":0.000001,"R'":0.000001,"R2":0.000001,
									 "F":0.000001,"F'":0.000001,"F2":0.000001,
									 "B":0.000001,"B'":0.000001,"B2":0.000001}
	#print(pheromoneDict)
	#print(pheromoneDict[cube_orientation]["U"])
	
	# Initialization of varibles. Here we are going to initailze all the partices
	for i in range(nPop):
		
		# We are going to append the scramble used as that was the only move applied till now
		ant_AllMoves.append(scramble)	
		
		# Initially all the particles will be in the initial scrambled position	
		ant_Orientation.append(cube_orientation)	

		# Initially since no moves were made the data structure is empty
		ant_OrientationMoves.append("")	
		
		# The fitness value for all ants will be the fitness value for the scrambled state
		ant_fitness.append(originalFitness)
	
	# We will use these variables to group the ants to the state which give minimum fitness value after ceratin iteration
	# This variable will decide how many depths the ant must go before regrouping.
	iterationsDone = 0
	
	# We will also use this varaible to regroup the ants immediately if a new minimum fitness was found
	# So regrouping will happen if 
	# 1. Minimum fitness was found - we regroup to that node immediately
	# 2. After certain iterations minimum fitness was not found and we will regroup and try again
	previousFitness = originalFitness # This is the minimum fitness for now
	
	# The ants will only search till a depth equal to a ceratin fitness value
	# After that they all will be grouped to the state that gives the next minimum fitness.
	# This state will be found by any of the ants
	depth = originalFitness
	
	# This varaible is used to hold the minimum fitness found till now. Initially it will be the fitness of scramble state
	globalMinFitness = originalFitness
	globalAllMoves = scramble
	globalOrientation = cube_orientation
	globalOrientationMoves = ""
	globalAnt = 0
	
	# This flag varaible is used to break out of the loop
	solutionFoundFlag = False
	
	# This varaible is used for plotting the graph
	xIter = []
	yFitnessCurrent = []
	yFitnessGlobal = []
	
	# Parameters of alpha and beta
	alpha = al
	beta = be
		
	# Number of iterations
	start_time = time.time()	# This is were the execution begins
	for iteration in range(maxIter):
		
		# If the number of iterations has reached a ceratin depth
		# Or if we found a new minimum fitness
		if iterationsDone == depth or globalMinFitness < previousFitness:
			
			print("\n")
			print("Regrouping. ",end = " ")
			
			# We have saved the minimum fitness as a global variable
			print("Minimum fitness : ",globalMinFitness)
			print("Found by ant : ",globalAnt)
			
			# Now make sure that all the ants are in this state
			for i in range(nPop):
				
				# Change orientation of all ants
				ant_Orientation[i] = globalOrientation
				
				# Now change all of their fitnessValue
				ant_fitness[i] = globalMinFitness
				
				# Now change all of their moves
				ant_AllMoves[i] = globalAllMoves
				
				# Now change the moves applied
				ant_OrientationMoves[i] = globalOrientationMoves
			
			# Now print it
			for i in range(nPop):
				print("Ant: ", i,end=" ")
				print("Orientation : ", ant_Orientation[i], end=" ")
				print("New fitness : ",ant_fitness[i])	
				
			# Now change the depth that need to be searched again
			depth = globalMinFitness
			
			# Now change the iterations back to 0
			iterationsDone = 0			
			
			# Now change the new fitness value to beat as the current global minimum
			previousFitness = globalMinFitness
			
			# Now we are regrouping to the node that gave minimum fitness.
			# So if the node that gave the minimum fitness was found at a ceratin depth above the current one,
			# then we need to delete all the nodes that come after the minimum fitness node.
			# If not then the deposited pheromones could confuse the ants. 
			for i in range(len(pheromoneDict)):
				
				# We are going to pop elements from the end.
				# If we have found the state that gave the minimum fitness we will put it back with reinitialized pheromone value and stop.
				
				# pops element from the end.
				# This will return key value pair
				orientation_pheromone = pheromoneDict.popitem()
				
				# If the orientation is the orientation that gives minimum fitnessValue
				if orientation_pheromone[0] == globalOrientation:
					# but we need to reinitialize the pheromone values as the ants are going to start from that point.
					# so already deposited pheromone values should not confuse them.
					pheromoneDict[globalOrientation] = {"U":0.000001,"U'":0.000001,"U2":0.000001,
													   "D":0.000001,"D'":0.000001,"D2":0.000001,
													   "L":0.000001,"L'":0.000001,"L2":0.000001,
													   "R":0.000001,"R'":0.000001,"R2":0.000001,
													   "F":0.000001,"F'":0.000001,"F2":0.000001,
													   "B":0.000001,"B'":0.000001,"B2":0.000001}		
					
					# We have reinitialized, so just break out of the loop 
					break
				
				# Else continue with the process
				else:
					continue
			
			# If the reinitialized orientation is the solved state. 
			if globalOrientation == "yyyyyyyyyooooooooogggggggggwwwwwwwwwrrrrrrrrrbbbbbbbbb":
				
				# Set flag to know that solution has been found
				solutionFoundFlag = True
				
				intermediate_time = time.time()	# This is where a particle will find the solved state
				solve_time = intermediate_time - start_time # The time for a particle to find the solution
				
				# Find all the ants that found the solved state.
				arr = []
				for i in range(len(solution)):
					arr.append(solution[i][1])
				
				# Now append the solution for the other ants
				for i in range(nPop):
					
					# Append the solution if and only if that ant has not found the solved state.
					if i not in arr:
						solution.append([iteration, i, ant_Orientation[ant], ant_OrientationMoves[ant], len(solutionMoves), solve_time])	
					
					else:
						continue
					
		
		# We need to find values for plotting
		xIter.append(iteration)
		sumFitness = 0
		for i in range(len(ant_fitness)):
			sumFitness = sumFitness + ant_fitness[i]
		yFitnessCurrent.append(sumFitness/nPop)	# We are going to append the average fitness of all ants, for the iteration
		yFitnessGlobal.append(globalMinFitness)
				
		print("\n")
		print("Iteration : ",iteration)
		
		# Number of ants
		for ant in range(nPop):
			
			# Break out of number of ant loop if we have found solution
			if solutionFoundFlag == True:
				break
			
			# Print which and it is
			print("Ant : ",ant,end = " ")
			
			# Print the orientation of the ant
			print("Orientation : ",ant_Orientation[ant],end = " ")
			
			# print the current fitness
			print("Current Fitnees : ",ant_fitness[ant],end= " ")
			
			# If the ant has not reached the solved state.
			if ant_Orientation[ant] != "yyyyyyyyyooooooooogggggggggwwwwwwwwwrrrrrrrrrbbbbbbbbb":
		
				# Assign probability to each moves
				# Initially the probability values are 0 for each moves, for each ant
				# They have to calculate it based on pheromone etc
				probabilityDict = {"U":0,"U'":0,"U2":0,"D":0,"D'":0,"D2":0,"L":0,"L'":0,"L2":0,"R":0,"R'":0,"R2":0,"F":0,"F'":0,"F2":0,"B":0,"B'":0,"B2":0}
				
				# The probability for the edges for the first at is given bytearray
				# P(i,j) = (pheromone(i,j) * eta(i,j))/sum_of_all_adjacent_edges_of_ij(eta(i,j)*pheromone(i,j))
				# We will assume that before the first ant there was an ant that travelled through all the edges of the tree and spread pheromone of unit 1
				
				# Now take all the possible moves
				for m in range(len(legal_moves)):
					
					# Apply that move to the cube
					properScramble = convert2Scramble(ant_AllMoves[ant] + legal_moves[m] + " ")
					
					# Find the length of the scramble
					noofMmoves = len(properScramble)	
					
					# Make that scramble and get the orientation
					scramble, cube_orientation = Scramble.scramble(True, properScramble, noofMmoves)
					
					# Now find the fitness value for the cube orientation
					fitnessValue = fit.fitness(cube_orientation)
					
					# Now the eta value in the numberator is (quality of edge = 1/Lk i.e inverse of the distance)
					# If we have gone through this node then take the deposited pheromone value
					if cube_orientation in pheromoneDict:
						pheromoneValue = pheromoneDict[cube_orientation][legal_moves[m]]
					# Else if this is the first time, then pheromone value is 0.000001
					else:
						pheromoneValue = 0.000001
					etaNumerator = (pheromoneValue**alpha) * ((1/fitnessValue)**beta)
					
					#print("\n")
					#print("Move : ",legal_moves[m], end = " ")
					#print("Fitnees : ", fitnessValue,end = " ")
					#print("Eta : ",etaNumerator)
					
					# Now we need to find the find the fitness of all the edges connected to the current edge.
					# Then only we can find the eta value of denominator
					
					etaDenominator = 0
					
					# Now take all the adjacent edges
					for n in range(len(legal_moves)):
						
						# Apply that move to the cube
																			#First move		 # Adjacent moves
						properScramble = convert2Scramble(ant_AllMoves[ant] + legal_moves[m] + legal_moves[n] + " ")
						
						# Find the length of the scramble
						noofMmoves = len(properScramble)	
						
						# Make that scramble and get the orientation
						scramble, cube_orientation = Scramble.scramble(True, properScramble, noofMmoves)
						
						# Now find the fitness value for the cube orientation
						fitnessValue = fit.fitness(cube_orientation)
						
						# Now the eta value in the numberator is (quality of edge = 1/Lk i.e inverse of the distance)
						# Now the eta value in the numberator is (quality of edge = 1/Lk i.e inverse of the distance)
						# If we have gone through this node then take the deposited pheromone value
						if cube_orientation in pheromoneDict:
							pheromoneValue = pheromoneDict[cube_orientation][legal_moves[m]]
						# Else if this is the first time, then pheromone value is 0.000001
						else:
							pheromoneValue = 0.000001
						eta = (pheromoneValue**alpha) * ((1/fitnessValue)**beta)
						
						# Now to get the denominator value we need to sum up the values in the denomintor
						etaDenominator = etaDenominator + eta
						
						#print("\n")
						#print("Move : ",legal_moves[n], end = " ")
						#print("Fitnees : ", fitnessValue,end = " ")
						#print("Eta : ",eta,end = " ")
						#print("Eta Denominator : ", etaDenominator)
					
					# Now find the probability of an edge
					probability = (etaNumerator/etaDenominator)
					
					# Now assign probability value to the edge in the probability dictionary
					probabilityDict[legal_moves[m]] = probability
					
					#print("\n")
					#print("Move : ",legal_moves[m])
					#print("Probability : ",probability)
					#print(probabilityDict)
				
				# Now print the probability dictionary for the ant
				#print(probabilityDict)
				
				# This probability distribution won't add up to 1.
				# So we need to take all of the probability and divide them by the sum
				sum = 0
				for i in probabilityDict: 
					sum = sum + probabilityDict[i] 
				#print("Sum : ",sum)
				
				# Divide each probability distribution by the sum
				for i in probabilityDict:
					probabilityDict[i] = probabilityDict[i]/sum
					
				# Now print the probability dictionary for the ant
				#print("\n")
				#print(probabilityDict)
				
				# Now make sure that the sum is 1
				#sum = 0
				#for i in probabilityDict: 
				#	sum = sum + probabilityDict[i] 
				#print("Sum : ",sum)
				
				# Now we need to sort the probability dictionary in ascending order

				# This will sort the dictionary, but it will return a list of tuple [(),(),..]
				dict = sorted(probabilityDict.items(), key=lambda x: x[1])   
				
				# So we need to convert the list of tuples back into a dictionary
				probabilityDict = {}
				for key,value in dict:
					probabilityDict[key] = value
				
				# Now we have got back our dictionary with the values sorted
				#print("\n")
				#print(probabilityDict)
				
				# Now we need to find the cumulative sum
				# We need to create a dictionary to hold the move and the cumulative distribution
				cumulativeDict = {}
				cumSum = 0
				for key,value in probabilityDict.items():
					cumSum = cumSum + value
					cumulativeDict[key] = cumSum
				
				#print("\n")
				#print(cumulativeDict)						
				
				# Now we need to select a random number
				number = random.random()
				#print("\n")
				#print("Random Number : ",number)
				
				# Now we need to find where the random number lands
				move = ""
				for key, value in cumulativeDict.items():
					# If the number generated is less than or equal to the value, we have got the required move.
					# After that just break out of the loop.
					if number <= value:
						move = key
						break
				
				# Print move applied
				print("Move : ",move, end = " ")
				
				# Now save the move applied by the ant
				ant_OrientationMoves[ant] = ant_OrientationMoves[ant] + move + " "
				
				# Now apply the move to the cube
				properScramble = convert2Scramble(ant_AllMoves[ant] + move + " ")
				
				# Find the length of the scramble
				noofMmoves = len(properScramble)	
				
				# Make that scramble and get the orientation
				scramble, cube_orientation = Scramble.scramble(True, properScramble, noofMmoves)
				
				# Now find the fitness value and save it
				fitnessValue = fit.fitness(cube_orientation)
				print("New Fitnees : ",fitnessValue,end=" ")
				ant_fitness[ant] = fitnessValue
				
				# The ant has selected the path
				# It will deposite pheromone value = 1/Lk
				pheromoneDict[ant_Orientation[ant]][move] = pheromoneDict[ant_Orientation[ant]][move] + 1/(fitnessValue)
				
				# Now save the orientation
				ant_Orientation[ant] = cube_orientation
				
				# Now save the move applied
				ant_AllMoves[ant] = scramble
				
				# Print pheromone
				#print("\n")
				#print(pheromoneDict)
				
				# Now if this is a new state that has not been reached by the ants, add it to the pheromone matrix dictionary.
				if ant_Orientation[ant] not in pheromoneDict.keys():
					pheromoneDict[ant_Orientation[ant]] = {"U":0.000001,"U'":0.000001,"U2":0.000001,
														   "D":0.000001,"D'":0.000001,"D2":0.000001,
														   "L":0.000001,"L'":0.000001,"L2":0.000001,
														   "R":0.000001,"R'":0.000001,"R2":0.000001,
														   "F":0.000001,"F'":0.000001,"F2":0.000001,
														   "B":0.000001,"B'":0.000001,"B2":0.000001}
				print("Pheromone dictionary : ",len(pheromoneDict))
				
				# Now check if this ant has found the global minimum.
				# If so then change all of the global values
				if ant_fitness[ant] < globalMinFitness:
					globalMinFitness = ant_fitness[ant]
					globalAllMoves = ant_AllMoves[ant]
					globalOrientation = ant_Orientation[ant]
					globalOrientationMoves = ant_OrientationMoves[ant]
					globalAnt = ant
				
				# If the cube is solved
				if ant_Orientation[ant] == "yyyyyyyyyooooooooogggggggggwwwwwwwwwrrrrrrrrrbbbbbbbbb":
					
					# Find the length of the solution
					# The moves applied is a string. So split it by space and remove the last character as it is a space.
					# This is needed to find the length of the solution. 
					# If it was a string then it would count the spaces.
					solutionMoves = ant_OrientationMoves[ant].split(" ")[:-1]

					intermediate_time = time.time()	# This is where a particle will find the solved state
					solve_time = intermediate_time - start_time # The time for a particle to find the solution
					
					# Iteration, ant, orientation, solution, solution length, time
					solution.append([iteration, ant, ant_Orientation[ant], ant_OrientationMoves[ant], len(solutionMoves), solve_time])	

					# If the ant has found the solution then we need to change the global minimum
					globalMinFitness = ant_fitness[ant]
					globalAllMoves = ant_AllMoves[ant]
					globalOrientation = ant_Orientation[ant]
					globalOrientationMoves = ant_OrientationMoves[ant]
					globalAnt = ant
		
		# Increment the depth searched by the ant.
		iterationsDone += 1
		
		# Break out of the iteration loop
		if solutionFoundFlag == True:
			break		
	
	end_time = time.time()	# This is where the entire PSO loop finishes execution
	total_time = end_time - start_time	# This is the total time needed for the loop execution
	
	# Print the initial cube orientation
	print("\n")
	print("Cube orientation: Yellow on top and green on front.")
	print("Reading order goes: Up, Right, Front, Down, Left, Back.")
	print("Scramble: ", originalScramble)
	print("Initial cube orientation : ",initialOrientation)
	
	# Print the solution vector
	for sol in solution:
		print("\n")
		print("Iteration : ",sol[0])
		print("Ant : ",sol[1])
		print("Orientation : ", sol[2])
		print("Solution : ",sol[3])
		print("Length : ",sol[4])
		print("Time : ",sol[5])
	
	# If the solution was not found print the appropriate information
	if len(solution)==0:
		print("\n")
		print("Solution was not found by any ant")
		print("The total number of ants that found solution: ",len(solution),"/",nPop)	# 0 particles solved it
		print("Original Solution Length: ", originalFitness)
		print("Average solution length: NIL")	# Since the solution was not found	
		print("Iteration at which the first solution was found: NIL")	# Since the solution was not found
		print("Iteration at which the last ant found the solution: NIL")	# Since the solution was not found
		print("Average iterations it takes for the next ant to reach solved state: NIL")	# Since the solution was not found
		print("Total time for loop execution : ",total_time)
	
	# Else if the solution was found
	else:
		# Print the details:
		# Find the average length of the solution
		print("\n")
		sumSol = 0
		for sol in solution:
			sumSol = sumSol + sol[4]
					
		averageSol = sumSol/len(solution)
		
		print("The total number of ants that found solution: ",len(solution),"/",nPop)
		print("Original Solution Length: ", originalFitness)
		print("Average solution length: ", averageSol)	
		
		# Find the average iteration and time it takes for the next particle to reach the solved state
		sumIter = 0
		sumIterTime = 0
		for i in range(len(solution)):
			if (i+1) >= len(solution):
				break
			else:
				sumIter = sumIter + (solution[i+1][0]-solution[i][0])
				sumIterTime = sumIterTime + (solution[i+1][5]-solution[i][5])
		
		averageIter = sumIter/len(solution)
		averageIterTime = sumIterTime/len(solution)
		
		
		# The minimum iteration at which the solution was found and also the maximum iteration	
		print("Iteration at which the first solution was found: ",solution[0][0])		
		print("Iteration at which the last ant found the solution: ", solution[-1][0])
		print("Average iterations it takes for the next ant to reach solved state: ",averageIter)
		print("\n")
		print("Time required to find the first solution : ",solution[0][5],"seconds")	# At the fifth index of the solution vector the time is stored
		print("Total time for ACO loop execution: ", solution[-1][5],"seconds")
		print("Average time it takes for the next ant to reach solved state: ",averageIterTime, "seconds")
	
	# Plotting the change of personal best with each iteration for particle
	plt.grid(True)
	plt.plot(xIter,yFitnessGlobal,c="blue",linestyle="--",marker="o")
	plt.plot(xIter,yFitnessCurrent,c="red",linestyle=':')	# Plot iteration vs fitness
	
	plt.xlabel('Iterations')	# naming the x axis as iterations
	plt.ylabel('Fitness Score')	# naming the y axis as fitness score	
	plt.title('Iterations vs Fitness')	# giving a title to my graph 
	plt.legend(["Global Fitness","Current Fitnees Average","Regrouping Points"]) 	
	plt.show()
	
	
# Main program
if __name__ == "__main__":
	print("\n")
	print("Ant Colony Optimization")
	iterations = int(input("Enter the number of iterations : "))
	ants = int(input("Enter the number of ants : "))
	al = int(input("Enter the parameter alpha : "))
	be = int(input("Enter the parameter beta : "))
	randomOrManual = input("Type M for manual scramble or R for random scrabmle : ")
	if randomOrManual == "R":
		flag = False
		scramble = ""
	elif randomOrManual == "M":
		flag = True
		scramble = input("Type scramble : ")
		
	# Function call
	# Add space to the scramble entered by the user, implementation reason.
	ACO(iterations, ants, al, be, flag, scramble+" ")	# Calling the ACO algorithm