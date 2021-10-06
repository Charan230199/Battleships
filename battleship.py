"""
Battleship Project
Name: G.V.S. Sai Charan
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"]=10
    data["cols"]=10
    data["board-size"]=500
    data["cell-size"]= data["board-size"]/data["rows"]                              
    data["Number of ships"]=5
    # User= test.testGrid()                                                          
    data["User-board"] =emptyGrid(data["rows"], data["cols"])
    data["computer"] = emptyGrid(data["rows"], data["cols"])                        
    addShips(data["computer"], data["Number of ships"])
    data["temp_boat"]= []
    data["user_track"]=0
    return


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["User-board"], True)
    drawShip(data, userCanvas, data["temp_boat"])
    drawGrid(data, compCanvas, data["computer"], False)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    pass


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    mouse_event = getClickedCell(data,event)
    if board == "user":
        clickUserBoard(data,mouse_event[0],mouse_event[1])
    else:
        runGameTurn(data,mouse_event[0],mouse_event[1])
    return

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid=[]
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(EMPTY_UNCLICKED)
        grid.append(col)
    return (grid)



'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    row = random.randint(1,8)
    col = random.randint(1,8)
    
    col_or_row = random.randint(0,1)
    
    ship1=[]
    
    if col_or_row == 0:                    
        for row in range(row-1, row+2):
            ship1.append([row,col])
    else:                                 
        for col in range(col-1, col+2):
            ship1.append([row,col])
    return ship1 



'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    temp=0
    for i in ship:
        if grid[i[0]][i[1]] == 1:
            temp+=1
            if temp == 3:
                return True
        else:
            return False


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    temp=0
    while temp < numShips:
        ship2= createShip()
        if checkShip(grid, ship2) == True:
            for i in range(len(ship2)):
                grid[ship2[i][0]][ship2[i][1]] =SHIP_UNCLICKED
            temp+=1
    return grid
    



'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    x=data["cell-size"]
    for row in range(data["rows"]):
        for col in range(data["cols"]):
            if grid[row][col] == SHIP_UNCLICKED:
                canvas.create_rectangle(x*col, x*row, x*(col+1), x*(row+1), fill="yellow")
            elif grid[row][col] == EMPTY_UNCLICKED:
                canvas.create_rectangle(x*col, x*row, x*(col+1), x*(row+1), fill="blue")
            elif grid[row][col] == SHIP_CLICKED:
                canvas.create_rectangle(x*col,x*row,x*(col+1),x*(row+1), fill="red")
            elif grid[row][col] == EMPTY_CLICKED:
                canvas.create_rectangle(x*col,x*row,x*(col+1),x*(row+1),fill="white")
            if grid[row][col] == SHIP_UNCLICKED and showShips==False:
                canvas.create_rectangle(x*col,x*row,x*(col+1),x*(row+1),fill="blue")
    return


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    if ship[0][1] == ship[1][1] == ship[2][1]:
        if (ship[1][0]-ship[0][0]) and (ship[2][0]-ship[1][0]) == EMPTY_UNCLICKED:
            return True
    return False



'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if ship[0][0] == ship[1][0] == ship[2][0] and (ship[1][1]-ship[0][1]) == (ship[2][1]-ship[1][1]):
        return True
    return False


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    x= int(event.x/data["cell-size"])
    y= int(event.y/data["cell-size"])
    return [y,x] 


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for i in range(len(ship)):
       canvas.create_rectangle(data["cell-size"]*(ship[i][1]), data["cell-size"]*(ship[i][0]), data["cell-size"]*(ship[i][1]+1), data["cell-size"]*(ship[i][0]+1), fill="white")
    return


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if checkShip(grid,ship) and (isVertical(ship) or isHorizontal(ship)):
        return True
    return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["User-board"], data["temp_boat"]):
        for i in data["temp_boat"]:
            data["User-board"][i[0]][i[1]] = SHIP_UNCLICKED
        data["user_track"]+=1
    else:
        print("error: ship is invalid")
    data["temp_boat"] = []
    return



'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["user_track"] == 5:      
        print("you can start the game!")
        return
    for ship in data["temp_boat"]:
        if [row,col] == ship:
            return
    data["temp_boat"].append([row,col])
    if len(data["temp_boat"]) == 3:
        placeShip(data)
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    x= board[row][col]
    if x == SHIP_UNCLICKED:
        x = SHIP_CLICKED
    elif x == EMPTY_UNCLICKED:
        x = EMPTY_CLICKED
    board[row][col] =x 
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["computer"][row][col] == SHIP_CLICKED or data["computer"][row][col] == EMPTY_CLICKED:
        return
    else:
        updateBoard(data,data["computer"],row,col,"user")
    x = getComputerGuess(data["User-board"])
    updateBoard(data,data["User-board"],x[0],x[1],"comp")
    return


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    row = random.randint(0,9)
    col = random.randint(0,9)
    print(row,col)
    while board[row][col] == SHIP_CLICKED or board[row][col] == EMPTY_CLICKED:
        row = random.randint(0,9)
        col = random.randint(0,9)
    if board[row][col] == SHIP_UNCLICKED or board[row][col] == EMPTY_UNCLICKED:
        return(row,col)


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    return


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
   
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    ## Finally, run the simulation to test it manually ##
     runSimulation(500, 500)
    # test.testGetComputerGuess()
