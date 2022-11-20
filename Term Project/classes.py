# These are the classes used to create my chess game

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

        # past list of moves
        self.moves = []

        # 0 is white, 1 is black's turn
        self.turn = 0

    # move piece function that allows piece to be moved
    def movePiece(self, val):
        print(val.startR, val.startC, val.endR, val.endC, val.pMove)

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
                    if p == 'Rook':
                        self.getRooks(possibilities, i, j)
                    elif p == 'Pawn':

                        self.getPawns(possibilities, i, j)
                    elif p == 'King':
                        self.getKings(possibilities, i, j)
                    elif p == 'Queen':
                        self.getQueens(possibilities, i, j)
        
        return possibilities
        
    # check if move is legal 
    def isLegal(self):
        return self.getMoves()

    def getRooks(self, possibilities, row, col):
        return

    # pawn movements possible
    def getPawns(self, possibilities, row, col):
        # white's turn
        if self.turn == 0:
            # single move case
            if self.board[row-1][col] == '_':
                possibilities.append(Move(self.board,(row,col),(row-1, col)))

                # double move case
                if row == 6 and self.board[row-2][col] == '_':
                    possibilities.append(Move(self.board,(row,col),(row-2, col)))
            # capturing diagonal right
            if col + 1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    possibilities.append(Move(self.board,(row,col),(row-1, col+1)))

            # capturing diagonal left
            if col - 1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    possibilities.append(Move(self.board,(row,col),(row-1, col-1)))

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
            # capture to left
            if col - 1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    possibilities.append(Move(self.board,(row,col),(row+1, col-1)))

    def getKings(self, possibilities, row, col):
        return
    def getQueens(self, possibilities, row, col):
        return

# move class that tracks movement by using start and end
class Move(object):
    def __init__(self, board, start, end):
        # get the row and col of the square clicked on and the target square
        self.startR = start[0]-1
        self.endR = end[0]-1
        self.startC = start[1]-1
        self.endC = end[1]-1

        # piece moved and piece that is taken
        self.pMove = board[self.startR][self.startC]
        self.pTaken = board[self.endR][self.endC]

        # converting to dictionaries (basically how chess notation works but in terms of indices)
        self.convertFile = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        self.convertC = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
        self.convertLevel = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
        self.convertR = {7:'1', 6:'2', 5:'3', 4:'4', 3:'5', 2:'6', 1:'7', 0:'8'}
        
    # get the official chess notation 
    def getOfficialSquare(self):
        temp = self.convertC(self.startC) + self.convertR(self.startR)
        hold = self.convertC(self.endC) + self.convertR(self.endR)
        return temp + hold

    
        
