import math, random, copy
from piecesClass import *
from cmu_112_graphics import *

def appStarted(app):
    app.rows = 8
    app.cols = 8
    app.cBoard = []
    app.margin = 100

    for i in range(app.rows):
        app.cBoard += [[None]*app.cols]
    # bKing = K(Pieces)
    
    for i in range(app.rows):
        for j in range(app.cols):
            if (i+j % 2 == 1):
                app.cBoard[i][j] = "black"
            else:
                app.cBoard[i][j] = "white"
def drawRook(app, canvas):
    canvas.create_rectangle(400,400,450,450, fill='red')
# def timerFired(app):

def mousePressed(app, event):
    if event.x == 200 :
        selectedPiece = 1
# def keyPressed(app, event):
    # return
def redrawAll(app, canvas):
    # canvas.create_text("Welcome to Ches")
    drawBoard(app, canvas)
    drawRook(app,canvas)
    print(app.cBoard[5][4])
# def drawBoard(app, canvas):
#     for i in range(8):
#         for j in range(8):
#             canvas.create_rectangle()


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



def main():
    runApp(width=800, height=800)
if __name__ == '__main__':
    main()