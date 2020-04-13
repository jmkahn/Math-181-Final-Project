import tkinter
import time
import random



class ChaosGame(object):

    def __init__(self, root):
        #make canvas
        self.canvas = tkinter.Canvas(root, width = 600, height = 600)
        self.canvas.pack()

        #make list of vertices
        self.vertices = [(5, 5), (5, 300), (300, 5)]

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

    def contraction(self, point1, point2, r=0.5):
        x = (point1[0] + point2[0])*r
        y = (point1[1] + point2[1])*r
        self.currentPoint = (x, y)
        self.drawPoint(x, y, 3)


moreDots = 1

def offswitch():
    moreDots = 0

if __name__ == '__main__':

    root = tkinter.Tk()

    w = ChaosGame(root)
    w.drawStartingPoints()

    while (moreDots ==1):
    # print("this is current point", w.currentPoint)
    # print("a vertex:", random.choice(w.vertices))
        w.contraction(w.currentPoint, random.choice(w.vertices))

        root.update()
        time.sleep(0.01)




    # root.bind(<Button-1>, offswitch)

    # w.drawPoint(10, 10)
    #
    #

    # w.drawPoint(15, 15)



    root.mainloop()
