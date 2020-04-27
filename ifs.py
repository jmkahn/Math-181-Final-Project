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


class FractalTransform():

    def __init__(self):
        self.contraction = [[0, 0], [0, 0]] #2x2 matrix
        self.translation = [[0], [0]] #1x2 matrix
        self.probability = 0 #a float value between 0 and 1


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
        return (newX, newY)


class IFS3():
    def __init__(self):
        listOfTransforms = [] #list of FractalTransforms
        self.currentPoint = (0, 0) #TODO: this should maybe in a matrix form?


    def pickTransformation(self):
        pass
        #extract probabilities from each transformation
        p1 = self.listOfTransforms[0].probability
        p2 = self.listOfTransforms[1].probability

        #choose a random number between 0 and 1
        n = random.random()
        # if n is between 0 and p1, choose transformation 1
        if n < p1:
            return self.listOfTransforms[0]
        # elif n is between p1 and p1 + p2, choose transformation 2
        elif n < (p1 + p2):
            return self.listOfTransforms[1]
        # else, choose transformation 3
        else:
            return self.listOfTransforms[2]


    def iterateIFS(self):
        '''Iterates the IFS by one step. Randomly chooses one of the three transformations to apply
        (based on the probability of each one) and applies that transformation to the current point'''
        # pick which transformation to apply
        transformation = self.pickTransformation()
        #apply that transformation to the current point and update current point
        self.currentPoint = transformation.transformPoint(self.currentPoint)



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

        self.homeScreen()



############### GENERAL METHODS ####################
    def homeScreen(self):


        welcome = Text(root, height=6)
        self.packWidget(welcome)
        welcome.insert(tk.END, "Welcome to an interactive exploration of Iterated Fractal Systems (IFS) \nby Jenna and Cassidy!\n more text \nmore text more text \nexplaining what this is ")
        #make Chaos game button
        chaosButton = Button(root, text= "Let's play the Chaos Game", command=self.preChaosScreen)
        self.packWidget(chaosButton)

        # #make input your own transformation(s) button
        otherButton =  Button(root, text="Enter a custom transformation", command=self.inputTransformation)
        self.packWidget(otherButton)


    def goBacktoHomeScreen(self):
        '''takes us back to the home screen'''
        self.moreDots = 0
        self.color = 0
        self.canvas.delete("all")

        self.hidePackedWidgets()
        self.homeScreen()


    def packWidget(self, widget):
        '''packs a widget (adds to GUI) and adds it to the list of currently packed widgets'''
        widget.pack()
        self.packedWidgets.append(widget)

    def hidePackedWidgets(self):
        '''hides all the widgets in the list of packed widgets and clears the list'''
        for widget in self.packedWidgets:
            widget.pack_forget()
        self.packedWidgets.clear()




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



    def drawPoint(self, vertex, point_size, color_fill='black'):
        '''draws a point on the canvas'''
        x = vertex[0]
        y = vertex[1]
        self.canvas.create_oval(x, y, x+point_size, y+point_size, outline=color_fill, fill=color_fill) # creates points


    def preChaosScreen(self):
        self.hidePackedWidgets() #clear previous widgets


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
        sets up the canvas and checks to make sure the inputs were valid'''
        #get the input from the entry fields
        numerator = self.ratioNum.get()
        denominator = self.ratioDenom.get()

        self.hidePackedWidgets() #clear previous widgets

        #go back button
        backButton = Button(root, text="Go Back", bg=DEFAULT_BUTTON_COLOR, command=self.goBacktoPreChaos)
        homeButton = Button(root, text="Home", bg=DEFAULT_BUTTON_COLOR, command=self.goBacktoHomeScreen)

        self.packWidget(backButton)
        self.packWidget(homeButton)

        self.canvas = Canvas(self.root,
                            width = WIDTH,
                            height = HEIGHT,
                            bg = CANVAS_COLOR)
        # self.canvas.pack(fill=BOTH, side=TOP)
        self.packWidget(self.canvas)

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
        self.hidePackedWidgets() #clear previous widgets

        #input three affine transformations

        class MatrixInputFrame(Frame):

            def __init__(self, number):
                super().__init__()

                self.initUI(number)

            def initUI(self, number):

                # self.columnconfigure(0, pad=3)
                # self.columnconfigure(1, pad=3)
                # self.columnconfigure(2, pad=30)
                # self.columnconfigure(3, pad=30)
                # self.columnconfigure(4, pad=3)
                #
                #
                # self.rowconfigure(0, pad=3)
                # self.rowconfigure(1, pad=3)
                # self.rowconfigure(2, pad=0)
                # self.rowconfigure(3, pad=3)
                # self.rowconfigure(4, pad=3)



                label1 = Label(self, text="Tranformation "+str(number))
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

                test = Label(self, text=")")
                test.config(font=("Courier", 22))
                test.grid(row=1, column=10, rowspan=2, sticky=tk.W)

                self.pack()


        list = []
        for n in range(1, 4):
            name = "w" + str(n)
            name = MatrixInputFrame(n)
            list.append(name)






if __name__ == '__main__':


    root = Tk() #make main window

    root.state('zoomed') #maximize window
    root.title("Math 181 Final Project")

    #game.start()

    gui = GUI(root) #initialize buttons and stuff



    root.mainloop()
