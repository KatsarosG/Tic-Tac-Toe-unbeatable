humanSymbol = 'X'
if humanSymbol == 'X':
    cpuSymbol = 'O'
else:
    cpuSymbol = 'X'

def place(to, symbol, board):
    board[to] = symbol

def remove(From, board):
    board[From] = '-'

def showBoard(board):
    for i in range(len(board)):
        print(board[i] , end=" " , flush=True)
        if (i+1)%3 == 0:
            print(' ') 

def humanMove():
    tempMove = -1
    moveDone = False
    while not moveDone:
        showBoard(gameBoard)
        tempMove = int(input('Make a move (1-9) : '))
        
        #for numpad:
        if tempMove == 1:
            tempMove = 7
        elif tempMove == 2:
            tempMove = 8
        elif tempMove == 3:
            tempMove = 9
        elif tempMove == 7:
            tempMove = 1
        elif tempMove == 8:
            tempMove = 2
        elif tempMove == 9:
            tempMove = 3
        
        place(tempMove-1, humanSymbol, gameBoard)
        moveDone = True

def getState(symbol, board):
    winCombs = [[0,1,2], [3,4,5], [6,7,8], 
               [0,3,6], [1,4,7], [2,5,8], 
               [0,4,8], [2,4,6]]
    Os = []
    Xs = []
    for i in range(len(board)):
        if board[i] == 'X':
            Xs.append(i)
        elif board[i] == 'O':
            Os.append(i) 

    a = 0
    for i in winCombs:
        if all(elem in Os for elem in i):
            if symbol == 'O':
                return(1)
            else:
                return(-1)
            a += 1        
        elif all(elem in Xs for elem in i):
            if symbol == 'X':
                return(1)
            else:
                return(-1)
            a += 1        
    if a == 0:
        if '-' not in board:
            return(0)
        else:
            #unfinished
            return(2)

def getBestMove(symbol, board):
    #          move,score
    returns = [-1, -2]

    def copyBoard(board):
        copy = []
        for i in board:
            copy.append(i)
        return(copy)

    def findClear(board):
        clear = []
        for i in range(len(board)):
            if board[i] == '-':
                clear.append(i)
        return(clear)
    
    clear = findClear(board)
    clearAndScores = []

    if len(clear)> 0:
        for i in range(9):
            clearAndScores.append('a')
            
    for i in range(len(clear)):
        move = clear[i]
        newBoard = copyBoard(board)
        place(move, symbol, newBoard)
        result = getState(symbol, newBoard)
        score = 'a'

        if result == 0:
            score = 0
        elif result == 1:
            score = 1
        elif result == 2:
            if symbol == 'X':
                otherSymbol = 'O'
            else:
                otherSymbol = 'X'
            nextMove = getBestMove(otherSymbol, newBoard) 
            score = -(nextMove[1])

        if score == 1:
            return([move, 1])
        
        returns =  [move,score]
        clearAndScores[move] = score

    firstToDo = []
    secToDo = []
    lastToDo = []
    for i in range(len(clearAndScores)):
        if clearAndScores[i] == 1:
            firstToDo.append(i)
        elif clearAndScores[i] == 0:
            secToDo.append(i)
        elif clearAndScores[i] == -1:
            lastToDo.append(i)
    
    if len(firstToDo) > 0:
        returns[0] = firstToDo[0]
        returns[1] = 1
    elif len(secToDo) > 0:
        returns[0] = secToDo[0]
        returns[1] = 0
    elif len(lastToDo) > 0:
        returns[0] = lastToDo[0]
        returns[1] = -1

    return(returns)

def cpuMove():
    move = getBestMove(cpuSymbol, gameBoard)
    move = move[0]
    place(move, cpuSymbol, gameBoard)

def stop():
    if getState('O',gameBoard) == 1 or getState('O',gameBoard) == -1  or  getState('O',gameBoard) == 0:
        return(True)

#main 
while True:
    gameBoard = ['-','-','-',
                 '-','-','-',
                 '-','-','-']

    firstMove = int(input('Who plays first? (CPU:1/HUMAN:2): '))
    humanSymbol = str(input('Player symbol? (X/O): '))

    if humanSymbol == 'X':
        cpuSymbol = 'O'
    else:
        cpuSymbol = 'X'  

    while not stop():
        if firstMove == 1:
            cpuMove()
            if not stop():
                humanMove()
        else:
            humanMove()
            if not stop():
                cpuMove()
    showBoard(gameBoard)
    print('=======================')