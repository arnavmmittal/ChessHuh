
# board class that keeps track of board and each square
class Board(object):
    def __init__(self):
        # board initializing with structured letters so they are easily accessed
        self.board = [
            ['bRook', 'bKn', 'bBish', 'bQueen', 'bKing', 'bBish', 'bKn', 'bRook'],
            ['bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn'],
            ['_','_','_','_','_','_','_','_'],
            ['_','_','_','_','_','_','_','_'],
            ['_','_','_','_','_','_','_','_'],
            ['_','_','_','_','_','_','_','_'],
            ['wPawn', 'wPawn', 'wPawn','wPawn','wPawn','wPawn','wPawn','wPawn'],
            ['wRook', 'wKn', 'wBish','wQueen','wKing','wBish','wKn','wRook'],  
        ]
    
        # initialize game deciding variables
        self.gameOver = False
        self.cMate = False
        self.draw = False
        self.enPassant = ()

        # past list of moves
        self.moves = []

        self.bKing = (0,4)
        self.wKing = (7,4)

        # 0 is white, 1 is black's turn
        self.turn = 0

        # state of castle using castle class
        self.castlingState = Castle(True,True,True,True)
        self.castles = [Castle(self.castlingState.wRight, self.castlingState.bRight,
                                self.castlingState.wLeft, self.castlingState.bLeft)]

    # move piece function that allows piece to be moved
    def movePiece(self, val):
        #piece being moved becomes empty
        self.board[val.startR][val.startC] = '_'

        # place you move to becomes piece moved
        self.board[val.endR][val.endC] = val.pMove

        # add to list of moves
        self.moves.append(val) 
        
        # switch whose turn it is
        if (self.turn == 0):
            self.turn = 1
        else:
            self.turn = 0
        
        # get kings locations
        if val.pMove == 'bKing':
            self.bKing = (val.endR, val.endC)
        elif val.pMove == 'wKing':
            self.wKing = (val.endR, val.endC)

        # promotion
        if val.promote:
            self.board[val.endR][val.endC] = val.pMove[0] + 'Queen'
        # check for en Passant
        if val.checkEnPassant:
            self.board[val.startR][val.endC] = '_'

        if val.pMove[1:] == 'Pawn' and abs(val.startR - val.endR) == 2:
            self.enPassant = ((val.startR+val.endR)//2, val.startC)
        else:
            self.enPassant = ()

        # checking castle
        if val.checkCastle:
            if val.endC - val.startC == 2:
                self.board[val.endR][val.endC-1] = self.board[val.endR][val.endC+1]
                self.board[val.endR][val.endC+1]='_'
            else:
                self.board[val.endR][val.endC+1] = self.board[val.endR][val.endC-2]
                self.board[val.endR][val.endC-2]='_'

        self.castling(val)

        self.castles.append(Castle(self.castlingState.wRight, self.castlingState.bRight,
                                self.castlingState.wLeft, self.castlingState.bLeft))

    # get all the possible moves in general
    def getMoves(self):
        possibilities = []

        # loop through board
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):

                # get who's side it is (white or black)
                side = self.board[i][j][0]

                if (self.turn == 0 and side == 'w') or (self.turn == 1 and side == 'b'):
                    # find piece type and check which one it is
                    p = self.board[i][j][1:]
                    
                    # based on piece type find all possible moves of that type
                    if p == 'Pawn':
                        self.getPawns(possibilities, i, j)
                    elif p == 'Bish':
                        self.getBishops(possibilities, i, j)
                    elif p == 'Rook':
                        self.getRooks(possibilities, i, j)
                    elif p == 'King':
                        self.getKings(possibilities, i, j)
                    elif p == 'Queen':
                        self.getQueens(possibilities, i, j)
                    elif p == 'Kn':
                        self.getKnights(possibilities, i, j)
        
        return possibilities
    
    def castling(self, val):
        # castling state (4 possible states) 
        if val.pMove == 'bKing':
            self.castlingState.bRight = False
            self.castlingState.bLeft = False
        # based on piece moved, change castling states
        elif val.pMove == 'wKing':
            self.castlingState.wRight = False
            self.castlingState.wLeft = False

        elif val.pMove == 'bRook':
            if val.startR == 0:
                if val.startC == 0:
                    self.castlingState.bLeft = False
                elif val.startC == 7:
                    self.castlingState.bRight = False

        elif val.pMove == 'wRook':
            if val.startR == 7:
                if val.startC == 0:
                    self.castlingState.wLeft = False
                elif val.startC == 7:
                    self.castlingState.wRight = False

    # check for check
    def check(self):
        # check if the piece is getting killed (or the square)
        if (self.turn == 0):
            return self.gettingKilled(self.wKing[0], self.wKing[1])
        else:
            return self.gettingKilled(self.bKing[0], self.bKing[1])
            
    # check if move is legal 
    def isLegal(self):
        # en passant possible
        hold = self.enPassant
        # hold a castle instance
        temp = Castle(self.castlingState.wRight, self.castlingState.bRight,
                        self.castlingState.wLeft, self.castlingState.bLeft)
        # get all general possible moves
        possibilities = self.getMoves()

        # get castle moves possible
        if self.turn == 0:
            self.getCastles(self.wKing[0],self.wKing[1],possibilities)
        else:
            self.getCastles(self.bKing[0],self.bKing[1],possibilities)

        # loop backwards 
        for i in range(len(possibilities) - 1, -1, -1):
            self.movePiece(possibilities[i])

            # switch who's move it is
            if (self.turn == 0):
                self.turn = 1
            else:
                self.turn = 0
            
            # check if the move causes a check
            if (self.check()):
                # remove possibility since move is illegal
                possibilities.remove(possibilities[i])

            # swtich turn 
            if (self.turn == 0):
                self.turn = 1
            else:
                self.turn = 0

            # reverse move 
            if (len(self.moves) != 0):
                # get last move
                last = self.moves.pop()
                #switch
                self.board[last.startR][last.startC] = last.pMove
                self.board[last.endR][last.endC] = last.pTaken
                # switch turn
                if (self.turn == 0):
                    self.turn = 1
                else:
                    self.turn = 0
                # change king's position
                if last.pMove == 'wKing':
                    self.wKing = (last.startR, last.startC)
                elif last.pMove == 'bKing':
                    self.bKing = (last.startR, last.startC)
                # reverse en Passant
                if last.checkEnPassant:
                    self.board[last.endR][last.endC] = '_'
                    self.board[last.startR][last.endC] = last.pTaken
                    self.enPassant = (last.endR,last.endC)
                if last.pMove[1:] == 'Pawn' and abs(last.startR - last.endC) == 2:
                    self.enPassant = ()

                # reverse castle
                self.castles.pop()
                self.castlingState = self.castles[-1]

                if last.checkCastle:
                    if last.endC - last.startC == 2:
                        self.board[last.endR][last.endC+1] = self.board[last.endR][last.endC-1]
                        self.board[last.endR][last.endC-1]='_'
                    else:
                        self.board[last.endR][last.endC-2] = self.board[last.endR][last.endC+1]
                        self.board[last.endR][last.endC+1]='_'

        # no moves left
        if (len(possibilities) == 0):
            # game is over
            self.gameOver = True

            # checkmate versus stalemate
            if self.check():
                self.cMate = True
            else:
                self.draw = True
        else:
            # reset
            self.draw = False
            self.cMate = False
            self.gameOver = False
        # switch back
        self.enPassant = hold
        self.castlingState = temp
        return possibilities

    # checking if board location is being hit by a piece
    def gettingKilled(self, row, col):
        # switch turn
        if (self.turn == 0):
            self.turn = 1
        else:
            self.turn = 0
        
        # get enemy's moves
        oppPossibilities = self.getMoves()
        # switch turn 
        if (self.turn == 0):
            self.turn = 1
        else:
            self.turn = 0

        # go through possible enemy moves and return true if final square is same as checking square
        for option in oppPossibilities:
            if option.endR == row and option.endC == col:
                return True
        return False

    # pawn movements possible
    def getPawns(self, possibilities, row, col):
        # white's turn
        if self.turn == 0:
            # single move case
            if self.board[row-1][col] == '_':
                possibilities.append(Move(self.board,(row,col),(row-1,col)))

                # double move case
                if row == 6 and self.board[row-2][col] == '_':
                    possibilities.append(Move(self.board,(row,col),(row-2, col)))

            # capturing diagonal left
            if col + 1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    possibilities.append(Move(self.board,(row,col),(row-1, col+1)))

                elif self.enPassant == (row-1, col+1):
                    possibilities.append(Move(self.board,(row,col),(row-1, col+1), checkEnPassant=True))

            # capturing diagonal right
            if col - 1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    possibilities.append(Move(self.board,(row,col),(row-1, col-1)))

                elif self.enPassant == (row-1, col-1):
                    possibilities.append(Move(self.board,(row,col),(row-1, col-1), checkEnPassant=True))

        # black's pawns moving, same as white just reversed directions
        else:
            # move pawn once
            if self.board[row+1][col] == '_':
                possibilities.append(Move(self.board,(row,col),(row+1, col)))
                # move twice
                if row == 1 and self.board[row+2][col] == '_':
                    possibilities.append(Move(self.board,(row,col),(row+2, col)))

            # capture to right
            if col + 1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    possibilities.append(Move(self.board,(row,col),(row+1, col+1)))
                # check en passant
                elif self.enPassant == (row+1, col+1):
                    possibilities.append(Move(self.board,(row,col),(row+1, col+1), checkEnPassant=True))

            # capture to left
            if col - 1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    possibilities.append(Move(self.board,(row,col),(row+1, col-1)))
                # check en Passant
                elif self.enPassant == (row+1, col-1):
                    possibilities.append(Move(self.board,(row,col),(row+1, col-1), checkEnPassant=True))

    # bishop move possibilities
    def getBishops(self, possibilities, row, col):
        # list of directions
        dirs = [(-1, -1),(-1,1), (1,-1),(1,1)]

        if self.turn == 0:
            opponent = 'b'
        else:
            opponent = 'w'

        for direction in dirs:
            for i in range(1, 8):
                # get all directions for up to 8 possibilities each way at first
                finalR = row + direction[0] * i
                finalC = col + direction[1] * i

                if finalR >= 0 and finalR < 8:
                    if finalC >= 0 and finalC < 8:
                        # final Position piece
                        finalP = self.board[finalR][finalC]

                        if (finalP == '_'):
                            possibilities.append(Move(self.board,(row, col),(finalR, finalC)))
                        elif (finalP[0] == opponent):
                            possibilities.append(Move(self.board, (row,col),(finalR,finalC)))
                            break
                        # if same side piece in way (break out of loop no more possibilities)
                        else:
                            break
                else:
                    break

    # rook move possibilities               
    def getRooks(self, possibilities, row, col):
        # list of directions
        dirs = [(-1, 0),(0,-1,),(1,0),(0,1)]

        if self.turn == 0:
            opponent = 'b'
        else:
            opponent = 'w'

        for direction in dirs:
            for i in range(1,8):
                # get all directions for up to 8 possibilities each way at first
                finalR = row + direction[0] * i
                finalC = col + direction[1] * i

                if finalR >= 0 and finalR < 8:
                    if finalC >= 0 and finalC < 8:

                        finalP = self.board[finalR][finalC]

                        if (finalP == '_'):
                            possibilities.append(Move(self.board,(row, col),(finalR, finalC)))
                        # opponent piece in the way
                        elif (finalP[0] == opponent):
                            possibilities.append(Move(self.board, (row,col),(finalR,finalC)))
                            break

                        # if same side piece is in the way
                        else:
                            break
                else:
                    break
                        
                
    # king move possibilities
    def getKings(self, possibilities, row, col):
        if self.turn == 0:
            opponent = 'b'
        else:
            opponent = 'w'
        # Word Search https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html#wordsearch1 
        for drow in [-1,0,1]:
            for dcol in [-1,0,1]:
                if (drow, dcol) != (0,0):
                    finalR = row + drow
                    finalC = col + dcol
                    
                    # check if in bounds
                    if finalR >= 0 and finalR < 8:
                        if finalC >= 0 and finalC < 8:
                            # set result position "piece" to final piece
                            finalP = self.board[finalR][finalC]
                            # if moving to empty square, add those possible moves
                            if (finalP == '_'):
                                possibilities.append(Move(self.board,(row,col),(finalR,finalC)))
                            # if opponent's piece is on square in range, add those possible captures
                            elif (finalP[0] == opponent):
                                possibilities.append(Move(self.board,(row,col),(finalR,finalC)))
                                break
    
    # get castle possibilities
    def getCastles(self, row, col, possibilities):
        # make sure not in check or through
        if self.gettingKilled(row,col):
            return
        
        # castling king side versus queen side
        if (self.turn == 0 and self.castlingState.wRight) or (self.turn == 1 and self.castlingState.bRight):
            self.getRight(row, col, possibilities)

        if (self.turn == 0 and self.castlingState.wLeft) or (self.turn == 1 and self.castlingState.bLeft):
            self.getLeft(row, col, possibilities)
    
    # king side castling
    def getRight(self,row, col, possibilities):
        if self.board[row][col+1] == '_' and self.board[row][col+2] == '_':
            if not self.gettingKilled(row, col+1) and not self.gettingKilled(row,col+2):
                possibilities.append(Move(self.board,(row,col), (row, col+2), checkCastle = True))

    # queen side castling
    def getLeft(self,row, col, possibilities):
        if self.board[row][col-1] == '_' and self.board[row][col-2] == '_' and self.board[row][col-3] == '_':
            if not self.gettingKilled(row, col-1) and not self.gettingKilled(row,col-2):
                possibilities.append(Move(self.board,(row,col), (row, col-2), checkCastle = True))
        
    # queen move possibilities
    def getQueens(self, possibilities, row, col):
        # queen movement is the same as bishop and rook combined
        self.getBishops(possibilities, row, col)
        self.getRooks(possibilities, row, col)

    # knight move possibilities
    def getKnights(self, possibilities, row, col):
        # 8 directions
        dirs = [(-2, -1),(-2,1), (1,2),(-1,2),(2,1),(2,-1),(1,-2),(-1,-2)]

        if self.turn == 0:
            friendly = 'w'
        else:
            friendly = 'b'

        for direction in dirs:
            finalR = row + direction[0] 
            finalC = col + direction[1] 

            if finalR >= 0 and finalR < 8:
                if finalC >= 0 and finalC < 8:
                    # get all directions for up to 8 possibilities each way at first
                    # final position piece
                    finalP = self.board[finalR][finalC]
                    if (finalP[0] != friendly):
                        possibilities.append(Move(self.board,(row, col),(finalR, finalC)))
                    
# move class that tracks movement by using start and end 
class Move(object):
    def __init__(self, board, start, end, checkEnPassant=False, checkCastle = False):
        # get the row and col of the square clicked on and the target square
        self.startR = start[0]
        self.endR = end[0]
        self.startC = start[1]
        self.endC = end[1]

        # for eq method later
        self.num = str(self.startR) + str(self.endR) + str(self.startC) + str(self.endC)
        
        # piece moved and piece that is taken
        self.pMove = board[self.startR][self.startC]
        self.pTaken = board[self.endR][self.endC]

        # promote, castle, en passant
        self.promote = (self.pMove == 'bPawn' and self.endR == 7) or (self.pMove == 'wPawn' and self.endR == 0)
        self.checkEnPassant = checkEnPassant
        self.checkCastle = checkCastle

        # check en Passant
        if self.checkEnPassant:
            if self.pMove == 'wPawn':
                self.pTaken = 'bPawn'
            elif (self.pMove == 'bPawn'):
                self.pTaken = 'wPawn'

        # converting to dictionaries (basically how chess notation works but in terms of indices)
        self.convertFile = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        self.convertC = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
        self.convertLevel = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
        self.convertR = {7:'1', 6:'2', 5:'3', 4:'4', 3:'5', 2:'6', 1:'7', 0:'8'}

    # same object needed
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.num == other.num
        else:
            return False
        

# class for castling
class Castle():
    def __init__(self, wRight, bRight, wLeft, bLeft):
        # 4 places where you can castle
        self.wRight = wRight
        self.bRight = bRight
        self.wLeft = wLeft
        self.bLeft = bLeft  
    
    
        
