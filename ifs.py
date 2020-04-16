import tkinter as tk
from tkinter import messagebox
import time
import random
from fractions import Fraction

moreDots = 1

POINT_SIZE = 2 #size to draw each point
DRAW_SPEED = 0.0001 #wait length between drawing points
CENTER = (300, 300) # center of the starting vertices


class ChaosGame(object):

    def __init__(self, root, ratio):
        #make canvas
        self.canvas = tk.Canvas(root, width = 1000, height = 1000)
        self.canvas.pack()

        # make list of vertices.
        # vertices source: https://mathopenref.com/coordpolycalc.html

        # triangle
        # centered at (300, 300 )
        # self.vertices = [(300, 0),
        #                 (40, 450),
        #                 (560,450)]

        #pentagon
        # centered at (300, 300), radius = 100
        self.vertices = [(300,200),
                            (205,269),
                            (241,381),
                            (359,381),
                            (395,269)
                            ]


        self.ratio = ratio #ratio = a fraction
        self.currentPoint = ()



    #Chaos game:

    #start with three vertices as points of the triangle (red, blue, green)
    #randomly choose one of the points (this is the seed)
    #randomly choose another point - draw a point halfway between the seed point and this point
    # then repeat, each time moving the previous point half the distance to the vertex which is chosen
    # (throw out the first few points)


    def drawPoint(self, vertex, size):
        # draws a point on the canvas
        x = vertex[0]
        y = vertex[1]
        self.canvas.create_oval(x, y, x+size, y+size, fill='black') # creates points
        self.canvas.pack() # organizes widget blocks before placing in parent widget

    def drawStartingPoints(self):
        # draws the initial vertices
        for vertex in self.vertices:
            self.drawPoint(vertex, 5) # draws point

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
        x = float((point1[0] + point2[0]) * r)
        y = float((point1[1] + point2[1]) * r)
        return (x, y) # return result of contraction


    # def contraction2(self, point1, point2):
        # transformation scales and translates right
        # r = self.ratio
        # x = (point1[0] + point2[0])* r + r #TODO: r is fraction
        # y = (point1[1] + point2[1])* r
        # return (x, y) # return result of contraction

    # def contraction3(self, point1, point2):
        # transformation scales and translates up diagonally to the right
        # r = self.ratio
        # x = (point1[0] + point2[0])*r + 0.5*r #TODO: r is fraction
        # y = (point1[1] + point2[1])*r + 0.5*r
        # return (x, y) # return result of contraction


    def moveToOrigin(self, point):
        return (point[0] - CENTER[0], point[1] - CENTER[1])

    def moveFromOrigin(self, point):
        return (point[0] + CENTER[0], point[1] + CENTER[1])


    def applyTransformation(self, point1, point2):
        # apply each of the three contractions to the point
        point1o = self.moveToOrigin(point1)
        point2o = self.moveToOrigin(point2)

        newPoint1 = self.contraction1(point1o, point2o)
        # newPoint2 = self.contraction2(newPoint1, point2)
        # newPoint3 = self.contraction3(newPoint2, point2)

        newPoint1 = self.moveFromOrigin(newPoint1)
        self.currentPoint = newPoint1
        self.drawPoint(newPoint1, POINT_SIZE) # draw the translated point




    def play(self):
        #executes the chaos game algorithm

        self.drawStartingPoints()
        self.initializePoint()


        while (moreDots == 1):
            self.applyTransformation(self.currentPoint, random.choice(self.vertices))

            self.canvas.update()
            time.sleep(DRAW_SPEED)


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
    ratioLabel = tk.Label(root, text="What contraction ratio do you want?")
    ratioLabel.grid(row=0)
    ratioNumLabel = tk.Label(root, text="Numerator:")
    ratioNumLabel.grid(row=1, column=0)
    ratioNum = tk.Entry(root)
    ratioNum.grid(row=1, column=1)

    ratioDenomLabel = tk.Label(root, text="Denominator:")
    ratioDenomLabel.grid(row=1, column=2)
    ratioDenom = tk.Entry(root)
    ratioDenom.grid(row=1, column=3)



    def executeChaos():
        #get the input from the entry fields
        numerator = ratioNum.get()
        denominator = ratioDenom.get()

        if not (numerator.isnumeric() and denominator.isnumeric()): #if the input is not an integer, give a warning box
             messagebox.showinfo("Error", "Inputs must be integers!")

        else:
            numerator = int(numerator)
            denominator = int(denominator)

            ratio = Fraction(numerator, denominator)
            print("the ratio is ", ratio)

            #hide the input fields from previous screen
            ratioLabel.grid_forget()
            ratioNumLabel.grid_forget()
            ratioNum.grid_forget()
            ratioDenomLabel.grid_forget()
            ratioDenom.grid_forget()
            ratioSubmit.grid_forget()

            #play chaos game
            game = ChaosGame(root, ratio)
            game.play()



    ratioSubmit = tk.Button(root, text="Submit", command=executeChaos)
    ratioSubmit.grid(row=2, column=0)




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
