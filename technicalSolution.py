import functools
import tkinter as tk
from tkinter import simpledialog,messagebox
import sys
import time
if 'M:/Python Packages' not in sys.path:
    sys.path.append('M:/Python Packages')
from variables import *
from functions import *
sys.setrecursionlimit(2**15)
import pygame
pygame.font.init()
font = pygame.font.SysFont(None, 30)

colours = [(199,69,64), (45,112,179), (56,140,70), (96,66,166), (0,0,0), (250,126,25)]

aliases = True
if aliases:
    initialiseAlias()

#Returns the size of the screen
def getScreenSize():
    root = tk.Tk()
    val = (root.winfo_screenheight(), root.winfo_screenwidth())
    root.destroy()
    return val


class Grid:
    def __init__(self, xMin, xMax, yMin, yMax, funcs = ['y = x'], vwoop = True, screenHeight = getScreenSize()[0], screenWidth = getScreenSize()[1]):
        screenheight = screenHeight
        screenwidth = screenWidth
        self.__xMin = xMin - 0.001 * xMin
        self.__xMax = xMax + 0.001 * xMax
        self.__xInt = xMax - xMin #Interval for x
        
        self.__yMin = yMin - 0.001 * yMin
        self.__yMax = yMax +0.001 * yMax
        self.__yInt = yMax - yMin #Interval for y

        self.__screenHeight = screenHeight
        self.__screenWidth = screenWidth

        self.__screen = pygame.display.set_mode((screenWidth,screenHeight))
        
        self.listFuncs = funcs
        self.__funcs = [Function(i, xMin, xMax, yMin, yMax, self.__screen) for i in funcs]
        self.__gridPoints = []
        self.__points = []
        
        self.vwoop = vwoop
        self.__funcBox = False
        
    def xGet(self):
        return (self.__xMin, self.__xMax, self.__xVal)
    
    def yGet(self):
        return (self.__yMin, self.__yMax, self.__yVal)
    
    def getGrid(self):
        return self.__gridPoints
    
    #Returns the increment in x (see overleaf)
    def xIncrement(self):
        return self.__xInt / self.__screenWidth

    #Returns the increment in y
    def yIncrement(self):
        return self.__yInt / self.__screenHeight

    #Creates the list of values of x to check
    def xValues(self):
        valueList = []
        currentValue = self.__xMin
        increment = self.xIncrement()
        
        while currentValue < self.__xMax:
            valueList.append(currentValue)
            currentValue += increment
            
        return valueList

    #Creates the list of values of y to check
    def yValues(self):
        valueList = []
        currentValue = self.__yMin
        increment = self.yIncrement()
        while currentValue < self.__yMax:
            valueList.append(currentValue)
            currentValue += increment
        return valueList

    def allUpdate(self, xMin, xMax, yMin, yMax):
        self.__xMin = xMin  - 0.001 * xMin
        self.__xMax = xMax  + 0.001 * xMin
        self.__xInt = xMax - xMin
        
        self.__yMin = yMin  - 0.001 * yMin
        self.__yMax = yMax  + 0.001 * yMax
        self.__yInt = yMax - yMin
        
        
    def updateGrid(self, newGrid):
        self.__gridPoints = newGrid

    def newPlot(self):
        try:
            self.__points = []
            self.__gridPoints = []
            self.__funcs = [Function(i, self.__xMin, self.__xMax, self.__yMin, self.__yMax, self.__screen) for i in self.listFuncs]
            print(self.__funcs)
            count = 1
            for func in self.__funcs:
                xGrid, yGrid = func.changeInSignGrid(count)
                count += 1
                self.__points.append((xGrid, yGrid))
            x, y = self.gridLines()
            self.__screen.fill((255, 255, 255))
            self.plotGrid(x, y)
            for i, point in enumerate(self.__points):
                for j in range(len(point[0])):
                    renderRect = pygame.Rect(point[0][j][1] + 1, maxY - point[1][j][1] - 1, 2, 2)
                    pygame.draw.rect(self.__screen, colours[i % len(colours)], renderRect)
                    if self.vwoop and point == self.__points[-1]:
                        pygame.display.update()
                pygame.display.update()
        except BaseException as e:
            messagebox.showerror(None, e)
            
    def plot(self, update, *func):
        if update:
            if func:
                count = len(self.__funcs)+1
                xGrid, yGrid = func[0].changeInSignGrid(count)
                self.__points.append((xGrid, yGrid))
            x, y = self.gridLines()
            self.__screen.fill((255, 255, 255))
            self.plotGrid(x, y)
            for i, point in enumerate(self.__points):
                for j in range(len(point[0])):
                    renderRect = pygame.Rect(point[0][j][1] + 1, maxY - point[1][j][1] - 1, 2, 2)
                    pygame.draw.rect(self.__screen, colours[i % len(colours)], renderRect)
                    if self.vwoop and point == self.__points[-1]:
                        pygame.display.update()
                pygame.display.update()

    def functionBox(self):
        self.__funcBox = (30, 30)
        pygame.draw.rect(self.__screen, (0, 255, 0), pygame.Rect(0, 0, self.__funcBox[0], self.__funcBox[1]))

    def crossBox(self):
        self.__crossBox = (self.__screenWidth - 30, 30)
        pygame.draw.rect(self.__screen, (255, 0, 0), pygame.Rect(self.__crossBox[0], 0, 30, 30))

    def plotGrid(self, xList, yList):
        for x in xList:
            if x == 0:
                pygame.draw.rect(self.__screen, (0,0,0), pygame.Rect(self.__screenWidth*(x-self.__xMin)/self.__xInt, 0, 4, self.__screenHeight))
            else:
                pygame.draw.rect(self.__screen, (149,149,149), pygame.Rect(self.__screenWidth*(x-self.__xMin)/self.__xInt, 0, 1, self.__screenHeight))
            img = font.render(str(x), True, (0,0,0))
            self.__screen.blit(img, (self.__screenWidth*(x-self.__xMin)/self.__xInt  - 20, self.__screenHeight - 20))
            
        for y in yList:
            if y == 0:
                pygame.draw.rect(self.__screen, (0,0,0), pygame.Rect(0, self.__screenHeight*(y-self.__yMin)/self.__yInt, self.__screenWidth, 4))
            else:
                pygame.draw.rect(self.__screen, (149,149,149), pygame.Rect(0, self.__screenHeight*(y-self.__yMin)/self.__yInt +1, self.__screenWidth, 1))
            img = font.render(str(y), True, (0,0,0))
            self.__screen.blit(img, (5, self.__screenHeight - self.__screenHeight*(y-self.__yMin)/self.__yInt - 15))

    def baseGrid(self):
        for i, func in enumerate(self.__funcs):
            print(func)
            xGrid, yGrid = func.changeInSignGrid(i+1)
            self.__points.append((xGrid, yGrid))
            
    def start(self):
        p = True
        update = True
        self.baseGrid()
        while p:
            self.plot(update)
            self.functionBox()
            self.crossBox()
            update = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos <= self.__funcBox:
                            x = self.getChoice()
                        if event.pos >= self.__crossBox:
                            p = False
                            pygame.quit()
                         

                    elif event.button == 3:
                        text = simpledialog.askstring('Add text', 'Enter text to add')
                        img = font.render(text, True, (0, 0, 0))
                        self.__screen.blit(img, event.pos)

                if event.type == pygame.QUIT:
                    p = False
                    pygame.quit()
                    
            if p:       
                pygame.display.update()
                time.sleep(1/60)

    def getChoice(self):
        options = tk.Tk()
        tk.Button(options, command = lambda: self.add_function(options), text='Add a new function', padx=10).grid(row=0, padx=(40,40), pady=(20,0))
        tk.Button(options, command = lambda: self.remove_function(options), text='Remove a function').grid(row=1)
        tk.Button(options, command = lambda: self.remove_text(options), text='Clear text').grid(row=2)
        tk.Button(options, command = lambda: self.change_bounds(options), text='Change bounds').grid(row=3)
        tk.Button(options, command = lambda: self.toggle_vwoop(options), text=f'Toggle drawing: {self.vwoop}').grid(row=4)
        tk.Button(options, command = options.destroy, text='Close').grid(row=5,pady=(0,20))
        options.mainloop()
        
    def toggle_vwoop(self, button):
        button.destroy()
        self.vwoop = not self.vwoop

    def disableVwoop(self):
        self.vwoop = False

    def enableVwoop(self):
        self.vwoop = True
        
    def add_function(self, button):
        button.destroy()
        func = simpledialog.askstring('Function prompt', 'Enter the function to add')
        function = Function(func, self.__xMin, self.__xMax, self.__yMin, self.__yMax, self.__screen)
        self.listFuncs.append(func)
        self.__funcs.append(function)
        self.plot(True, function)
        
    def remove_function(self, button):
        button.destroy()
        
        option = tk.Tk()
        for i, func in enumerate(self.__funcs):
            string = f'{i}: {func}'
            tk.Button(option, command = lambda: self.removePoint(i, option), text = string, padx = 10).grid(row = i)
        option.mainloop()

    def removePoint(self, option, button):
        button.destroy()
        try:
            self.__points.pop(option)
            self.__funcs.pop(option)
            if self.vwoop:
                self.disableVwoop()
                self.plot(True)
                self.enableVwoop()
            else:
                self.plot(True)
        except:
            messagebox.showerror('Invalid option')
            
    def remove_text(self, button):
        if self.vwoop:
            self.disableVwoop()
            self.plot(True)
            self.enableVwoop()
        else:
            self.plot(True)
        button.destroy()
    
    def change_bounds(self, button):
        master = tk.Tk()
        tk.Label(master, text='Lower bound of x').grid(row=0)
        tk.Label(master, text='Upper bound of x').grid(row=1)
        tk.Label(master, text='Lower bound of y').grid(row=2)
        tk.Label(master, text='Upper bound of y').grid(row=3)
        entryLX = tk.Entry(master)
        entryUX = tk.Entry(master)
        entryLY = tk.Entry(master)
        entryUY = tk.Entry(master)
        entryLX.grid(row=0,column=1)
        entryUX.grid(row=1,column=1)
        entryLY.grid(row=2,column=1)
        entryUY.grid(row=3,column=1)
        tk.Button(master, text='Enter', command=master.quit).grid(row=4,column=0,sticky=tk.W,pady=4)
        master.mainloop()
        try:
            self.allUpdate(int(eval(entryLX.get())), int(eval(entryUX.get())), int(eval(entryLY.get())), int(eval(entryUY.get())))
            self.newPlot()
        except:
            messagebox.showerror('Invalid fields')
        master.destroy()
        button.destroy()
        return True
    
    def gridLines(self):
        xList = [0]
        yList = [0]
        mxCount1 = 0
        mxCount2 = 0
        myCount1 = 0
        myCount2 = 0
        xMinTemp = self.__xMin
        xMaxTemp = self.__xMax
        yMinTemp = self.__yMin
        yMaxTemp = self.__yMax
        if xMinTemp != 0:
            while abs(xMinTemp) < 1:
                mxCount1 += 1
                xMinTemp *= 10
        if xMaxTemp != 0:
            while abs(xMaxTemp) < 1:
                mxCount2 += 1
                xMaxTemp *= 10
        if yMinTemp != 0:
            while abs(yMinTemp) < 1:
                myCount1 += 1
                yMinTemp *= 10
        if yMaxTemp != 0:
            while abs(yMaxTemp) < 1:
                yxCount2 += 1
                yMaxTemp *= 10
        xMag = 10 ** (max(len(str(abs(self.__xMin)).split('.')[0]) - mxCount1, len(str(abs(self.__xMax)).split('.')[0])-mxCount2)-1)
        yMag = 10 ** (max(len(str(abs(self.__yMin)).split('.')[0]) - myCount1, len(str(abs(self.__yMax)).split('.')[0])-myCount2)-1)

        xCount = 0
        while xCount - xMag >= self.__xMin:
            xCount -= xMag
            xList.append(xCount)

        xCount = 0
        while xCount + xMag <= self.__xMax:
            xCount += xMag
            xList.append(xCount)

        yCount = 0
        while yCount - yMag >= self.__yMin:
            yCount -= yMag
            yList.append(yCount)
            
        yCount = 0
        while yCount + yMag <= self.__yMax:
            yCount += yMag
            yList.append(yCount)
        return xList, yList

########################################################################################################################

def check(string, func):
    funcPart = str(func).split('=')
    if funcPart[0] == string and string not in funcPart[1]:
        func = funcPart[1]
        return func
    elif string not in funcPart[0] and funcPart[1] == string:
        func = funcPart[0]
        return func
    return False

################################################################################################

class Function:
    def __init__(self, function, xMin, xMax, yMin, yMax, screen, *derivative):
        if 'import' in function or 'sys' in function or 'tk' in function or 'time' in function or '\n' in function:
            raise BaseException('no')
        
        self.__func = function
        self.__xMin = xMin - 0.000001 * xMin
        self.__xMax = xMax + 0.000001 * xMax
        self.__xInt = xMax - xMin #Interval for x

        self.__screen = screen
        self.__yMin = yMin - 0.000001 * yMin
        self.__yMax = yMax + 0.000001 * yMax
        self.__yInt = yMax - yMin #Interval for y
        self.__screenHeight = getScreenSize()[0]
        self.__screenWidth = getScreenSize()[1]
        
    def xGet(self):
        return (self.__xMin, self.__xMax, self.__xVal)
    
    def yGet(self):
        return (self.__yMin, self.__yMax, self.__yVal)
    
    def getGrid(self):
        return self.__gridPoints
    
    #Returns the increment in x (see overleaf)
    def xIncrement(self):
        return self.__xInt / (self.__screenWidth)

    #Returns the increment in y
    def yIncrement(self):
        return self.__yInt / (self.__screenHeight)

    #Creates the list of values of x to check
    def xValues(self):
        valueList = []
        currentValue = self.__xMin
        increment = self.xIncrement()
        
        while currentValue < self.__xMax:
            valueList.append(currentValue)
            currentValue += increment
            
        return valueList

    #Creates the list of values of y to check
    def yValues(self):
        valueList = []
        currentValue = self.__yMin
        increment = self.yIncrement()
        while currentValue < self.__yMax:
            valueList.append(currentValue)
            currentValue += increment
        return valueList

    def allUpdate(self, xMin, xMax, yMin, yMax):
        self.__xMin = xMin - 0.000001 * xMin
        self.__xMax = xMax + 0.000001 * xMax
        self.__xInt = xMax - xMin #Interval for x
        
        self.__yMin = yMin - 0.000001 * yMin
        self.__yMax = yMax + 0.000001 * yMax
        self.__yInt = yMax - yMin
        
    def __repr__(self):
        return self.__func

    def __str__(self):
        return self.__func
    
    def calcPoints(self, count):
        gridPoints = [] #List of gridpoints, format ((xPos, yPos), val)
        tempFunc = self.__func
        if tempFunc == None:
            raise BaseException('No function defined.')

        tFunc = check('Y', self.__func)
        funcPart = tempFunc.split('=')
        newFunc = f'{funcPart[0]}-({funcPart[1]})' #Rearrangement of
        #function to be calculated (see overleaf)
        global maxX, maxY
        X, Y = self.xValues(), self.yValues()
        maxX, maxY = len(X), len(Y)
        xCount = 0
        yCount = 0
        yLen = len(self.yValues())

        text = f'{count}: {self.__func}'
        T = font.render(text, True, (255, 255, 255))
        self.__screen.blit(T, (0, self.__screenHeight-35))
        
        if tFunc:
            self.__func = self.__func.replace('Y', 'y')
            for x1 in X:
                try:
                    val = self.derivative(x1)
                except:
                    val = 1
                    
                for y in Y:
                    gridPoints.append(((x1, y),(xCount, yCount), val-y))
                    yCount += 1
                yCount = 0
                xCount += 1
                self.progressBar(xCount, maxY, yCount, maxY)
            self.__screen.fill((0,0,0))
        else:    
            for x in X:
                for y in Y:
                    try:
                        val = eval(newFunc)
                    except:
                        val = 1
                    gridPoints.append(((x, y),(xCount, yCount), val))
                    yCount += 1
                yCount = 0
                xCount += 1
                self.progressBar(xCount, maxY, yCount, maxY)
            self.__screen.fill((0,0,0))
        return gridPoints

    def progressBar(self, x, maxX, y, maxY):
        progress = (x*maxX + y) / (self.__screenWidth * self.__screenHeight) * self.__screenWidth
        pygame.draw.rect(self.__screen, (0, 0, 255), pygame.Rect(0, self.__screenHeight-5, progress, 5))
        pygame.display.update()
        
    def changeInSignGrid(self, count):
        xGrid = []
        yGrid = []
        self.__gridPoints = self.calcPoints(count)
        maxPoint = self.__gridPoints[-1]
        xMax = maxPoint[1][0]
        yMax = maxPoint[1][1]
        for x in range(xMax):
            for y in range(yMax):
                topLeftPoint  = self.__gridPoints[x*maxY+y]
                tlVal = topLeftPoint[2]
                
                topRightPoint = self.__gridPoints[x*maxY+y+1]
                trVal = topRightPoint[2]
                
                botLeftPoint  = self.__gridPoints[(x+1)*maxY+y]
                blVal = botLeftPoint[2]
                
                botRightPoint = self.__gridPoints[(x+1)*maxY+y+1]
                brVal = botRightPoint[2]

                if tlVal * trVal * blVal * brVal == 0:
                    xGrid.append((topLeftPoint[0][0], topLeftPoint[1][0]))
                    yGrid.append((topLeftPoint[0][1], topLeftPoint[1][1]))
                try:
                    if sgn(tlVal) == sgn(trVal) == sgn(blVal) == sgn(brVal):
                        pass
                    else:
                        xGrid.append((topLeftPoint[0][0], topLeftPoint[1][0]))
                        yGrid.append((topLeftPoint[0][1], topLeftPoint[1][1]))
                except:
                    pass
        return xGrid, yGrid

    def derivative(self, point):
        func = check('y', self.__func)
        if func:
            zeroes = 7
            if type(point) == tuple:
                point = point[0]
                
            x = point
            minVal = eval(func)
            
            x += (10 ** -zeroes) * point
            maxVal = eval(func)

            dif = x - point
            return (maxVal - minVal) / dif
        else:
            return 0

    def integral(self, minX, maxX):
        func = check('y', self.__func)
        if func:
            if minX == maxX:
                return 0
            elif minX > maxX:
                minX, maxX = maxX, minX

            numberOfPoints = 1000000
            total = 0
            points = []
            interval = (maxX - minX) / numberOfPoints
            check = minX - interval
            
            while check <= (maxX - interval):
                x = check + interval
                value = eval(func)
                points.append(value)
                check += interval

            for i in points:
                if i != points[0] or i != points[-1]:
                    total += 2 * i
                else:
                    total += i
            total /= 2
            h = (maxX - minX) / numberOfPoints
            total *= h
            return total
        else:
            return 0
        
if __name__ == '__main__':
    baseGrid = Grid(-10,10,-5,5, [], False)
    baseGrid.start()
