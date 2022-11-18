
class Board():
    def __init__(self, turn):
        # board initializing
        self.board = [
            ['bRook', 'bKn', 'bBish', 'bQueen', 'bKing', 'bBish', 'bKn', 'bRook'],
            ['bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn'],
            ['_', '_', '_','_','_','_','_','_'],
            ['_', '_', '_','_','_','_','_','_'],
            ['_', '_', '_','_','_','_','_','_'],
            ['_', '_', '_','_','_','_','_','_'],
            ['wPawn', 'wPawn', 'wPawn','wPawn','wPawn','wPawn','wPawn','wPawn'],
            ['wRook', 'wKn', 'wBish','wQueen','wKing','wBish','wKn','wRook'],  
        ]
        # 0 is white, 1 is black's turn
        self.turn = turn
        
