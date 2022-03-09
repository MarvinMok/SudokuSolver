from collections import deque
from types import MappingProxyType
from copy import copy
global moveDict
global moveSetDict
global solution 
solution = 2 ** 324 - 1

def printboard(board):

    for row in board:
        for ele in row:
            print(ele, end=" ")
        print()


    


def DLX():

    ''' for 729 possible moves, each columnn represents the board as 4 constraint sets with 81 bits of info, 81*4 = 324
    bits are number-row, row-col, number-box, number-col
    0 - 80 r-c
    81 - 161 n-r
    162 - 242 n-c
    243 - 323 n-b

    Thus, each move is represented by 4 bits. Therefore:
        - by keeping a dictionary or list of every move (0-729), we know which moves we
            can remove immediately duringn reduction
        - the maximum recursion depth is 81 = 324 bits per move / 4 bits per move, or the 81 - numberOfClues
            - makes sense as thats the maximum amount of moves we can make
        -



    Valid solution is when XOR solution set of moves is 2^325-1


    Psuedocode:

    def DLX(matrix, S):
    
        bestCol = column with least amount of Trues

        basecases:
            if matrix has no columns
                return S, True

            if bestCol has 0 Trues
                return S, False
        

        for matrix[randomRow][bestCol] in numRow: // for all possible moves to fill in our constraint (bestCol)
            newmatrix = matrix
            if matrix[randomRow][bestCol] is True: // if this move is possible
                Reduce newmatrix
                result = DLX(newmatrix, S + randomRow)
                if result[1] is True: // solution
                    return result
                else:
                    continue

        


        #Reduction algorithm
        newmatrix = matrix
        for matrix[randomRow][col] in numCol:
            if matrix[randomRow][col] is True: // For each column j such that A(r, j) == 1,
                for matrix [row][col] in numRow:
                    if matrix [row][col] is True: // for each row i such that A(i, j) == 1,
                        remove row from newmatrix
            remove col from newmatrix
        
        #Reduction improved
        given Dictionary D, which has 729 keys= row ; value= set of rows to remove
        remove rows in D[row]
        D is always the same after we reduce the originanl 729 x 324 by the givens


    Data structures, ideas, and stuff

    - Reduction alg improved only works when we store S XOR
        - This is for finding BestCol -- we dont check columns where S XOR = 1
    - S is deque, so before every DLX we push, and after we pop
    - Matrix is best used as a set of integers
        - integers is obv as its a mask, also better for set
        - set is useful for Reduction
            - Since each row is an int, each key for Dictionary D1 can just be that int instead of
                an index. 
            - Furthermore, we can do set subtraction for fast removal
    - to find bestCol:
        - we store a dictionary for each column where key=col, value=numbers of ones
        - we iterate through the dictionary to find the best column:
            - use S XOR to ensure this col has not been removed
            - instantly cut branch if column = 0 (no possible)
            - instantly add set to S if column = 1 (naked or hidden singles)
            - valuable for heuristics / pruning later
            - faster than iterating through entire matrix everytime
                - instead, during reduction, we iterate through each number and subtract 1 (we will store the indices where it has a one)
                    after DLX we add back
                - Thus we have a second dictionary D2 where key:row, value:indices
                    - we could also combine this with D1 since they have the same key


7 2 0 0 9 6 0 0 3 
0 0 0 2 0 5 0 0 0 
0 8 0 0 0 4 0 2 0 
0 0 0 0 0 0 0 6 0 
1 0 6 5 0 3 8 0 7 
0 4 0 0 0 0 0 0 0 
0 3 0 8 0 0 0 9 0 
0 0 0 7 0 2 0 0 0 
2 0 0 4 3 0 0 1 8 


7 2 5 1 9 6 4 8 3 
4 6 3 2 8 5 9 7 1 
9 8 1 3 7 4 5 2 6 
3 7 2 9 4 8 1 6 5 
1 9 6 5 2 3 8 4 7 
5 4 8 6 1 7 2 3 9 
6 3 4 8 5 1 7 9 2 
8 1 9 7 6 2 3 5 4 
2 5 7 4 3 9 6 1 8 
    
    '''
    global moveDict
    global moveSetDict
    matrix = [[None for i in range(324)] for j in range(729)]

    #convert str to 2d matrix
    board = [[None for j in range(0, 9)] for i in range(0, 9)] 
    a = '800000000003600000070090200050007000000045700000100030001000068008500010090000400'
    #
    for i in range(0,9):
        for j in range(0,9):
            board[i][j] = int(a[i * 9 + j])

    #convert 2d matrix to incidence matrix
    '''
    0 - 80 r-c
    81 - 161 n-r
    162 - 242 n-c
    243 - 323 n-b
    '''
    matrix = 0
    S = deque()
    SXOR = 0
    for row in range(9):
        for col in range(9):
            matrix = 0
            value = board[row][col]
            box  = row // 3 * 3 + col // 3
            if value != 0:
                matrix = 1 << row * 9 + col ^ 1 << 81 + (value - 1) * 9 + row ^ 1 << 81 * 2 + (value - 1) * 9 + col ^ 1 << 81 * 3 + (value - 1) * 9 + box
                S.append(matrix)
                SXOR = SXOR ^ matrix
    incidenceMatrix = createIncidence(board)
    moveDict = createDictionary(incidenceMatrix)
    moveSetDict = ColtoRowDict(incidenceMatrix)

    newIM = copy(incidenceMatrix)
    for given in S:
        for i in range(324):
            if given >> i & 1:
                for move in incidenceMatrix:
                    if move >> i & 1:
                        newIM.discard(move)
    incidenceMatrix = newIM

    
    
    printboard(subsetToBoard(S))

    #reduce by matrix

    #print(incidenceMatrix)
    #print(moveDict)

    bestColDict = createBestColDict(incidenceMatrix)

    print()
    #print(bestColDict)

    return DLXhelper(incidenceMatrix, S, SXOR, bestColDict)




def DLXhelper(incidenceM, S, SXOR, bestColDict):
    
    #basecase

    if SXOR == solution:
        return True, S

    minCol = -1
    min1s = 100
    for col, value in bestColDict.items():
        if not SXOR >> col & 1:
            if value == 0: 
                return (False, 1)
            elif value < min1s:
                min1s = value
                minCol = col

    for move in moveSetDict[minCol]:
        if move in incidenceM:
            S.append(move)
            #print(minCol)

            indices = moveDict[move][0]
            for i in indices:
                bestColDict[i] -= 1

            #printboard(subsetToBoard(S))

            #print()

            result = DLXhelper(incidenceM - moveDict[move][1], S, SXOR ^ move, bestColDict)

            if result[0]:
                return True, S

            S.pop()
            for i in indices:
                bestColDict[i] += 1

    return (False, 2)



    
def createBestColDict(incidenceM):
    d = {}
    for i in range(324):
        t = 0
        moveSet = set()
        for move in incidenceM:
            if move >> i & 1:
                t += 1
                moveSet.add(move)

        d[i] = t

    return d


def ColtoRowDict(incidenceM):
    d = {}
    
    for i in range(324):
        t = set()
        for move in incidenceM:
            if move >> i & 1:
                t.add(move)
        d[i] = t
    return MappingProxyType(d)

def createIncidence(board):
    incidenceM = set()

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for value in range(9):
                    box  = row // 3 * 3 + col // 3
                    temp = 1 << row * 9 + col | 1 << 81 + value * 9 + row | 1 << 81 * 2 + value * 9 + col | 1 << 81 * 3 + value * 9 + box
                    incidenceM.add(temp)

    return incidenceM 


def subsetToBoard(S):
    board = [[0 for j in range(0, 9)] for i in range(0, 9)]
    x = 0
    for row in range(9):
        for col in range(9):
            for move in S:
                if move >> row * 9 + col & 1:
                    for num in range(9):
                        box  = row // 3 * 3 + col // 3
                        if  move >> 81 * 1 + num * 9 + row & 1 :    
                            board[row][col] = num + 1
                            break
    return board




def createDictionary(incidenceM):
    d1 = {}

    for move in incidenceM:
        indices = []
        for i in range(324):
            if move >> i & 1:
                indices.append(i)
        d1[move] = tuple(indices)


    d2 = {}

    for mainMove in incidenceM:
        toRemove = set()
        for movesToRemove in incidenceM:
            for i in d1[mainMove]:
                if movesToRemove >> i & 1:
                    toRemove.add(movesToRemove)

        d2[mainMove] = frozenset(toRemove)

    return MappingProxyType({ move : (d1[move], d2[move]) for move in incidenceM})

if __name__ == "__main__":
    y = 0

    board = [[None for j in range(0, 9)] for i in range(0, 9)] 
    a = '720096003000205000080004020000000060106503807040000000030800090000702000200430018'
    for i in range(0,9):
        for j in range(0,9):
            board[i][j] = int(a[i * 9 + j])
            if int(a[i * 9 + j]) != 0:
                y+= 1
    print(y)
    matrix = 0
    t= []
    for row in range(9):
        for col in range(9):
            matrix = 0
            value = board[row][col]
            box  = row // 3 * 3 + col // 3
            if value != 0:
                matrix = 1 << row * 9 + col ^ 1 << 81 + (value - 1) * 9 + row ^ 1 << 81 * 2 + (value - 1) * 9 + col ^ 1 << 81 * 3 + (value - 1) * 9 + box
                t.append(matrix)
    #print(matrix)
    #printboard(subsetToBoard(t))
    #print()
    printboard(board)
    print()
    a = DLX();
    print(a)
    printboard(subsetToBoard(a[1]))








