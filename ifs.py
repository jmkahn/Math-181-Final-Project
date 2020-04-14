import tkinter as tk
import time
import random

moreDots = 1


class ChaosGame(object):

    def __init__(self, root, ratio):
        #make canvas
        self.canvas = tk.Canvas(root, width = 600, height = 600)
        self.canvas.pack()

        #make list of vertices
        self.vertices = [(5, 5), (5, 300), (300, 5)]

        self.ratio = ratio

        self.currentPoint = ()
        self.initializePoint()


    #Chaos game:

    #start with three vertices as points of the triangle (red, blue, green)
    #randomly choose one of the points (this is the seed)
    #randomly choose another point - draw a point halfway between the seed point and this point
    # then repeat, each time moving the previous point half the distance to the vertex which is chosen
    # (throw out the first few points)


    def drawStartingPoints(self):
        for vertex in self.vertices:
            x = vertex[0]
            y = vertex[1]
            self.drawPoint(x, y, 5)


    def drawPoint(self, x, y, size):
        c = self.canvas
        c.create_oval(x, y, x+size, y+size, fill='black')
        c.pack()

    def initializePoint(self):
        seed = random.choice(self.vertices)
        point1 = random.choice(self.vertices)
        self.contraction(seed, point1)

    #TODO: figure out the correct contraction equations for generalized r
    def contraction(self, point1, point2):
        r = self.ratio
        x = (point1[0] + point2[0])/r
        y = (point1[1] + point2[1])/r

        self.currentPoint = (x, y)
        self.drawPoint(x, y, 3)



    def play(self):

        moreDots = 1
        self.drawStartingPoints()

        while (moreDots == 1):
            self.contraction(self.currentPoint, random.choice(self.vertices))

            self.canvas.update()
            time.sleep(0.01)



        root.bind("<Button-1>", switch)








if __name__ == '__main__':

    # ratio = input("What contraction ratio do you want? Input an integer value. \n")
    # ratio = int(ratio)


    root = tk.Tk()

    def chaosScreen():
        print("we will now play the chaos game")
        ratio = 2
        game = ChaosGame(root, ratio)
        game.play()

        chaosButton.config(state="disabled")
        otherButton.pack_forget()




    def transformationScreen():
        print("we will now generate custom transformations")


    # def switch(event):
    #     # print("I am happen now!!!! ")
    #     global moreDots
    #     if moreDots = 1:
    #         moreDots = 0 #TODO: make it so that we can restart when click again
    #     else:
    #         #continue playing chaos game
    #         pass


    #make Chaos game button
    chaosButton = tk.Button(root, text= "Let's play the Chaos Game", command=chaosScreen)
    chaosButton.pack()


    #make input your own transformation(s) button
    otherButton = tk.Button(root, text="Enter a custom transformation", command=transformationScreen)
    otherButton.pack()


    #TODO: hide the buttons when we get to a screen (and then go backtracking)
    #TODO: prevent it from starting another chaos game once one has been started (by hiding the buttons)



    root.mainloop()
