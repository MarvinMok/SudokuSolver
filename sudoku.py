import threading
import multiprocessing
global y


'''def solveSudokuHelper3(board):
	t = None
	if isSol(board):
		return board
	else:
		zeros = find0(board)
		if not zeros:
			return
		else:
			i = zeros[0]
			j = zeros[1]
			for x in range(1,10):
				if isValid(i,j,x,board) is True:
					board[i][j]=x
					t = solveSudokuHelper3(board) 
				if t:
					return t
				board[i][j]=0

	return t

def solveSudokuHelper2(board, i,j):
    t = None
    if i==8 and j==8:
        if board[i][j]!=0:
        	return board
        else:
            for x in range(1,10):
                if isValid(i,j,x,board) is True:
                    board[i][j]=x
                    return board
    
    elif j>8:
        t = solveSudokuHelper2(board, i+1, 0)
    
    elif board[i][j]==0:
        for x in range(1,10):
            if isValid(i,j,x,board) is True:
                board[i][j]=x
                t = solveSudokuHelper2(board, i, j+1) 
                if t:
                	return t
                board[i][j]=0
    else:
        t = solveSudokuHelper2(board, i, j+1)
    return t'''


def copyBoard(oldboard):
	newboard = [[oldboard[i][j] for j in range(0, 9)] for i in range(0, 9)] 
	return newboard

def isSol(board):
	total = 0
	for i in range(0,9):
		total += sum(board[i])
	return total == 405

def find0(board):
	for i in range(0,9):
		for j in range(0,9):
			if board[i][j] == 0:
				return i, j
	return False
def findNakedSingles():
	pass

def findHiddenSingles():
	pass

def isValid(i,j,x,board):
    #check row
    for col in range(9):
        if board[i][col] == x:
            return False
    
    #check column
    for row in range(9):
        if board[row][j] == x:
            return False
    
    #check block
    startrow = i - i % 3
    startcol= j - j % 3
    
    p = startrow
    while p <= startrow + 2:
        l = startcol
        while l <= startcol + 2:
            if board[p][l] == x:
                return False
            l += 1
        p += 1
    
    return True
def solveSudokuHelper(s, solution):
	#global y
	#y += 1
	#print(y)
	while s and solution[0] == 1:
		oldboard = s.pop()
		if isSol(oldboard):
			s = []
			print("solved")
			solution[0] = oldboard

		else:
			zeros = find0(oldboard)
			if zeros:
				i = zeros[0]
				j = zeros[1]
				for x in range(1,10):
					if isValid(i,j,x,oldboard):
						newboard = copyBoard(oldboard)
						newboard[i][j] = x
						s.append(newboard)
		#print(s)
   

def solveSudoku(startboard):

	#t = solveSudokuHelper3(startboard)
	#return t

	board = copyBoard(startboard)
	s = [board]
	solution = [1]
	done = False

	oldboard = s.pop()
	if isSol(oldboard):
		s = []
		print("solved")
		solution[0] = oldboard

	else:
		zeros = find0(oldboard)
		if zeros:
			i = zeros[0]
			j = zeros[1]
			for x in range(1,10):
				if isValid(i,j,x,oldboard):
					newboard = copyBoard(oldboard)
					newboard[i][j]=x
					s.append(newboard)
	threads = []

	for i in range(0, 2):
		threads.append(threading.Thread(target= solveSudokuHelper, args = (s, solution)))
		threads[i].start()



	while not done:
		if solution[0] != 1:
			done = True
			return solution[0]
		
		
		#print(s)
		#t1.join()
		#print(solution)
	#print(s)
		




def printboard(board):

    for row in board:
        for ele in row:
            print(ele, end=" ")
        print()


if __name__ == "__main__":
	#global y
	#y = 0
	board = [[None for j in range(0, 9)] for i in range(0, 9)] 
	a = '720096003000205000080004020000000060106503807040000000030800090000702000200430018'
	for i in range(0,9):
		for j in range(0,9):
			board[i][j] = int(a[i * 9 + j])
	t = solveSudoku(board)
	printboard(t)
	






	


	