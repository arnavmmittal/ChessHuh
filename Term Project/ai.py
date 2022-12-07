import random

# tracking score for each piece (values)
materialVals = {'King': 0, 'Queen': 8, 'Rook':5, 'Bish':4, 'Kn':3, 'Pawn':1}

# checkmate worth max
cMate = 100

# stalemate 
sMate = 0

# makes random move from legal moves
def randMove(legalMoves):
    if len(legalMoves) != 0:
        return legalMoves[random.randint(0,len(legalMoves)-1)]
    return None

# gets a score in terms of material
def getMaterial(board):
    mat = 0
    # loop through each cell in board and add points for each respective place
    for r in board:
        for cell in r:
            if cell[0] == 'w':
                mat += materialVals[cell[1:]]
            elif cell[0] == 'b':
                mat -= materialVals[cell[1:]]
    return mat

# non recursive miniMax algorithm to get best move (no alpha beta pruning which would've saved time and found better moves)
# 
# Help from https://www.chessprogramming.org/Minimax
# and https://www.idtech.com/blog/minimax-algorithm-in-chess-checkers-tic-tac-toe 

def getBest(state, legalMoves):
    best = None
    minMax = cMate 
    
    # random shuffle all the legal moves
    random.shuffle(legalMoves)

    # go through moves
    for legalMove in legalMoves:

        state.movePiece(legalMove)
        oppMoves = state.isLegal()

        # reverse max (due to zero sum)
        oppMax = -1 * cMate

        # check opponents moves for each legal move
        for oppMove in oppMoves:
            # move the piece
            state.movePiece(oppMove)

            # check if draw or checkmate  and get material
            if state.cMate:
                if state.turn == 0:
                    mat = -1 * cMate
                elif state.turn == 1:
                    mat = cMate
            elif state.draw:
                mat = sMate
            else:
                if state.turn == 0:
                    mat = -1 * getMaterial(state.board)
                elif state.turn == 1:
                    mat = getMaterial(state.board)

            # if material switch greater, then switch
            if mat > oppMax:
                oppMax = mat
                
            # reverse move 
            if (len(state.moves) != 0):
                # get last move
                last = state.moves.pop()
                #switch
                state.board[last.startR][last.startC] = last.pMove
                state.board[last.endR][last.endC] = last.pTaken
                # switch turn
                if (state.turn == 0):
                    state.turn = 1
                else:
                    state.turn = 0

                # change king's position
                if last.pMove == 'wKing':
                    state.wKing = (last.startR, last.startC)
                elif last.pMove == 'bKing':
                    state.bKing = (last.startR, last.startC)
                
                # enpassant part of reverse
                if last.checkEnPassant:
                    state.board[last.endR][last.endC] = '_'
                    state.board[last.startR][last.endC] = last.pTaken
                    state.enPassant = (last.endR,last.endC)
                if last.pMove[1:] == 'Pawn' and abs(last.startR - last.endC) == 2:
                    state.enPassant = ()
                
                # reverse castle
                state.castles.pop()
                state.castlingState = state.castles[-1]
                
                if last.checkCastle:
                    if last.endC - last.startC == 2:
                        state.board[last.endR][last.endC+1] = state.board[last.endR][last.endC-1]
                        state.board[last.endR][last.endC-1]='_'
                    else:
                        state.board[last.endR][last.endC-2] = state.board[last.endR][last.endC+1]
                        state.board[last.endR][last.endC+1]='_'

        # switch and get best move
        if oppMax < minMax:
            minMax = oppMax
            best = legalMove

        # reverse move 
        if (len(state.moves) != 0):
            # get last move
            last = state.moves.pop()
            # switch
            state.board[last.startR][last.startC] = last.pMove
            state.board[last.endR][last.endC] = last.pTaken
            # switch turn
            if (state.turn == 0):
                state.turn = 1
            else:
                state.turn = 0
            # change king's position
            if last.pMove == 'wKing':
                state.wKing = (last.startR, last.startC)
            elif last.pMove == 'bKing':
                state.bKing = (last.startR, last.startC)
            # for enpassant
            if last.checkEnPassant:
                state.board[last.endR][last.endC] = '_'
                state.board[last.startR][last.endC] = last.pTaken
                state.enPassant = (last.endR,last.endC)
            if last.pMove[1:] == 'Pawn' and abs(last.startR - last.endC) == 2:
                state.enPassant = ()
            
            # reverse for castle
            state.castles.pop()
            state.castlingState = state.castles[-1]

            if last.checkCastle:
                if last.endC - last.startC == 2:
                    state.board[last.endR][last.endC+1] = state.board[last.endR][last.endC-1]
                    state.board[last.endR][last.endC-1]='_'
                else:
                    state.board[last.endR][last.endC-2] = state.board[last.endR][last.endC+1]
                    state.board[last.endR][last.endC+1]='_'
    # return best move found
    return best
