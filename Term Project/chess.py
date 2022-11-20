import math, random, copy
import boardClass
from cmu_112_graphics import *

# Piece Images from ->
# https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent
def appStarted(app):
    app.rows = 8
    app.cols = 8
    # app.cBoard = []
    app.margin = 100
    app.Pieces = dict()
    app.start = True
    
    pcs = ['bRook', 'bKn', 'bBish', 'bQueen', 'bKing', 'bPawn', 'wRook', 'wBish', 'wKn', 'wQueen', 'wKing', 'wPawn']
    for p in pcs:
        app.Pieces[p] = app.loadImage('pieceImages/' + p + ".png")

    # for i in range(app.rows):
    #     app.cBoard += [[None]*app.cols]
    # # bKing = K(Pieces)
    
    # for i in range(app.rows):
    #     for j in range(app.cols):
    #         if (i+j % 2 == 1):
    #             app.cBoard[i][j] = "black"
    #         else:
    #             app.cBoard[i][j] = "white"


    

# def timerFired(app):
    
        

def mousePressed(app, event):
    if event.x == 200 :
        selectedPiece = 1
# def keyPressed(app, event):
    # return


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
    # loops that create board of equal blue cells
    
    for i in range(app.rows):
        for j in range(app.cols):
            if ((i+j) % 2 == 1):
                drawCell(app, canvas, i, j, "black")

            else:
                drawCell(app, canvas, i, j, "white")


def drawPcs(app, canvas, board):
    for i in range(app.rows):
        for j in range(app.cols):
            p = board[i][j]
            if "_" != p:
                canvas.create_image(200, 200, image=ImageTk.PhotoImage(app.Pieces[p]))

def redrawAll(app, canvas):
    # canvas.create_text("Welcome to Chess")
    drawBoard(app, canvas)
    drawPcs(app, canvas, boardClass.Board().board)


def main():
    runApp(width=800, height=800)


if __name__ == '__main__':
    main()
