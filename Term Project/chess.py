import math, random, copy
import classes
from cmu_112_graphics import *

# Piece Images from ->
# https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent
def appStarted(app):
    app.rows = 8
    app.cols = 8
    app.margin = 100
    app.Pieces = dict()
    app.start = True
    app.counter = 0
    app.clicks = []
    app.selection = ()
    


    app.state = classes.Board()
    app.legalMoves = app.state.isLegal()
    app.moved = False
    app.cellSize = (app.width - 2*app.margin)/8
    pcs = ['bRook', 'bKn', 'bBish', 'bQueen', 'bKing', 'bPawn', 'wRook', 'wBish', 'wKn', 'wQueen', 'wKing', 'wPawn']
    for p in pcs:
        app.Pieces[p] = app.scaleImage(app.loadImage('pieceImages/' + p + ".png"),1.2)
        

# def timerFired(app):
#     if app.moved:
#         app.legalMoves = app.state.isLegal()
#         app.moved = False
    
        
def mousePressed(app, event):
    if (event.x < app.width-app.margin) and event.x > app.margin:
        if (event.y < app.height-app.margin and event.y > app.margin):
            r = event.y // app.cellSize
            c = event.x // app.cellSize
            if r <9 and r >-1:
                if c < 9 and c > -1:
                    if app.selection == (event.x, event.y):
                        app.clicks = []
                        app.selection = ()
                    else:
                        r,c = math.floor(r), math.floor(c)
                        app.selection = (r,c)
                        app.clicks.append(app.selection)
                    if len(app.clicks) == 2:
                        print(app.selection)
                        m = classes.Move(app.state.board,app.clicks[0],app.clicks[1])
                        print(m, 'x')
                        # if m in app.legalMoves:
                        #     print("hi")
                        app.state.movePiece(m)
                        app.moved = True
                        
                        print(app.state.board)
                        app.selection = ()
                        app.clicks = []
        
def keyPressed(app, event):
    if event.key == "r":
        app.state.board = classes.Board().board


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

def drawCell(app, canvas, row, col, color):
    # draw each cell in board
    canvas.create_rectangle(getCellBounds(app, row, col),
        fill=color, outline='black', width=4)

def drawBoard(app, canvas):
    
    for i in range(app.rows):
        for j in range(app.cols):

            if ((i+j) % 2 == 1):
                drawCell(app, canvas, i, j, "maroon")

            else:
                drawCell(app, canvas, i, j, "white")


def drawPcs(app, canvas, board):
    for i in range(app.rows):
        for j in range(app.cols):
            (x0,y0,x1,y1) = getCellBounds(app,i,j)
            p = board[i][j]
            if "_" != p:
                canvas.create_image((x0+x1)/2, (y0+y1)/2, image=ImageTk.PhotoImage(app.Pieces[p]))

def redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height/10, text="Welcome to ChessHuh!", font="Arial 30",fill='black')
    drawBoard(app, canvas)
    drawPcs(app, canvas, app.state.board)

def main():
    runApp(width=800, height=800)

if __name__ == '__main__':
    main()
