import tkinter as tk
from tkinter import messagebox, Tk, Canvas, Frame, BOTH, TOP
import time
import random
from fractions import Fraction

#canvas dimensions
WIDTH = 800
HEIGHT = 800


moreDots = 1
aButtonWasPressed = 0

LARGE_POINT_SIZE = 5 #size to draw vertices
POINT_SIZE = 1 #size to draw each point
DRAW_SPEED = 0.0001 #wait length between drawing points
CENTER = (400, 400) # center of the starting vertices


#vertex lists
# vertices source: https://mathopenref.com/coordpolycalc.html
# #  cenntered at (300, 300) r=300
# TRIANGLE = [(300, 0), (40, 450), (560,450)]
# SQUARE = [(512,88), (88,88), (88,512), (512,512)]
# PENTAGON = [(300,0), (15,207), (124,543), (476,543), (585,207)]


TRIANGLE = [(400, 0), (54, 600), (746,600)]
SQUARE = [(683,117), (117,117), (117,683), (683,683)]
PENTAGON = [(400,0), (20,276), (165,724), (635,724), (780,276)]



# interface colors
DEFAULT_BUTTON_COLOR = 'PaleTurquoise1' #colors: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
CLICKED_BUTTON_COLOR = 'IndianRed3'
CANVAS_COLOR = 'thistle1'

class ChaosGame(object):


    def __init__(self, ratio, shape):

        self.vertices = self.setVertices(shape)


        self.ratio = ratio #ratio = a fraction
        self.currentPoint = ()


    def setVertices(self, shape):
        '''makes list of vertices'''
        if shape == 'triangle':
            return TRIANGLE
        elif shape == 'square':
            return SQUARE
        elif shape == 'pentagon':
            return PENTAGON


    #Chaos game:

    #start with three vertices as points of the triangle (red, blue, green)
    #randomly choose one of the points (this is the seed)
    #randomly choose another point - draw a point halfway between the seed point and this point
    # then repeat, each time moving the previous point half the distance to the vertex which is chosen
    # (throw out the first few points)

    #
    #
    # def drawStartingPoints(self):
    #     '''draws the initial vertices'''
    #     for vertex in self.vertices:
    #         self.drawPoint(vertex, 5) # draws point

    def initializePoint(self):
        '''plays the first iteration of the Chaos game'''
        # randomly chooses 2 vertices
        seed = random.choice(self.vertices)
        point1 = random.choice(self.vertices)

        # applies contraction transformations on these vertices
        self.applyTransformation(seed, point1)


    def contraction1(self, point1, point2):

        # transformation scales towards the origin
        r = self.ratio
        x = float((point1[0] + point2[0]) * r)
        y = float((point1[1] + point2[1]) * r)
        return (x, y) # return result of contraction


    def moveToOrigin(self, point):
        return (point[0] - CENTER[0], point[1] - CENTER[1])

    def moveFromOrigin(self, point):
        return (point[0] + CENTER[0], point[1] + CENTER[1])


    def applyTransformation(self, point1, point2):
        '''executes a single step of the chaos game'''

        # translates the points to be centered about the origin
        point1o = self.moveToOrigin(point1)
        point2o = self.moveToOrigin(point2)

        # applies the contraction
        newPoint1 = self.contraction1(point1o, point2o)

        # translates the new, contracted point back from the origin
        newPoint1 = self.moveFromOrigin(newPoint1)
        self.currentPoint = newPoint1



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



class GUI(Frame):

    def __init__(self, root):

        Frame.__init__(self, root)
        self.root = root

        self.packedWidgets = []
        self.shape_button_list = []

        self.shape = ''

        self.homeScreen()


    #functions to set which shape we'll play the chaos game with
    def setTriangle(self):
        global aButtonWasPressed
        aButtonWasPressed = 1

        self.shape = 'triangle'
        for button in self.shape_button_list:
            button['background'] = DEFAULT_BUTTON_COLOR
        self.shape_button_list[0]['background']= CLICKED_BUTTON_COLOR

    def setSquare(self):
        global aButtonWasPressed
        aButtonWasPressed = 1

        self.shape = 'square'
        for button in self.shape_button_list:
            button['background'] = DEFAULT_BUTTON_COLOR
        self.shape_button_list[1]['background']= CLICKED_BUTTON_COLOR

    def setPentagon(self):
        global aButtonWasPressed
        aButtonWasPressed = 1

        self.shape = 'pentagon'
        for button in self.shape_button_list:
            button['background'] = DEFAULT_BUTTON_COLOR
        self.shape_button_list[2]['background']= CLICKED_BUTTON_COLOR



    def drawPoint(self, vertex, point_size, color_fill='black'):
        '''draws a point on the canvas'''
        x = vertex[0]
        y = vertex[1]
        self.canvas.create_oval(x, y, x+point_size, y+point_size, fill=color_fill) # creates points


    def homeScreen(self):
        #make Chaos game button
        chaosButton = tk.Button(root, text= "Let's play the Chaos Game", command=self.preChaosScreen)
        self.packWidget(chaosButton)

        # #make input your own transformation(s) button
        otherButton = tk.Button(root, text="Enter a custom transformation", command=self.inputTransformation)
        self.packWidget(otherButton)

        self.homeButtons = [chaosButton, otherButton]



    def preChaosScreen(self):
        self.hidePackedWidgets() #clear previous widgets


        # create buttons for user to select number of vertices
        verticesLabel = tk.Label(root, text="Select the starting number of vertices.")
        triButton = tk.Button(root, text="Triangle", bg=DEFAULT_BUTTON_COLOR, command=self.setTriangle)
        squareButton = tk.Button(root, text="Square", bg=DEFAULT_BUTTON_COLOR, command=self.setSquare)
        pentButton = tk.Button(root, text="Pentagon", bg=DEFAULT_BUTTON_COLOR, command=self.setPentagon)

        self.shape_button_list = [triButton, squareButton, pentButton]

        #
        # verticesLabel.grid(row=0)
        # triButton.grid(row=1, column=0)
        # squareButton.grid(row=1, column=1)
        # pentButton.grid(row=1, column=2)
        # ratioLabel.grid(row=2)
        # noteLabel.grid(row=3)
        # ratioNum.grid(row=4, column=0)
        # ratioDash.grid(row=4, column=1)
        # ratioDenom.grid(row=4, column=2)
        # ratioSubmit.grid(row=5, column=0)



        #create box for user to input contraction ratio
        ratioLabel = tk.Label(root, text="What contraction ratio do you want? Enter a fraction.")
        noteLabel = tk.Label(root, text="(Note: contraction ratios less than 1 tend to work best)")

        self.ratioNum = tk.Entry(root)
        ratioDash = tk.Label(root, text="/")
        self.ratioDenom = tk.Entry(root)

        ratioSubmit = tk.Button(root, text="Submit", bg=DEFAULT_BUTTON_COLOR, command=self.executeChaos)

        self.preChaosWidgets = [verticesLabel, triButton, squareButton, pentButton, ratioLabel, noteLabel, self.ratioNum, ratioDash, self.ratioDenom, ratioSubmit]

        for widget in self.preChaosWidgets:
            self.packWidget(widget)



    def executeChaos(self):
        #get the input from the entry fields
        numerator = self.ratioNum.get()
        denominator = self.ratioDenom.get()

        self.hidePackedWidgets() #clear previous widgets

        #go back button
        backButton = tk.Button(root, text="Go Back", bg=DEFAULT_BUTTON_COLOR, command=self.goBacktoPreChaos)
        homeButton = tk.Button(root, text="Home", bg=DEFAULT_BUTTON_COLOR, command=self.goBacktoHomeScreen)

        self.packWidget(backButton)
        self.packWidget(homeButton)

        self.canvas = Canvas(self.root,
                            width = WIDTH,
                            height = HEIGHT,
                            bg = CANVAS_COLOR)
        # self.canvas.pack(fill=BOTH, side=TOP)
        self.packWidget(self.canvas)

        global aButtonWasPressed

        if not(numerator.isnumeric() and denominator.isnumeric()): #if the input is not an integer, give a warning box
             messagebox.showinfo("Error", "Inputs must be integers!")

        elif aButtonWasPressed == 0:
            messagebox.showinfo("Error", "Please choose a number of vertices!")

        else:
            numerator = int(numerator)
            denominator = int(denominator)

            ratio = Fraction(numerator, denominator)

            aButtonWasPressed = 0
            game = ChaosGame(ratio, self.shape)
            self.playChaos(game)




    def playChaos(self, game):
        for vertex in game.vertices: #draw the vertices
            self.drawPoint(vertex, LARGE_POINT_SIZE)

        game.initializePoint() #set first point

        global moreDots
        moreDots = 1


        while moreDots == 1:
            self.drawPoint(game.currentPoint, POINT_SIZE) # draw the translated point
            game.applyTransformation(game.currentPoint, random.choice(game.vertices))

            self.canvas.update()
            time.sleep(DRAW_SPEED)


    def goBacktoPreChaos(self):
        global moreDots
        moreDots = 0
        self.canvas.delete("all")

        self.hidePackedWidgets()
        self.preChaosScreen()

    def goBacktoHomeScreen(self):
        global moreDots
        moreDots = 0
        self.canvas.delete("all")

        self.hidePackedWidgets()
        self.homeScreen()

    def inputTransformation(self):
        pass


    def packWidget(self, widget):
        widget.pack()
        self.packedWidgets.append(widget)



    def hidePackedWidgets(self):
        for widget in self.packedWidgets:
            widget.pack_forget()
        self.packedWidgets.clear()





if __name__ == '__main__':


    root = Tk() #make main window

    root.state('zoomed') #maximize window


    #game.start()

    gui = GUI(root) #initialize buttons and stuff



    root.mainloop()
