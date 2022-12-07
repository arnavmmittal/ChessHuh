import math, random, copy
import ai
import classes

from cmu_112_graphics import *

# Piece Images from ->
# https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent
def appStarted(app):
    # game dimensions
    app.rows = 8
    app.cols = 8
    app.margin = 100

    # types of pieces
    app.Pieces = dict()

    # keeps track of clicks (location)
    app.clicks = []
    # selected location
    app.selection = ()

    # timers for black and white 
    app.wTimer = 300
    app.bTimer = 300

    # current state that game is going in
    app.state = classes.Board()
    app.start = True

    # whether player 1 and 2 are real players or not
    app.p1 = True
    app.p2 = True

    # player turn
    app.pTurn = (app.state.turn == 0 and app.p1) or (app.state.turn == 1 and app.p2)
    
    # get legal moves
    app.legalMoves = app.state.isLegal()

    app.moved = False

    # get size of each cell
    app.cellSize = (app.width - 2*app.margin)/8

    # check if game over
    app.gameOver = app.state.cMate or app.state.draw


    # loading images based on pieces
    pcs = ['bRook', 'bKn', 'bBish', 'bQueen', 'bKing', 'bPawn', 'wRook', 'wBish', 'wKn', 'wQueen', 'wKing', 'wPawn']
    for p in pcs:
        app.Pieces[p] = app.scaleImage(app.loadImage('pieceImages/' + p + ".png"),1.2)

# controls if user wants pass and play or to play against AI
def choosePlayer(app):
    # get user input
    whiteSide = int(input("Choose if white is player or AI (0 or 1, respectively)."))
    blackSide = int(input("Choose if black is player or AI (0 or 1, respectively)."))

    # use user input to switch which side is AI and which side is player (or both)
    if whiteSide == 1:
        app.p1 = False
    elif whiteSide == 0:
        app.p1 = True
    if blackSide == 1:
        app.p2 = False
    else:
        app.p2 = True


def timerFired(app):
    # timer delay mainly for AI
    app.timerDelay = 100

    # tracking timers and decrementing 
    if app.p1 == True and app.p2 == True and not app.state.cMate and not app.state.draw:
        # goes down by 1000 milliseconds or 1 second
        app.timerDelay = 1000

        # based on whose turn, reduce timer until 0
        if app.state.turn == 0:
            app.wTimer -= 1
            if app.wTimer <= 0:
                app.state.cMate = True
                app.gameOver = True
        elif app.state.turn == 1:
            app.bTimer -= 1
            if app.bTimer <= 0:
                app.state.cMate = True
                app.gameOver = True

    # if game is not over
    if not app.state.cMate and not app.state.draw:

        # choose AI or player
        if app.start:
            choosePlayer(app)
            app.start = False
        
        # get player's turn
        app.pTurn = (app.state.turn == 0 and app.p1) or (app.state.turn == 1 and app.p2)

        # AI moves
        if not app.gameOver and not app.pTurn and app.moved == False:
            # get best move 
            artificial = ai.getBest(app.state, app.legalMoves)
            # if there is no best move calculated, then gets random move from legal moves
            if artificial == None and app.state.cMate == False and app.state.draw == False:
                artificial = ai.randMove(app.legalMoves)

            if (artificial != None):
                app.state.movePiece(artificial)
                app.moved = True
        # if moved, get new legal moves
        if app.moved:
            app.moved = False
            app.legalMoves = app.state.isLegal()
    
# main function in chess.py
def mousePressed(app, event):
    # get player turn
    app.pTurn = (app.state.turn == 0 and app.p1) or (app.state.turn == 1 and app.p2)
    # if game is not over 
    if not app.gameOver and app.pTurn:
        # check bounds of click
        if (event.x < app.width-app.margin) and event.x > app.margin:
            if (event.y < app.height-app.margin and event.y > app.margin):
                # get technical row and column of 2d chess board
                r = event.y // (app.cellSize)
                c = event.x // (app.cellSize)
                # check bounds
                if r <9 and r >-1:
                    if c < 9 and c > -1:
                        # get tuple of selection point
                        if app.selection == (event.x, event.y):
                            app.clicks = []
                            app.selection = ()
                        else:
                            # convert from float to int
                            r,c = math.floor(r)-1, math.floor(c)-1
                            # selected square
                            app.selection = (r,c)
                            # add to clicks
                            app.clicks.append(app.selection)

                        # if mouse clicked twice, piece is moved (if legal)
                        if len(app.clicks) == 2:
                            # use move class to get move
                            m = classes.Move(app.state.board,app.clicks[0],app.clicks[1])
                            # for all legal moves, if move is in it, move that piece
                            for i in range(len(app.legalMoves)):
                                if m == app.legalMoves[i]:

                                    # moving piece
                                    app.state.movePiece(app.legalMoves[i])
                                    app.moved = True

                                    # reset
                                    app.selection = ()
                                    app.clicks = []

                            if not app.moved:
                                # just first selection (gets rid of "selecting empty square" bug)
                                app.clicks = [app.selection]
                
                if app.moved:
                    app.moved = False
                    app.legalMoves = app.state.isLegal()
        
def keyPressed(app, event):
    # reset board if r clicked
    if event.key == "r":
        app.state = classes.Board()
        app.moved = False
        app.legalMoves = app.state.isLegal()
        app.wTimer = 300
        app.bTimer = 300
        app.state.cMate = False
        app.state.draw = False
        app.start = True
        
    
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

# draws each cell in chess board
def drawCell(app, canvas, row, col, color):
    # draw each cell in board
    canvas.create_rectangle(getCellBounds(app, row, col),
        fill=color, outline='black', width=4)

# draws chess board
def drawBoard(app, canvas):
    # loop through chess board size and draw different colored square based on odd or even
    for i in range(app.rows):
        for j in range(app.cols):

            if ((i+j) % 2 == 1):
                drawCell(app, canvas, i, j, "maroon")

            else:
                drawCell(app, canvas, i, j, "white")

# draws all the pieces at the right place
def drawPcs(app, canvas, board):
    for i in range(app.rows):
        for j in range(app.cols):
            (x0,y0,x1,y1) = getCellBounds(app,i,j)

            # using app.Pieces, this checks the board for piece occupied squares and fills them with images
            p = board[i][j]
            if "_" != p:
                canvas.create_image((x0+x1)/2, (y0+y1)/2, image=ImageTk.PhotoImage(app.Pieces[p]))

# draws timers with formatting
def drawTimers(app, canvas):
    # only if pass and play
    if app.p1 == True and app.p2 == True:
        # highlight the respective timer blue
        if app.state.turn == 0:
            canvas.create_rectangle(app.width/8, app.height/15, app.width/4, app.height/9, fill='light blue')
            canvas.create_rectangle(3*app.width/4, app.height/15, 7*app.width/8, app.height/9, fill='white')
        if app.state.turn == 1:
            canvas.create_rectangle(app.width/8, app.height/15, app.width/4, app.height/9, fill='white')
            canvas.create_rectangle(3*app.width/4, app.height/15, 7*app.width/8, app.height/9, fill='light blue')
        
        # convert timer value to minutes and seconds format for white and black
        wMin = app.wTimer//60
        wSec = str(app.wTimer % 60)
        
        if int(wSec) < 10:
            wSec = "0"+str(wSec)
            print(wSec)

        bMin = app.bTimer//60
        bSec = str(app.bTimer % 60)

        if int(bSec) < 10:
            bSec = "0"+str(bSec)

        # create text that is the timer
        canvas.create_text(3*app.width/16, 4*app.height/45, text=str(wMin) + ":" + str(wSec), fill='black', font="Arial 20")
        canvas.create_text(13*app.width/16, 4*app.height/45, text=str(bMin) + ":" + str(bSec), fill='black', font="Arial 20")

# draw final result
def drawEnd(app, canvas):
    # if game over
    if (app.state.cMate or app.state.draw):
        if app.state.cMate == True and not app.state.draw:
            canvas.create_rectangle(0, app.height/2.5, app.width, 2*app.height/3.25, fill="maroon")
            temp = ""
            if app.state.turn == 1:
                temp = "White"
            else:
                temp = "Black"
            # win by time
            if app.wTimer <= 0 or app.bTimer <= 0:
                canvas.create_text(app.width/2, app.height/2, text="- " +temp + " wins on time! -", font='Arial 50')
            # win by checkmate
            else:
                canvas.create_text(app.width/2, app.height/2, text="- Checkmate! " + temp + " Wins! -", font='Arial 50')
            
        # draw by stalemate
        elif app.state.draw == True:
            canvas.create_rectangle(0, app.height/2.5, app.width, 2*app.height/3.25, fill='maroon')
            canvas.create_text(app.width/2, app.height/2, text="- It's a Tie! -", font='Arial 50')


def redrawAll(app, canvas):
    # background
    canvas.create_rectangle(0,0,app.width,app.height, fill='black')
    # title
    canvas.create_text(app.width/2, app.height/12, text="ChessHuh", font="Arial 40",fill='white')

    # draw board, pieces, timers, and ending result (with condition)
    drawBoard(app, canvas)
    drawPcs(app, canvas, app.state.board)
    drawTimers(app,canvas)
    drawEnd(app,canvas)

def main():
    runApp(width=800, height=800)

if __name__ == '__main__':
    main()
