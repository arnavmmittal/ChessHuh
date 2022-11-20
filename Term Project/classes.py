# These are the classes used to create my chess game

# board class that keeps track of board and each square
class Board(object):
    def __init__(self):
        # board initializing
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
        self.moves = []
        # 0 is white, 1 is black's turn
        self.turn = 0

    def movePiece(self, val):
        print(val.startR, val.startC, val.endR, val.endC, val.pMove)
        self.board[val.startR][val.startC] = '_'
        self.board[val.endR][val.endC] = val.pMove

        self.moves.append(val) 
        
        if (self.turn == 0):
            self.turn = 1
        else:
            self.turn = 0
    
    def getMoves(self):
        possibilities = []

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                side = self.board[i][j][0]
                if (self.turn == 0 and side == 'w') or (self.turn == 1 and side == 'b'):
                    p = self.board[i][j][1:]
                    
                    if p == 'Rook':
                        self.getRooks(possibilities, i, j)
                    elif p == 'Pawn':

                        self.getPawns(possibilities, i, j)
                    elif p == 'King':
                        self.getKings(possibilities, i, j)
                    elif p == 'Queen':
                        self.getQueens(possibilities, i, j)
        
        return possibilities
        
    def isLegal(self):
        return self.getMoves()

    def getRooks(self, possibilities, row, col):
        return

    def getPawns(self, possibilities, row, col):
        if self.turn == 0:
            if self.board[row-1][col] == '_':
                possibilities.append(Move(self.board,(row,col),(row-1, col)))
                if row == 6 and self.board[row-2][col] == '_':
                    possibilities.append(Move(self.board,(row,col),(row-2, col)))

            if col + 1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    possibilities.append(Move(self.board,(row,col),(row-1, col+1)))
            if col - 1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    possibilities.append(Move(self.board,(row,col),(row-1, col-1)))
        else:
            if self.board[row+1][col] == '_':
                possibilities.append(Move(self.board,(row,col),(row+1, col)))
                if row == 1 and self.board[row+2][col] == '_':
                    possibilities.append(Move(self.board,(row,col),(row+2, col)))

            if col + 1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    possibilities.append(Move(self.board,(row,col),(row+1, col+1)))
            if col - 1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    possibilities.append(Move(self.board,(row,col),(row+1, col-1)))

    def getKings(self, possibilities, row, col):
        return
    def getQueens(self, possibilities, row, col):
        return


class Move(object):
    def __init__(self, board, start, end):
        self.startR = start[0]-1
        self.endR = end[0]-1
        self.startC = start[1]-1
        self.endC = end[1]-1
        self.pMove = board[self.startR][self.startC]
        self.pTaken = board[self.endR][self.endC]

        self.convertFile = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        self.convertC = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
        self.convertLevel = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
        self.convertR = {7:'1', 6:'2', 5:'3', 4:'4', 3:'5', 2:'6', 1:'7', 0:'8'}
        
    def getOfficialSquare(self):
        temp = self.convertC(self.startC) + self.convertR(self.startR)
        hold = self.convertC(self.endC) + self.convertR(self.endR)
        return temp + hold

    
        
