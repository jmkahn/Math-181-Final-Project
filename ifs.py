import tkinter as tk
from tkinter import messagebox, Tk, Canvas, Frame, BOTH, LEFT, RIGHT, BOTTOM, TOP, X, Button, Label, Entry, Text, DISABLED
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
CANVAS_PAD = 50 # margin on side of canvas
LARGE_POINT_SIZE = 5 #size to draw vertices
POINT_SIZE = 1 #size to draw each point
DRAW_SPEED = 0.000001 #wait length between drawing points
RADIUS = 400
CENTER = (400, 400) # center of the starting vertices

NUM_ITERATIONS = 200 # number of times to iterate before setting autoscaler (bigger = more likely to be accurate (up to a point))

DRAW_COLOR_LIST = ['#00aedb', '#a200ff', '#f47835', '#332C96', '#8ec127', '#d41243'] #source: https://www.color-hex.com/color-palette/471 (with a sixth color added from  https://www.schemecolor.com/faster-and-sharper.php)

#vertex lists
# vertices source: https://mathopenref.com/coordpolycalc.html
# #  cenntered at (300, 300) r=300
# TRIANGLE = [(300, 0), (40, 450), (560,450)]
# SQUARE = [(512,88), (88,88), (88,512), (512,512)]
# PENTAGON = [(300,0), (15,207), (124,543), (476,543), (585,207)]

# vertex lists
# centered at (400, 400) r=400
VERTEX_DICT = {'triangle': [(400, 0), (54, 600), (746,600)],
                'square': [(683,117), (117,117), (117,683), (683,683)],
                'pentagon': [(400,0), (20,276), (165,724), (635,724), (780,276)],
                'hexagon': [(600,54), (200,54), (0,400), (200,746), (600,746), (800,400)]} #TODO: can't quite see the bottom vertices


class ChaosGame(object):
    '''stores information about the chaos game and iterates points according to the rules'''

    def __init__(self, ratio, shape):
        self.vertices = self.setVertices(shape)
        self.ratio = ratio #ratio = a fraction
        self.currentPoint = ()

    def setVertices(self, shape):
        '''returns a list of vertices'''
        return VERTEX_DICT[shape]

    def initializePoint(self):
        '''plays the first iteration of the Chaos game'''
        seed = random.choice(self.vertices) # randomly chooses 2 vertices
        point1 = random.choice(self.vertices)
        self.applyTransformation(seed, point1) # applies contraction transformations on these vertices

    def contraction(self, point1, point2):
        '''returns a new point that is the (contraction ratio * the distance between the two points) from the first point'''
        # transformation scales towards the origin
        r = self.ratio
        x = float((point1[0] + point2[0]) * r)
        y = float((point1[1] + point2[1]) * r)
        return (x, y) # return result of contraction

    def moveToOrigin(self, point):
        '''translates a point so that it is centered about the origin'''
        return (point[0] - CENTER[0], point[1] - CENTER[1])

    def moveFromOrigin(self, point):
        '''undoes the translation to make the point centered about the origin'''
        return (point[0] + CENTER[0], point[1] + CENTER[1])

    def applyTransformation(self, point1, point2):
        '''executes a single step of the chaos game'''
        point1o = self.moveToOrigin(point1) # translates the points to be centered about the origin
        point2o = self.moveToOrigin(point2)
        newPoint1 = self.contraction(point1o, point2o) # applies the contraction
        self.currentPoint = self.moveFromOrigin(newPoint1) # translates the new, contracted point back from the origin

class FractalTransform():
    '''creates a linear transformation from the inputted data and stores the method to apply that transformation to a point'''

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


    def transformPoint(self, point):
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
        return (newX, newY)

class IFS3():
    def __init__(self, transformList):
        self.listOfTransforms = transformList #list of FractalTransform objects
        self.currentPoint = (0, 0)

    def pickTransformation(self):
        '''chooses a weighted random transformation based on the probability of each transformation'''
        probabilities = []
        for transform in self.listOfTransforms:
            probabilities.append(transform.probability)
        return random.choices(self.listOfTransforms, weights=probabilities)[0]

    def iterateIFS(self):
        '''Iterates the IFS by one step. Randomly chooses one of the three transformations to apply
        (based on the probability of each one) and applies that transformation to the current point'''
        # pick which transformation to apply
        transformation = self.pickTransformation()
        #apply that transformation to the current point and update current point
        self.currentPoint = transformation.transformPoint(self.currentPoint)

    def resetCurrentPoint(self):
        self.currentPoint = (0, 0)

class MatrixInputFrame(Frame):

    def __init__(self, number, master):
        super().__init__(master)
        self.initUI(number) #number refers to the index of this frame (whether it is the 1st, 2nd, etc)

    def initUI(self, number):
        '''makes the UI for the of fields and labels for inputting one transformation'''
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
        #populate all the fields with 0 to start
        # for field in self.allFields:
        #     field.insert(0, "0")

class GUI(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root

        self.packedWidgets = []
        self.shape_button_list = []

        self.moreDots = 1 # variables I use to keep track of whether certain events happened or not
        self.aButtonWasPressed = 0
        self.color = 0
        self.shape = ''

        self.screenDict = {'home': self.homeScreen, 'preChaos': self.preChaosScreen, 'transform': self.inputTransformation}


        self.homeScreen()

############### GENERAL METHODS ####################
    def goBacktoHomeScreen(self):
        '''takes us back to the home screen'''
        self.previousScreen = 'home'
        self.goBack()

    def goBack(self):
        '''takes us back to the previous screen'''
        self.moreDots = 0
        self.color = 0
        self.hidePackedWidgets()
        if self.previousScreen == 'preChaos' or self.previousScreen == 'transform': #clears the canvas if we were on a drawing screen
            self.canvas.delete("all")
        self.screenDict[self.previousScreen]() #go to whatever the previous screen was

    def packWidget(self, widget, padx=1, pady=1, side=TOP, fill=tk.NONE):
        '''packs a widget (adds to GUI) and adds it to the list of currently packed widgets'''
        widget.pack(padx=padx, pady=pady, side=side)
        self.packedWidgets.append(widget)

    def hidePackedWidgets(self):
        '''hides all the widgets in the list of packed widgets and clears the list'''
        for widget in self.packedWidgets:
            widget.pack_forget()
        self.packedWidgets.clear()

    def goBackButtons(self):
        '''creates and places the back and home buttons that appear on all the screens'''
        backFrame = Frame(root)
        self.packWidget(backFrame, side=TOP, fill=X)

        backButton = Button(backFrame, text="Go Back", bg=DEFAULT_BUTTON_COLOR, command=self.goBack)
        homeButton = Button(backFrame, text="Home", bg=DEFAULT_BUTTON_COLOR, command=self.goBacktoHomeScreen)
        backButton.pack(side=LEFT, padx=5, pady=5)
        homeButton.pack(side=LEFT, padx=5, pady=5)

    def createCanvas(self):
        '''creates and packs a canvas with set dimensions'''
        self.canvas = Canvas(self.root,
                            width = WIDTH,
                            height = HEIGHT,
                            bg = CANVAS_COLOR)
        # self.canvas.pack(fill=BOTH, side=TOP)
        self.packWidget(self.canvas)

    def homeScreen(self):
        '''creates the interface for the home screen'''
        welcome = Text(root, height=18) #welcome text box
        self.packWidget(welcome)
        welcome.insert(tk.END, "Welcome to an interactive exploration of Iterated Fractal Systems (IFS) \nby Jenna and Cassidy!\n\nFor some math background, an IFS is a complete metric space paired with a\nfinite set of contraction mappings. A cool theorem states that the set of\nall contraction mappings of an IFS is also a contraction mapping (resulting\nin fractals!). Because of this, every IFS has a unique fixed point called\nan attractor. In other words, an IFS is a metric space that consists of many\nsequences that converge to exactly one unique fixed point called an attractor.\n\nIn this interactive tool, we hope to help you understand fractals better by\ngiving you the tools to visualize how a fractal is generated. We have 2 options\nbelow: playing with preset options that produce fractals for different polygons\nusing the Chaos Game, or entering custom transformations that creates your own\nfractal pattern for a triangle.\n\nFeel free to choose between the 2 options by clicking 1 of the buttons below! ")
        welcome["state"] = DISABLED
        #make Chaos game button
        chaosButton = Button(root, text= "Let's play the Chaos Game", command=self.preChaosScreen)
        self.packWidget(chaosButton)
        # #make input your own transformation(s) button
        otherButton =  Button(root, text="Enter a custom transformation", command=self.inputTransformation)
        self.packWidget(otherButton)


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
        '''creates the screen for inputting the settings before arriving at the main chaos game'''
        self.previousScreen = 'home'
        self.aButtonWasPressed = 0
        self.hidePackedWidgets() #clear previous widgets
        self.goBackButtons()

        mainFrame = Frame(root)
        self.packWidget(mainFrame, side=TOP)

        explanationText = Text(mainFrame, height=6)
        explanationText.insert(tk.END, "Chaos Game is a recursive algorithm that produces fractals. It starts by\nchoosing a random point inside a regular n-sided polygon, such as a triangle,\nsquare, pentagon, or hexagon. Then, draw the next point a fraction (contraction\nratio) of the distance between the first random point and a randomly chosen\nvertex of the n original vertices of the polygon. The process continues by\nrepeatedly drawing new points using the same fractional distance idea.")
        explanationText["state"] = DISABLED
        #TODO: give more hints about how to play it fun
        explanationText.pack()

        # create buttons for user to select number of vertices
        vertexButtonsFrame = Frame(mainFrame)
        vertexButtonsFrame.pack(pady=15)
        verticesLabel = Label(vertexButtonsFrame, text="Select the starting configuration of vertices.")
        triButton = Button(vertexButtonsFrame, text="Triangle", bg=DEFAULT_BUTTON_COLOR, command=self.setTriangle)
        squareButton = Button(vertexButtonsFrame, text="Square", bg=DEFAULT_BUTTON_COLOR, command=self.setSquare)
        pentButton = Button(vertexButtonsFrame, text="Pentagon", bg=DEFAULT_BUTTON_COLOR, command=self.setPentagon)
        hexButton = Button(vertexButtonsFrame, text="Hexagon", bg=DEFAULT_BUTTON_COLOR, command=self.setHexagon)

        self.shape_button_list = [triButton, squareButton, pentButton, hexButton]

        verticesLabel.grid(columnspan=2)
        triButton.grid(row=1, column=0, padx=5, pady=5)
        squareButton.grid(row=1, column=1, padx=5, pady=5)
        pentButton.grid(row=2, column=0, padx=5, pady=5)
        hexButton.grid(row=2, column=1, padx=5, pady=5)


        #create box for user to input contraction ratio
        ratioFrame = Frame(mainFrame)
        ratioFrame.pack(pady=15)
        ratioLabel = Label(ratioFrame, text="Enter a fraction. This is your contraction ratio.")
        noteLabel = Label(ratioFrame, text="(Note: contraction ratios less than 1 tend to work best)")
        ratioLabel.pack()
        noteLabel.pack()

        fractionFrame = Frame(ratioFrame)
        fractionFrame.pack(side=BOTTOM)
        self.ratioNum = Entry(fractionFrame, bd=3, width =4)
        self.ratioNum.pack(side=LEFT)
        ratioDash = Label(fractionFrame, text="/")
        ratioDash.pack(side=LEFT)
        self.ratioDenom = Entry(fractionFrame, bd=3, width=4)
        self.ratioDenom.pack(side=LEFT)

        # button to add coloring
        self.colorToggle = Button(mainFrame, text="Add coloring", bg=DEFAULT_BUTTON_COLOR, command=self.toggleColor)
        self.colorToggle.pack(pady=10)

        #submit button
        ratioSubmit = Button(mainFrame, text="Submit", bg=DEFAULT_BUTTON_COLOR, command=self.executeChaos)
        ratioSubmit.pack()

    def toggleColor(self):
        if self.color == 0:
            #change button color to pressed
            self.colorToggle['background'] = CLICKED_BUTTON_COLOR
        else:
            #change button color to white
            self.colorToggle['background'] = DEFAULT_BUTTON_COLOR
        self.color = (self.color + 1) % 2

    def executeChaos(self):
        '''creates the screen that comes after the user inputs their settings.
        sets up the canvas and checks to make sure the inputs were valid. then
        displays the chaos game on the screen '''
        #get the input from the entry fields
        numerator = self.ratioNum.get()
        denominator = self.ratioDenom.get()

        self.hidePackedWidgets() #clear previous widgets
        self.goBackButtons()
        self.previousScreen = 'preChaos'
        self.createCanvas()

        if not(numerator.isnumeric() and denominator.isnumeric()): #if the input is not an integer, give a warning box
             messagebox.showinfo("Error", "Inputs must be integers!")

        elif self.aButtonWasPressed == 0:
            messagebox.showinfo("Error", "Please choose a number of vertices!")

        else:
            ratio = Fraction(int(numerator), int(denominator))
            game = ChaosGame(ratio, self.shape)
            self.playChaos(game)

    def playChaos(self, game):
        '''iterates the chaos game and draws a point after each iteration'''
        for vertex in game.vertices: #draw the vertices
            self.drawPoint(vertex, LARGE_POINT_SIZE)

        game.initializePoint() #set first point
        self.drawPoint(game.currentPoint, POINT_SIZE) # draw point #TODO: the first point is black even when color is on

        self.moreDots = 1
        while self.moreDots == 1:
            vertexIndex = random.choice(range(len(game.vertices)))
            currentVertex = game.vertices[vertexIndex]
            game.applyTransformation(game.currentPoint, currentVertex)

            if self.color == 1: #if coloring is turned on
                currentColor = DRAW_COLOR_LIST[vertexIndex]
                self.drawPoint(game.currentPoint, POINT_SIZE, currentColor) # draw the translated point
            else:
                self.drawPoint(game.currentPoint, POINT_SIZE) # draw the translated point

            self.canvas.update()
            time.sleep(DRAW_SPEED)

################## Input your own Transformation Methods ##########################

    def inputTransformation(self):
        '''screen for inputting the transformations'''
        self.hidePackedWidgets() #clear previous widgets
        #go back button
        self.previousScreen = 'home'

        self.goBackButtons()

        explanationText = Text(root, height=15)
        explanationText.insert(tk.END, "Fractals can be created by using probability and recursion of transformations.\nEssentially, you can create a fractal by applying set transformations, each with\nan associated probability of occurring, to produce new points (with x-coordinate\nand y-coordinate). This means that every time you produce a new point, it is\ndone by applying a transformation that is determined based on its probability of\nbeing chosen.\n\nIn this case, you can create 3 different transformations, each of which you can set its probability (p) of occurring. Each transformation consists of a scaling matrix (4 inputs), which scale the x- and y-coordinates, as well as a\ntranslation vector, which shifts the x- and y-coordinates.\n\nNote: The transformations create cooler fractals when the input values are less than 1. Also, the probabilities (p) must sum to 1.") #TODO: fix this text
        explanationText["state"] = DISABLED #make it non-editable
        self.packWidget(explanationText)

        transformationsFrame = Frame(root)
        self.packWidget(transformationsFrame)

        self.inputFrames = []
        for n in range(1, 5):
            inputFrame = MatrixInputFrame(n, transformationsFrame)
            self.inputFrames.append(inputFrame)
            inputFrame.pack(pady=10)


        buttonFrame = Frame(root)
        self.packWidget(buttonFrame)
        submit = Button(buttonFrame, text="Submit", bg=DEFAULT_BUTTON_COLOR, command=self.drawCustomTransformsScreen)
        submit.pack()

        # zeros = Button(buttonFrame, text="Fill blanks", bg=DEFAULT_BUTTON_COLOR, command=self.fillZeros)
        # zeros.pack()


    def drawCustomTransformsScreen(self):
        '''draws the results of the inputted transformations'''
        # create each transformation object

        transformList = []
        for i in range(len(self.inputFrames)):
            transformList.append(FractalTransform(self.inputFrames[i])) #TODO: error  here when making FractalTransforms

        # create the set of transformations object (IFS3)
        ifsObj = IFS3(transformList)

        self.hidePackedWidgets()
        #TODO: check that probabilities all add up to 1
        #TODO: if a field wasn't filled, automatically populate it with 0

        self.previousScreen = 'transform'
        self.goBackButtons()

        self.createCanvas()

        dim = self.autoScale(ifsObj)

        self.moreDots = 1
        while self.moreDots == 1:

            #draw point
            # barnsleyDomain = (-2.1820, 2.6558)
            # barnsleyRange = (0, 9,9983)

            pointToDraw = self.shiftPoint(ifsObj.currentPoint, dim)
            self.drawPoint(pointToDraw)
            #iterate IFS
            ifsObj.iterateIFS()

            self.canvas.update()
            time.sleep(DRAW_SPEED)


    def autoScale(self, ifsObj):
        extremeValues = [0, 0, 0, 0] #list with format minX, maxX, minY, maxY
        iterations = 0

        while iterations < NUM_ITERATIONS:
            ifsObj.iterateIFS()

            x = ifsObj.currentPoint[0]
            y = ifsObj.currentPoint[1]

            if x < extremeValues[0]:
                extremeValues[0] = x
            if x > extremeValues[1]:
                extremeValues[1] = x
            if y < extremeValues[2]:
                extremeValues[2] = y
            if y > extremeValues[3]:
                extremeValues[3] = y
            iterations += 1
        ifsObj.resetCurrentPoint()
        print('extreme values:', extremeValues)

        point1 = (extremeValues[0], extremeValues[2])
        point2 = (extremeValues[1], extremeValues[3])
        print('shift small', self.shiftPoint(point1, extremeValues))
        print('shift big', self.shiftPoint(point2, extremeValues))

        return extremeValues
    #
    # def fillZeros(self):
    #     for frame in self.inputframes:
    #         for field in frame.allFields:
    #             entry = field.get()
    #     pass
    #

    def shiftPoint(self, point, oldDim):
        '''old Dim is a list of 4 values: minX, maxX, minY, maxY'''
        oldDomain = oldDim[:2]
        oldRange = oldDim[2:]
        maxX = WIDTH - CANVAS_PAD
        minX = CANVAS_PAD

        maxY = HEIGHT - CANVAS_PAD
        minY = CANVAS_PAD
        xNew = (point[0] - oldDomain[0]) * (maxX - minX)/(oldDomain[1]- oldDomain[0])+50 #TODO: the padding needs to shift here
        yNew = (point[1] - oldRange[0]) * (maxY - minY)/ (oldRange[1]- oldRange[0])
        yNew = maxY - yNew #do this bc the canvas coordinates have 0 at the top and then go down
        return (xNew, yNew)


if __name__ == '__main__':

    root = Tk() #make main window

    root.state('zoomed') #maximize window
    root.title("Math 181 Final Project")

    #game.start()

    gui = GUI(root) #initialize buttons and stuff

    root.mainloop()
