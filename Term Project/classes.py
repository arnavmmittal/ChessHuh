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

    
        
