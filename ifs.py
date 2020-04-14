import tkinter as tk
import time
import random

moreDots = 1




class ChaosGame(object):

    def __init__(self, root, ratio):
        #make canvas
        self.canvas = tk.Canvas(root, width = 600, height = 600)
        self.canvas.pack()

        # make list of vertices
        self.vertices = [(5, 5), (5, 300), (300, 5)]

        self.ratio = ratio
        self.currentPoint = ()



    #Chaos game:

    #start with three vertices as points of the triangle (red, blue, green)
    #randomly choose one of the points (this is the seed)
    #randomly choose another point - draw a point halfway between the seed point and this point
    # then repeat, each time moving the previous point half the distance to the vertex which is chosen
    # (throw out the first few points)


    def drawStartingPoints(self):
        # draws the initial vertices
        for vertex in self.vertices:
            self.drawPoint(vertex, 5) # draws point

    def drawPoint(self, vertex, size):
        # draws a point on the canvas
        x = vertex[0]
        y = vertex[1]
        self.canvas.create_oval(x, y, x+size, y+size, fill='black') # creates points
        self.canvas.pack() # organizes widget blocks before placing in parent widget


    def initializePoint(self):
        # randomly chooses 2 vertices
        seed = random.choice(self.vertices)
        point1 = random.choice(self.vertices)

        # applies contraction transformations on these vertices
        self.applyTransformation(seed, point1)

    #TODO: figure out the correct contraction equations for generalized r
    def contraction1(self, point1, point2):
        # transformation scales towards the origin
        r = self.ratio
        x = (point1[0] + point2[0])/r
        y = (point1[1] + point2[1])/r
        return (x, y) # return result of contraction

    def contraction2(self, point1, point2):
        # transformation scales and translates right
        r = self.ratio
        x = (point1[0] + point2[0])/r + r
        y = (point1[1] + point2[1])/r
        return (x, y) # return result of contraction

    def contraction3(self, point1, point2):
        # transformation scales and translates up diagonally to the right
        r = self.ratio
        x = (point1[0] + point2[0])/r + 0.5*r
        y = (point1[1] + point2[1])/r + 0.5*r
        return (x, y) # return result of contraction


    def applyTransformation(self, point1, point2):
        # apply each of the three contractions to the point
        newPoint1 = self.contraction1(point1, point2)
        newPoint2 = self.contraction2(newPoint1, point2)
        newPoint3 = self.contraction3(newPoint2, point2)
        self.currentPoint = newPoint3
        self.drawPoint(newPoint3, 3) # draw the translated point




    def play(self):
        #executes the chaos game algorithm

        self.drawStartingPoints()
        self.initializePoint()

        while (moreDots == 1):
            self.applyTransformation(self.currentPoint, random.choice(self.vertices))

            self.canvas.update()
            time.sleep(0.01)


        root.bind("<Button-1>", switch)



#TODO: the off switch doesn't work anymore, I'm not sure why
def switch(event):
    # print("I am happen now!!!! ")
    global moreDots
    moreDots = 0



def preChaosScreen():
    #screen to input contraction ratio before playing game

    chaosButton.pack_forget() #hide the "let's play the chaos game" button


    #create box for user to input contraction ratio
    ratioLabel = tk.Label(root, text="What contraction ratio do you want? Input an integer value.")
    ratioLabel.grid(row=0)
    ratioEntry = tk.Entry(root)
    ratioEntry.grid(row=0, column=1)


    def executeChaos():
        #get the input from the entry field
        ratio = ratioEntry.get()
        ratio = int(ratio) #TODO: check for improper (non-integer) inputs
        print("the ratio is, ", ratio)

        #hide the input fields from previous screen
        ratioLabel.grid_forget()
        ratioEntry.grid_forget()
        ratioSubmit.grid_forget()

        #play chaos game
        game = ChaosGame(root, ratio)
        game.play()



    ratioSubmit = tk.Button(root, text="Submit", command=executeChaos)
    ratioSubmit.grid(row=0, column=2)




if __name__ == '__main__':


    root = tk.Tk() #make main window


    #make Chaos game button
    chaosButton = tk.Button(root, text= "Let's play the Chaos Game", command=preChaosScreen)
    chaosButton.pack()


    # #make input your own transformation(s) button
    # otherButton = tk.Button(root, text="Enter a custom transformation", command=transformationScreen)
    # otherButton.pack()
    #


    root.mainloop()
