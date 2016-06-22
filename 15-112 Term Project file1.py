from tkinter import *
import random



def init(data):
    data.bg = "black" # Background color
    data.cursorX = 0
    data.cursorY = 0
    data.brushPos = []
    data.redo = []
    data.brushCol = "white"
    data.brushType = "circle"
    data.isPressed = False

def mousePressed(event, data):
    data.brushPos.append([])

def mouseHeld(event, data):
    data.brushPos[-1].append((event.x,event.y))
    
def mouseMoved(event, data):
    data.cursorX = event.x
    data.cursorY = event.y

def undo(event, data):
    if len(data.brushPos) > 0:
        data.redo.append(data.brushPos.pop())
    
def redo(event, data):
    if len(data.redo) > 0:
        data.brushPos.append(data.redo.pop())
    
def keyPressed(event, data):
    pass

def brushTypes(data):
    brush = data.brushType
    # if brush = ""

def timerFired(data):
    pass
    
def drawBrush(canvas,x,y):
    r = 5
    canvas.create_oval(x-r,y-r,x+r,y+r,fill = "white")
    
def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill = data.bg)
    
    drawBrush(canvas,data.cursorX,data.cursorY)
    
    for i in data.brushPos:
        for j in i:
            (x,y) = (j)
            drawBrush(canvas,x,y)
        

########################################################################
#                          my run function
########################################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mouseMovedWrapper(event, canvas, data):
        mouseMoved(event, data)
        redrawAllWrapper(canvas, data)
    
    def mouseHeldWrapper(event, canvas, data):
        mouseHeld(event, data)
        redrawAllWrapper(canvas, data)
    
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
    
    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
        
    def undoWrapper(event, canvas, data):
        print(data.brushPos)
        undo(event, data)
        redrawAllWrapper(canvas, data)    
            
    def redoWrapper(event, canvas, data):
        redo(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Motion>", lambda event:
                            mouseMovedWrapper(event, canvas, data))
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event:
                            mouseHeldWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Control-z>", lambda event:
                            undoWrapper(event, canvas, data))
    root.bind("<Control-r>", lambda event:
                            redoWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(300, 300)