import tkinter as tk
from tkinter import messagebox, Tk, Canvas, Frame, BOTH, LEFT, BOTTOM, TOP, X, Button, Label, Entry, Text
import time
import random
from fractions import Fraction

# interface colors
DEFAULT_BUTTON_COLOR = 'gray85' #colors: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
CLICKED_BUTTON_COLOR = 'IndianRed3'
CANVAS_COLOR = 'snow'

# drawing/canvas constants
WIDTH = 800 #canvas dimensions
HEIGHT = 800
LARGE_POINT_SIZE = 5 #size to draw vertices
POINT_SIZE = 1 #size to draw each point
DRAW_SPEED = 0.000001 #wait length between drawing points
RADIUS = 400
CENTER = (400, 400) # center of the starting vertices


DRAW_COLOR_LIST = ['#00aedb', '#a200ff', '#f47835', '#332C96', '#8ec127', '#d41243'] #source: https://www.color-hex.com/color-palette/471 (with a sixth color added from  https://www.schemecolor.com/faster-and-sharper.php)

#vertex lists
# vertices source: https://mathopenref.com/coordpolycalc.html
# #  cenntered at (300, 300) r=300
# TRIANGLE = [(300, 0), (40, 450), (560,450)]
# SQUARE = [(512,88), (88,88), (88,512), (512,512)]
# PENTAGON = [(300,0), (15,207), (124,543), (476,543), (585,207)]

# vertex lists
# centered at (400, 400) r=400
TRIANGLE = [(400, 0), (54, 600), (746,600)]
SQUARE = [(683,117), (117,117), (117,683), (683,683)]
PENTAGON = [(400,0), (20,276), (165,724), (635,724), (780,276)]
HEXAGON = [(600,54), (200,54), (0,400), (200,746), (600,746), (800,400)] #TODO: can't quite see the bottom vertices


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
        elif shape == 'hexagon':
            return HEXAGON

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

class FractalTransform():

    def __init__(self, matrixInputFrame):
        data = []
        for item in matrixInputFrame.allFields:
            entry = float(item.get())
            data.append(entry)

        self.contraction = [[data[0], data[1]], #2x2 matrix
                            [data[2], data[3]]]

        self.translation = [[data[4]], #1x2 matrix
                            [data[5]]]

        self.probability = data[6]  #a float value between 0 and 1


    def transformPoint(self, point): #
        '''takes in a point in the form (x, y), applies itself to the point: [contraction]*[point] + [translation]. returns the result'''
        a = self.contraction[0][0]
        b = self.contraction[0][1]
        c = self.contraction[1][0]
        d = self.contraction[1][1]


        e = self.translation[0][0]
        f = self.translation[1][0]

        x = point[0]
        y = point[1]

        newX = a*x + b*y + e
        newY = c*x + d*y + f

        print("newX and newY", newX, newY)
        return (newX, newY)

class IFS3():
    def __init__(self, transformList):
        self.listOfTransforms = transformList #list of FractalTransforms
        self.currentPoint = (0, 0)


    def pickTransformation(self):
        #extract probabilities from each transformation
        p1 = self.listOfTransforms[0].probability
        p2 = self.listOfTransforms[1].probability
        p3 = self.listOfTransforms[2].probability

        #choose a random number between 0 and 1
        n = random.random()
        # if n is between 0 and p1, choose transformation 1
        if n < p1:
            return self.listOfTransforms[0]
        # elif n is between p1 and p1 + p2, choose transformation 2
        elif n < (p1 + p2):
            return self.listOfTransforms[1]
        # else, choose transformation 3
        elif n < (p1 + p2 + p3):
            return self.listOfTransforms[2]
        else:
            return self.listOfTransforms[3]


    def iterateIFS(self):
        '''Iterates the IFS by one step. Randomly chooses one of the three transformations to apply
        (based on the probability of each one) and applies that transformation to the current point'''
        # pick which transformation to apply
        transformation = self.pickTransformation()
        #apply that transformation to the current point and update current point
        self.currentPoint = transformation.transformPoint(self.currentPoint)

class MatrixInputFrame(Frame):

    def __init__(self, number):
        super().__init__()

        self.initUI(number)

    def initUI(self, number):

        for n in range(12):
            self.columnconfigure(n, pad=3)

        for n in range(4):
            self.rowconfigure(n, pad=3)


        label1 = Label(self, text="Transformation "+str(number))
        label1.grid(row=0)


        paren1 = Label(self, text="(")
        paren1.config(font=("Courier", 22))
        paren1.grid(row=1, column=0, rowspan=2, sticky=tk.E)


        aEntry = Entry(self)
        aEntry.grid(row=1, column=1)
        bEntry = Entry(self)
        bEntry.grid(row=1, column=2)
        cEntry = Entry(self)
        cEntry.grid(row=2, column=1)
        dEntry = Entry(self)
        dEntry.grid(row=2, column=2)


        paren2 = Label(self, text=")")
        paren2.config(font=("Courier", 22))
        paren2.grid(row=1, column=3, rowspan=2, sticky=tk.W)


        paren3 = Label(self, text="(")
        paren3.config(font=("Courier", 22))
        paren3.grid(row=1, column=4, rowspan=2, sticky=tk.E)

        xLabel = Label(self, text= "x")
        xLabel.grid(row=1, column= 5)
        yLabel = Label(self, text= "y")
        yLabel.grid(row=2, column= 5)

        paren4 = Label(self, text=")")
        paren4.config(font=("Courier", 22))
        paren4.grid(row=1, column=6, rowspan=2, sticky=tk.W)


        addLabel = Label(self, text="+")
        addLabel.config(font=("Courier", 16))
        addLabel.grid(row=1, column=7, rowspan=2)


        paren5 = Label(self, text="(")
        paren5.config(font=("Courier", 22))
        paren5.grid(row=1, column=8, rowspan=2, sticky=tk.E)

        eEntry = Entry(self)
        eEntry.grid(row=1, column=9)
        fEntry = Entry(self)
        fEntry.grid(row=2, column=9)

        paren6 = Label(self, text=")")
        paren6.config(font=("Courier", 22))
        paren6.grid(row=1, column=10, rowspan=2, sticky=tk.W)

        pLabel = Label(self, text="p = ")
        pLabel.config(font=("Courier", 16))
        pLabel.grid(row = 3, column=7, columnspan=2)

        pEntry = Entry(self)
        pEntry.grid(row=3, column=9)

        self.allFields = [aEntry, bEntry, cEntry, dEntry, eEntry, fEntry, pEntry]

class GUI(Frame):

    def __init__(self, root):

        Frame.__init__(self, root)
        self.root = root

        self.packedWidgets = []
        self.shape_button_list = []

        # variables I use to keep track of whether something happened or not
        self.moreDots = 1
        self.aButtonWasPressed = 0

        self.color = 0
        self.shape = ''

        self.screenDict = {'home': self.homeScreen, 'preChaos': self.preChaosScreen, 'transform': self.inputTransformation}


        self.homeScreen()

############### GENERAL METHODS ####################
    def homeScreen(self):


        welcome = Text(root, height=18)
        self.packWidget(welcome)
        welcome.insert(tk.END, "Welcome to an interactive exploration of Iterated Fractal Systems (IFS) \nby Jenna and Cassidy!\n\nFor some math background, an IFS is a complete metric space paired with a\nfinite set of contraction mappings. A cool theorem states that the set of\nall contraction mappings of an IFS is also a contraction mapping (resulting\nin fractals!). Because of this, every IFS has a unique fixed point called\nan attractor. In other words, an IFS is a metric space that consists of many\nsequences that converge to exactly one unique fixed point called an attractor.\n\nIn this interactive tool, we hope to help you understand fractals better by\ngiving you the tools to visualize how a fractal is generated. We have 2 options\nbelow: playing with preset options that produce fractals for different polygons\nusing the Chaos Game, or entering custom transformations that creates your own\nfractal pattern for a triangle.\n\nFeel free to choose between the 2 options by clicking 1 of the butons below! ")
        #make Chaos game button
        chaosButton = Button(root, text= "Let's play the Chaos Game", command=self.preChaosScreen)
        self.packWidget(chaosButton)

        # #make input your own transformation(s) button
        otherButton =  Button(root, text="Enter a custom transformation", command=self.inputTransformation)
        self.packWidget(otherButton)

    def goBacktoHomeScreen(self):
        '''takes us back to the home screen'''
        self.previousScreen = 'home'
        self.goBack()

    def packWidget(self, widget, pady=1):
        '''packs a widget (adds to GUI) and adds it to the list of currently packed widgets'''
        widget.pack(pady=pady)
        self.packedWidgets.append(widget)

    def hidePackedWidgets(self):
        '''hides all the widgets in the list of packed widgets and clears the list'''
        for widget in self.packedWidgets:
            widget.pack_forget()
        self.packedWidgets.clear()

    def goBackButtons(self):
        #go back button
        backButton = Button(root, text="Go Back", bg=DEFAULT_BUTTON_COLOR, command=self.goBack)
        homeButton = Button(root, text="Home", bg=DEFAULT_BUTTON_COLOR, command=self.goBacktoHomeScreen)

        self.packWidget(backButton)
        self.packWidget(homeButton)

    def goBack(self):
        self.moreDots = 0
        self.color = 0
        self.hidePackedWidgets()

        #TODO: make better
        if self.previousScreen == 'preChaos' or self.previousScreen == 'transform':
            self.canvas.delete("all")
        #go to whatever the previous screen was
        self.screenDict[self.previousScreen]()

    def createCanvas(self):
        self.canvas = Canvas(self.root,
                            width = WIDTH,
                            height = HEIGHT,
                            bg = CANVAS_COLOR)
        # self.canvas.pack(fill=BOTH, side=TOP)
        self.packWidget(self.canvas)

#############CHAOS GAME METHODS####################
    #functions to set which shape we'll play the chaos game with
    def setTriangle(self):
        self.aButtonWasPressed = 1

        self.shape = 'triangle'
        for button in self.shape_button_list:
            button['background'] = DEFAULT_BUTTON_COLOR
        self.shape_button_list[0]['background']= CLICKED_BUTTON_COLOR

    def setSquare(self):
        self.aButtonWasPressed = 1

        self.shape = 'square'
        for button in self.shape_button_list:
            button['background'] = DEFAULT_BUTTON_COLOR
        self.shape_button_list[1]['background']= CLICKED_BUTTON_COLOR

    def setPentagon(self):
        self.aButtonWasPressed = 1

        self.shape = 'pentagon'
        for button in self.shape_button_list:
            button['background'] = DEFAULT_BUTTON_COLOR
        self.shape_button_list[2]['background']= CLICKED_BUTTON_COLOR

    def setHexagon(self):
        self.aButtonWasPressed = 1

        self.shape = 'hexagon'
        for button in self.shape_button_list:
            button['background'] = DEFAULT_BUTTON_COLOR
        self.shape_button_list[3]['background']= CLICKED_BUTTON_COLOR

    def drawPoint(self, vertex, point_size = POINT_SIZE, color_fill='black'):
        '''draws a point on the canvas'''
        x = vertex[0]
        y = vertex[1]
        self.canvas.create_oval(x, y, x+point_size, y+point_size, outline=color_fill, fill=color_fill) # creates points

    def preChaosScreen(self):
        self.previousScreen = 'home'
        self.hidePackedWidgets() #clear previous widgets

        explanationText = Text(root, height=6)
        explanationText.insert(tk.END, "Chaos Game is a recursive algorithm that produces fractals. It starts by\nchoosing a random point inside a regular n-sided polygon, such as a triangle,\nsquare, pentagon, or hexagon. Then, draw the next point a fraction (contraction\nratio) of the distance between the first random point and a randomly chosen\nvertex of the n original vertices of the polygon. The process continues by\nrepeatedly drawing new points using the same fractional distance idea.")
        self.packWidget(explanationText)

        # create buttons for user to select number of vertices
        verticesLabel = Label(root, text="Select the starting configuration of vertices.")
        triButton = Button(root, text="Triangle", bg=DEFAULT_BUTTON_COLOR, command=self.setTriangle)
        squareButton = Button(root, text="Square", bg=DEFAULT_BUTTON_COLOR, command=self.setSquare)
        pentButton = Button(root, text="Pentagon", bg=DEFAULT_BUTTON_COLOR, command=self.setPentagon)
        hexButton = Button(root, text="Hexagon", bg=DEFAULT_BUTTON_COLOR, command=self.setHexagon)


        self.shape_button_list = [triButton, squareButton, pentButton, hexButton]

        #create box for user to input contraction ratio
        ratioLabel = Label(root, text="Enter a fraction. This is your contraction ratio.")
        noteLabel = Label(root, text="(Note: contraction ratios less than 1 tend to work best)")

        self.ratioNum = Entry(root)
        ratioDash = Label(root, text="/")
        self.ratioDenom = Entry(root)

        # button to add coloring
        self.colorToggle = Button(root, text="Add coloring", bg=DEFAULT_BUTTON_COLOR, command=self.toggleColor)

        #submit button
        ratioSubmit = Button(root, text="Submit", bg=DEFAULT_BUTTON_COLOR, command=self.executeChaos)

        #keep track of all the widgets in a list
        self.preChaosWidgets = [verticesLabel, triButton, squareButton, pentButton, hexButton, ratioLabel, noteLabel, self.ratioNum, ratioDash, self.ratioDenom, self.colorToggle, ratioSubmit]

        for widget in self.preChaosWidgets:
            self.packWidget(widget)

        self.goBackButtons()

    def toggleColor(self):
        if self.color == 0:
            #change button color to pressed
            self.colorToggle['background'] = CLICKED_BUTTON_COLOR
        else:
            #change button color to white
            self.colorToggle['background'] = DEFAULT_BUTTON_COLOR
        self.color += 1
        self.color = self.color % 2

    def executeChaos(self):
        '''creates the screen that comes after the user inputs their settings.
        sets up the canvas and checks to make sure the inputs were valid. then
        displays the chaos game on the screen '''
        #get the input from the entry fields
        numerator = self.ratioNum.get()
        denominator = self.ratioDenom.get()

        self.hidePackedWidgets() #clear previous widgets
        self.previousScreen = 'preChaos'

        self.goBackButtons()
        self.createCanvas()

        if not(numerator.isnumeric() and denominator.isnumeric()): #if the input is not an integer, give a warning box
             messagebox.showinfo("Error", "Inputs must be integers!")

        elif self.aButtonWasPressed == 0:
            messagebox.showinfo("Error", "Please choose a number of vertices!")

        else:
            numerator = int(numerator)
            denominator = int(denominator)

            ratio = Fraction(numerator, denominator)

            self.aButtonWasPressed = 0
            game = ChaosGame(ratio, self.shape)
            self.playChaos(game)

    def playChaos(self, game):
        '''iterates the chaos game and draws a point after each iteration'''
        for vertex in game.vertices: #draw the vertices
            self.drawPoint(vertex, LARGE_POINT_SIZE)

        game.initializePoint() #set first point
        self.drawPoint(game.currentPoint, POINT_SIZE) # draw point


        self.moreDots = 1

        while self.moreDots == 1:
            vertexIndex = random.choice(range(len(game.vertices)))
            currentVertex = game.vertices[vertexIndex]
            game.applyTransformation(game.currentPoint, currentVertex)

            if self.color == 1:
                currentColor = DRAW_COLOR_LIST[vertexIndex]
                self.drawPoint(game.currentPoint, POINT_SIZE, currentColor) # draw the translated point
            else:
                self.drawPoint(game.currentPoint, POINT_SIZE) # draw the translated point

            self.canvas.update()
            time.sleep(DRAW_SPEED)

    def goBacktoPreChaos(self):
        '''takes us back to the screen for inputting settings'''
        self.moreDots = 0
        self.color = 0
        self.canvas.delete("all")

        self.hidePackedWidgets()
        self.preChaosScreen()

################## Input your own Transformation Methods ##########################

    def inputTransformation(self):
        '''screen for inputting the transformations'''
        self.hidePackedWidgets() #clear previous widgets
        #go back button
        self.previousScreen = 'home'

        self.goBackButtons()

        explanationText = Text(root, height=15)
        explanationText.insert(tk.END, "Fractals can be created by using probability and recursion of transformations.\nEssentially, you can create a fractal by applying set transformations, each with\nan associated probability of occurring, to produce new points (with x-coordinate\nand y-coordinate). This means that every time you produce a new point, it is\ndone by applying a transformation that is determined based on its probability of\nbeing chosen.\n\nIn this case, you can create 3 different transformations, each of which you can set its probability (p) of occurring. Each transformation consists of a scaling matrix (4 inputs), which scale the x- and y-coordinates, as well as a\ntranslation vector, which shifts the x- and y-coordinates.\n\nNote: The transformations create cooler fractals when the input values are less than 1. Also, the probabilities (p) must sum to 1.")
        self.packWidget(explanationText)

        self.inputFrames = []
        for n in range(1, 5):
            inputFrame = MatrixInputFrame(n)
            self.inputFrames.append(inputFrame)
            self.packWidget(inputFrame, pady=10)


        submit = Button(root, text="Submit", bg=DEFAULT_BUTTON_COLOR, command=self.drawCustomTransformsScreen)
        self.packWidget(submit)


    def drawCustomTransformsScreen(self):
        '''draws the results of the inputted transformations'''
        # create each transformation object

        transformList = []
        for i in range(len(self.inputFrames)):
            transformList.append(FractalTransform(self.inputFrames[i]))

        # create the set of transformations object (IFS3)
        ifsObj = IFS3(transformList)

        self.hidePackedWidgets()
        #TODO: check that probabilities all add up to 1
        #TODO: if a field wasn't filled, automatically populate it with 0

        self.previousScreen = 'transform'
        self.goBackButtons()

        self.createCanvas()

        self.moreDots = 1
        while self.moreDots == 1:

            #draw point
            barnsleyDomain = (-2.1820, 2.6558)
            barnsleyRange = (0, 9,9983)
            pointToDraw = shiftPoint(ifsObj.currentPoint, barnsleyDomain, barnsleyRange, (100, 500), (100, 500))
            print("drawing this point: ", pointToDraw)
            self.drawPoint(pointToDraw)
            #iterate IFS
            ifsObj.iterateIFS()

            self.canvas.update()
            time.sleep(DRAW_SPEED)


def shiftPoint(point, oldDomain, oldRange, newDomain, newRange):
    '''oldRange is pair of y values, so is newRange. Domain the same but with y values'''
    xNew = (point[0] - oldDomain[0]) * (newDomain[1] - newDomain[0])/(oldDomain[1]- oldDomain[0])
    yNew = (point[1] - oldRange[0]) * (newRange[1]- newRange[0])/ (oldRange[1]- oldRange[0])
    return (xNew, yNew)


if __name__ == '__main__':

    root = Tk() #make main window

    root.state('zoomed') #maximize window
    root.title("Math 181 Final Project")

    #game.start()

    gui = GUI(root) #initialize buttons and stuff

    root.mainloop()
