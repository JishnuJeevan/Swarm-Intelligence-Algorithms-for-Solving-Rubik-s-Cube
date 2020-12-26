"""
Code taken from: https://github.com/BenGotts/Python-Rubiks-Cube-Scrambler
"""

# Orientation of the cube i.e. yellow on top and red on front.
# This is the only orientation that Kociemba will accept to evaluate the fitness function.
# U R F D L B
# [y]ellow = [U]P, [o]range = [R]ight, [g]reen = [F]ront, [w]hite = [D]own, [r]ed = [L]eft, [b]lue = [B]ack 
cube = [
		['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y'], 
		['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'], 
		['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'], 
		['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], 
		['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']		
		]

def faceMove(x):
    temp = cube[x][0]
    cube[x][0] = cube[x][6]
    cube[x][6] = cube[x][4]
    cube[x][4] = cube[x][2]
    cube[x][2] = temp

    temp = cube[x][1]
    cube[x][1] = cube[x][7]
    cube[x][7] = cube[x][5]
    cube[x][5] = cube[x][3]
    cube[x][3] = temp
    return

def faceMovePrime(x):
    temp = cube[x][0]
    cube[x][0] = cube[x][2]
    cube[x][2] = cube[x][4]
    cube[x][4] = cube[x][6]
    cube[x][6] = temp

    temp = cube[x][1]
    cube[x][1] = cube[x][3]
    cube[x][3] = cube[x][5]
    cube[x][5] = cube[x][7]
    cube[x][7] = temp
    return

def uMove(move):
    if(move == "U"):
        faceMove(0)

        temp = cube[1][0]
        cube[1][0] = cube[2][0]
        cube[2][0] = cube[3][0]
        cube[3][0] = cube[4][0]
        cube[4][0] = temp

        temp = cube[1][1]
        cube[1][1] = cube[2][1]
        cube[2][1] = cube[3][1]
        cube[3][1] = cube[4][1]
        cube[4][1] = temp

        temp = cube[1][2]
        cube[1][2] = cube[2][2]
        cube[2][2] = cube[3][2]
        cube[3][2] = cube[4][2]
        cube[4][2] = temp
    elif(move == "U'"):
        faceMovePrime(0)

        temp = cube[1][0]
        cube[1][0] = cube[4][0]
        cube[4][0] = cube[3][0]
        cube[3][0] = cube[2][0]
        cube[2][0] = temp

        temp = cube[1][1]
        cube[1][1] = cube[4][1]
        cube[4][1] = cube[3][1]
        cube[3][1] = cube[2][1]
        cube[2][1] = temp

        temp = cube[1][2]
        cube[1][2] = cube[4][2]
        cube[4][2] = cube[3][2]
        cube[3][2] = cube[2][2]
        cube[2][2] = temp
    elif(move == "U2"):
        uMove("U")
        uMove("U")
    return

def dMove(move):
    if(move == "D"):
        faceMove(5)

        temp = cube[1][6]
        cube[1][6] = cube[4][6]
        cube[4][6] = cube[3][6]
        cube[3][6] = cube[2][6]
        cube[2][6] = temp

        temp = cube[1][5]
        cube[1][5] = cube[4][5]
        cube[4][5] = cube[3][5]
        cube[3][5] = cube[2][5]
        cube[2][5] = temp

        temp = cube[1][4]
        cube[1][4] = cube[4][4]
        cube[4][4] = cube[3][4]
        cube[3][4] = cube[2][4]
        cube[2][4] = temp
        return
    elif(move == "D'"):
        faceMovePrime(5)

        temp = cube[1][6]
        cube[1][6] = cube[2][6]
        cube[2][6] = cube[3][6]
        cube[3][6] = cube[4][6]
        cube[4][6] = temp

        temp = cube[1][5]
        cube[1][5] = cube[2][5]
        cube[2][5] = cube[3][5]
        cube[3][5] = cube[4][5]
        cube[4][5] = temp

        temp = cube[1][4]
        cube[1][4] = cube[2][4]
        cube[2][4] = cube[3][4]
        cube[3][4] = cube[4][4]
        cube[4][4] = temp
        return
    elif(move == "D2"):
        dMove("D")
        dMove("D")
    return

def rMove(move):
    if(move == "R"):
        faceMove(3)

        temp = cube[0][4]
        cube[0][4] = cube[2][4]
        cube[2][4] = cube[5][4]
        cube[5][4] = cube[4][0]
        cube[4][0] = temp

        temp = cube[0][3]
        cube[0][3] = cube[2][3]
        cube[2][3] = cube[5][3]
        cube[5][3] = cube[4][7]
        cube[4][7] = temp

        temp = cube[0][2]
        cube[0][2] = cube[2][2]
        cube[2][2] = cube[5][2]
        cube[5][2] = cube[4][6]
        cube[4][6] = temp
        return
    elif(move == "R'"):
        faceMovePrime(3)

        temp = cube[0][4]
        cube[0][4] = cube[4][0]
        cube[4][0] = cube[5][4]
        cube[5][4] = cube[2][4]
        cube[2][4] = temp

        temp = cube[0][3]
        cube[0][3] = cube[4][7]
        cube[4][7] = cube[5][3]
        cube[5][3] = cube[2][3]
        cube[2][3] = temp

        temp = cube[0][2]
        cube[0][2] = cube[4][6]
        cube[4][6] = cube[5][2]
        cube[5][2] = cube[2][2]
        cube[2][2] = temp
        return
    elif(move == "R2"):
        rMove("R")
        rMove("R")
    return

def lMove(move):
    if(move == "L"):
        faceMove(1)

        temp = cube[0][0]
        cube[0][0] = cube[4][4]
        cube[4][4] = cube[5][0]
        cube[5][0] = cube[2][0]
        cube[2][0] = temp

        temp = cube[0][7]
        cube[0][7] = cube[4][3]
        cube[4][3] = cube[5][7]
        cube[5][7] = cube[2][7]
        cube[2][7] = temp

        temp = cube[0][6]
        cube[0][6] = cube[4][2]
        cube[4][2] = cube[5][6]
        cube[5][6] = cube[2][6]
        cube[2][6] = temp
        return
    elif(move == "L'"):
        faceMovePrime(1)

        temp = cube[0][0]
        cube[0][0] = cube[2][0]
        cube[2][0] = cube[5][0]
        cube[5][0] = cube[4][4]
        cube[4][4] = temp

        temp = cube[0][7]
        cube[0][7] = cube[2][7]
        cube[2][7] = cube[5][7]
        cube[5][7] = cube[4][3]
        cube[4][3] = temp

        temp = cube[0][6]
        cube[0][6] = cube[2][6]
        cube[2][6] = cube[5][6]
        cube[5][6] = cube[4][2]
        cube[4][2] = temp
        return
    elif(move == "L2"):
        lMove("L")
        lMove("L")
    return

def fMove(move):
    if(move == "F"):
        faceMove(2)

        temp = cube[0][6]
        cube[0][6] = cube[1][4]
        cube[1][4] = cube[5][2]
        cube[5][2] = cube[3][0]
        cube[3][0] = temp

        temp = cube[0][5]
        cube[0][5] = cube[1][3]
        cube[1][3] = cube[5][1]
        cube[5][1] = cube[3][7]
        cube[3][7] = temp

        temp = cube[0][4]
        cube[0][4] = cube[1][2]
        cube[1][2] = cube[5][0]
        cube[5][0] = cube[3][6]
        cube[3][6] = temp
        return
    elif(move == "F'"):
        faceMovePrime(2)

        temp = cube[0][6]
        cube[0][6] = cube[3][0]
        cube[3][0] = cube[5][2]
        cube[5][2] = cube[1][4]
        cube[1][4] = temp

        temp = cube[0][5]
        cube[0][5] = cube[3][7]
        cube[3][7] = cube[5][1]
        cube[5][1] = cube[1][3]
        cube[1][3] = temp

        temp = cube[0][4]
        cube[0][4] = cube[3][6]
        cube[3][6] = cube[5][0]
        cube[5][0] = cube[1][2]
        cube[1][2] = temp
        return
    elif(move == "F2"):
        fMove("F")
        fMove("F")
    return

def bMove(move):
    if(move == "B"):
        faceMove(4)

        temp = cube[0][2]
        cube[0][2] = cube[3][4]
        cube[3][4] = cube[5][6]
        cube[5][6] = cube[1][0]
        cube[1][0] = temp

        temp = cube[0][1]
        cube[0][1] = cube[3][3]
        cube[3][3] = cube[5][5]
        cube[5][5] = cube[1][7]
        cube[1][7] = temp

        temp = cube[0][0]
        cube[0][0] = cube[3][2]
        cube[3][2] = cube[5][4]
        cube[5][4] = cube[1][6]
        cube[1][6] = temp
        return
    elif(move == "B'"):
        faceMovePrime(4)

        temp = cube[0][2]
        cube[0][2] = cube[1][0]
        cube[1][0] = cube[5][6]
        cube[5][6] = cube[3][4]
        cube[3][4] = temp

        temp = cube[0][1]
        cube[0][1] = cube[1][7]
        cube[1][7] = cube[5][5]
        cube[5][5] = cube[3][3]
        cube[3][3] = temp

        temp = cube[0][0]
        cube[0][0] = cube[1][6]
        cube[1][6] = cube[5][4]
        cube[5][4] = cube[3][2]
        cube[3][2] = temp
        return
    elif(move == "B2"):
        bMove("B")
        bMove("B")
    return

def scramble(scr, len):
	# Reintialize the cube orientation.
	# Global variables will only be initialized once so every time a scramble is made it will affect the same position.
	# So we need to re initalize it so that the moves made b one particle don't affect the orientation for a different particle.
	global cube
	cube = [
		['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y'], 
		['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'], 
		['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'], 
		['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], 
		['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']		
		]
	x=0
	for x in range(len):
		if(scr[x][0] == "U"):
			uMove(scr[x][0]+scr[x][1])
		elif(scr[x][0] == "D"):
			dMove(scr[x][0]+scr[x][1])
		elif(scr[x][0] == "R"):
			rMove(scr[x][0]+scr[x][1])
		elif(scr[x][0] == "L"):
			lMove(scr[x][0]+scr[x][1])
		elif(scr[x][0] == "F"):
			fMove(scr[x][0]+scr[x][1])
		elif(scr[x][0] == "B"):
			bMove(scr[x][0]+scr[x][1])

	"""
	print(                               "    " + cube[0][0] + cube[0][1] + cube[0][2] + "\n" +
										 "    " + cube[0][7] + "y" + cube[0][3] + "\n" +
										 "    " + cube[0][6] + cube[0][5] + cube[0][4] + "\n\n" +
	cube[1][0] + cube[1][1] + cube[1][2] + " " + cube[2][0] + cube[2][1] + cube[2][2] + " " + cube[3][0] + cube[3][1] + cube[3][2] + " " + cube[4][0] + cube[4][1] + cube[4][2] + "\n" +
	cube[1][7] + "r" + cube[1][3] + " " + cube[2][7] + "g" + cube[2][3] + " " + cube[3][7] + "o" + cube[3][3] + " " + cube[4][7] + "b" + cube[4][3] + "\n" +
	cube[1][6] + cube[1][5] + cube[1][4] + " " + cube[2][6] + cube[2][5] + cube[2][4] + " " + cube[3][6] + cube[3][5] + cube[3][4] + " " + cube[4][6] + cube[4][5] + cube[4][4] + "\n\n" +
										 "    " + cube[5][0] + cube[5][1] + cube[5][2] + "\n" +
										 "    " + cube[5][7] + "w" + cube[5][3] + "\n" +
										 "    " + cube[5][6] + cube[5][5] + cube[5][4] + "\n")  
	"""
	return cube