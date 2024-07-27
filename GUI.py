# Supporting library
import problem
import tkinter as tk
import FileHandler

# Searching algorithm
from BFS_level_2_3 import BFS_level_2_3
from source_level_1.A_star import a_star_search
from source_level_1.BFS import BFS
from source_level_1.DFS import DFS
from source_level_1.UCS import UCS
from source_level_1.GBFS import GBFS
from hill_climbing_level_4 import hill_climbing_level_4

def drawSquare(canvas, x, y, edge, **kwargs):
    canvas.create_rectangle(x * edge, y * edge, x * edge + edge, y * edge + edge, **kwargs)
    
def drawSearchLines(canvas, array, edge, isEnd):
    for index, point in enumerate(array):
        x = point[0][1]
        y = point[0][0]
        if index + 1 < len(array):
            deltaX = array[index + 1][0][1] - x
            deltaY = array[index + 1][0][0] - y
            x = x + 1 / 2
            y = y + 1 / 2
            if index != 0:
                canvas.create_line([(x * edge, y * edge), ((x + deltaX / 2) * edge, (y + deltaY / 2) * edge)], fill = point[1])
            if index == len(array) - 2 and isEnd == 0:
                continue
            canvas.create_line([((x + deltaX / 2) * edge, (y + deltaY / 2) * edge), ((x + deltaX) * edge, (y + deltaY) * edge)], fill = point[1])

class SystemGUI():
    def __init__(self, root):
        self.root = root
        self.root.geometry('820x620')
        self.root.title("Delivery system")
        self.font1 = ("Bahnschrift Light SemiCondensed", 12)
        self.font2 = ("Bahnschrift Light SemiCondensed", 20)
        self.root.option_add("*Font", self.font1)
        
        self.default_text = "Enter input file..."
        self.text1 = "The file's name must not be left blank!"
        self.text2 = "An error occur while opening input file\nPlease enter another file's name..."
        self.root.protocol("WM_DELETE_WINDOW", self.exit)    
        self.width = 0
        self.height = 0
        self.edge = 0
            
        self.fileName = ""
        self.map = [[0]]
        self.listSs = []
        self.listCurSs = [None for _ in range(len(self.listSs))]
        self.listGs = []
        self.listFs = []
        self.isSolvable = True
        self.isLevel1 = False
        
        self.isHead = True
        self.isTail = False
        self.isResetList = True
        
        self.curNumState = 0
        self.listPath = [[]]
        self.listLine = [[]]
        self.listRemainLine = [[]]
        
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame3 = tk.Frame(self.root)
        self.frame4 = tk.Frame(self.root)
        self.frame5 = tk.Frame(self.root)
        
        self.autoRunTime = [1, {1: 1000, 2: 600, 3: 400, 4: 200, 5: 100}]
        self.resetBtn = [True, True, True]
        
        self.listColorSs = [["#00B050", "green"], ["#00B050", "green"], ["#00B050", "green"]]
        self.listColorCurSs = [["#73F589", "green"], ["#73F589", "green"], ["#73F589", "green"]]
        self.listColorGs = [["#E73B29", "darkred"], ["#E73B29", "darkred"], ["#E73B29", "darkred"]]
        self.listColorFs = [["#F3F595", "black"], ["#F6F791", "black"], ["#F7F98B", "black"], ["#F9FA81", "black"], ["#FBFB75", "black"], ["#FCFD64", "black"], ["#FDFD54", "black"], ["#FEFE3B", "black"], ["#FFFF27", "black"], ["#FFFF10", "black"]]
        self.listColorLines = ["green", "red", "blue"]
        
        self.showFrame1()
        
    def mainFrame(self): #### Frame 1  
        ## Input frame
        self.entry = tk.Text(self.frame1, fg = "gray", width = 60, height = 3, padx = 10, bg = "white", highlightbackground = "#2F4F4F")
        self.entry.insert("1.0", self.default_text)
        self.entry.pack(pady = 5)
        self.entry.bind("<FocusIn>", self.entryOnFocus)
        self.entry.bind("<FocusOut>", self.entryOnBlur)  
        self.entry.bind("<KeyPress>", self.resetText)

        ### SubFrame
        self.subFrame = tk.Frame(self.frame1)
        self.subFrame.pack(pady = (20, 10))

        ## Enter button
        self.enterBtn = tk.Button(self.subFrame, text = "Enter", command = self.getFileName, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.enterBtn.pack(pady = (5, 10))
        
        ## Exit button
        self.exitBtn1 = tk.Button(self.subFrame, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.exitBtn1.pack(pady = (5, 10))
        
    def chooseViewFrame(self): #### Frame 2
        ### Frame a
        self.subFrame2a = tk.Frame(self.frame2)
        self.subFrame2a.pack(expand=True, anchor='center', pady = (0, 80)) 
        
        if not self.isSolvable:
            self.unsolvableFrame = tk.Canvas(self.subFrame2a, bg = "#F0F0F0", width = 600, height = 400)
            self.unsolvableFrame.pack(expand=True, anchor='center', pady = (10, 10))     
            self.unsolvableFrame.create_text(300, 200, text = "This problem is unsolvable!", fill="black", font = self.font2)
        else:
            self.chooseView = tk.Canvas(self.subFrame2a, bg = "#F0F0F0", width = 600, height = 50)
            self.chooseView.pack(expand=True, anchor='center', pady = (10, 10))     
            self.chooseView.create_text(300, 10, text = "Choose a type of view", fill="black", font = self.font2)
            
            ## Final result
            self.finalResultBtn = tk.Button(self.subFrame2a, text = "Show final result", command = self.showFrame3, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
            self.finalResultBtn.pack(pady = (10, 10))
            
            ## Step by step manually
            self.stepByStepManuBtn = tk.Button(self.subFrame2a, text = "Show step by step manually", command = self.showFrame4, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
            self.stepByStepManuBtn.pack(pady = (10, 10))
            
            ## Step by step automatically
            self.stepByStepAutoBtn = tk.Button(self.subFrame2a, text = "Show step by step automatically", command = lambda: self.showFrame4(True), bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
            self.stepByStepAutoBtn.pack(pady = (10, 10))
            
        ### Frame b
        self.subFrame2b = tk.Frame(self.frame2)
        self.subFrame2b.pack(expand=True, anchor='center', pady = (20, 0)) 
            
        ## Back button 1
        self.backBtn1 = tk.Button(self.subFrame2b, text = "Back", command = self.backFromFrame2, bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
        self.backBtn1.pack(side = tk.LEFT, pady = (10, 10), padx = (0, 30))
        
        ## Exit button 2
        self.exitBtn2 = tk.Button(self.subFrame2b, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
        self.exitBtn2.pack(side = tk.LEFT, pady = (10, 10), padx = (30, 0))
    
    def chooseAlgoFrame(self):
        ### Frame a
        self.subFrame5a = tk.Canvas(self.frame5, bg = "#F0F0F0", width = 600, height = 50)
        self.subFrame5a.pack(expand=True, anchor='center', pady = (10, 0))     
        self.subFrame5a.create_text(300, 10, text = "Choose an algorithm to run", fill = "black", font = self.font2)
        
        ### Frame b
        self.subFrame5b = tk.Frame(self.frame5)
        self.subFrame5b.pack(expand=True, anchor='center', pady = (0, 80)) 
        
        ## Frame b1
        self.subFrame5b1 = tk.Frame(self.subFrame5b)
        self.subFrame5b1.pack(expand=True, anchor='center', pady = (10, 0)) 
        
        self.algoBtn1 = tk.Button(self.subFrame5b1, text = "Breadth first search", command = lambda : self.runAlgo(1), bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
        self.algoBtn1.pack(side = tk.LEFT, pady = (10, 0), padx = (10, 12))
        
        self.algoBtn2 = tk.Button(self.subFrame5b1, text = "Depth first search", command = lambda : self.runAlgo(2), bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
        self.algoBtn2.pack(side = tk.LEFT, pady = (10, 0), padx = (12, 12))

        self.algoBtn3 = tk.Button(self.subFrame5b1, text = "Uniform cost search", command = lambda : self.runAlgo(3), bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
        self.algoBtn3.pack(side = tk.LEFT, pady = (10, 0), padx = (12, 10))
        
        ## Frame b2
        self.subFrame5b2 = tk.Frame(self.subFrame5b)
        self.subFrame5b2.pack(expand=True, anchor='center', pady = (10, 12)) 
        
        self.algoBtn4 = tk.Button(self.subFrame5b2, text = "Greedy best first search", command = lambda : self.runAlgo(4), bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
        self.algoBtn4.pack(side = tk.LEFT, pady = (10, 10), padx = (12, 10))

        self.algoBtn5 = tk.Button(self.subFrame5b2, text = "A* search", command = lambda : self.runAlgo(5), bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
        self.algoBtn5.pack(side = tk.LEFT, pady = (10, 10), padx = (10, 10))
        
        ### Frame c
        self.subFrame5c = tk.Frame(self.frame5)
        self.subFrame5c.pack(expand=True, anchor='center', pady = (10, 10)) 
        
        ## Back button 1
        self.backBtn4 = tk.Button(self.subFrame5c, text = "Back", command = self.resetProblem, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.backBtn4.pack(pady = (5, 10))

        ## Exit button 2
        self.exitBtn5 = tk.Button(self.subFrame5c, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.exitBtn5.pack(pady = (10, 5))
        return
    
    def runAlgo(self, numAlgo):
        listAlgo = {
            1 : BFS,
            2 : DFS,
            3 : UCS,
            4 : GBFS,
            5 : a_star_search
        }
        self.listPath[0] = listAlgo[numAlgo](self.problem)
        if isinstance(self.listPath[0], int):
            self.isSolvable = False
        else:
            self.getListEdgePath()
        self.showFrame2()
    
    def finalResultFrame(self): #### Frame 3
        self.move2DContent(self.listRemainLine, self.listLine)
        
        wth = 600 if len(self.map[0]) > 3 / 2 * len(self.map) else int(400 * len(self.map[0]) / len(self.map))
        hht = 400 if len(self.map) > 2 / 3 * len(self.map[0]) else int(600 * len(self.map) / len(self.map[0]))
        
        cellEdge = int(((wth / len(self.map[0])) + (hht / len(self.map))) / 2)
        wth = cellEdge * len(self.map[0])
        hht = cellEdge * len(self.map)
        
        ### Sub frame 3 a
        self.subFrame3a = tk.Canvas(self.frame3, bg = "white", width = wth, height = hht)
        self.subFrame3a.pack(expand=True, anchor='center', pady = (10, 10))  
        
        self.mapDrawing(self.subFrame3a, wth, hht, cellEdge)
        
        ### Sub frame 3 b
        self.subFrame3b = tk.Frame(self.frame3)
        self.subFrame3b.pack(expand=True, anchor='center', pady = (10, 10))  
        
        self.backBtn2 = tk.Button(self.subFrame3b, text = "Back", command = self.showFrame2, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.backBtn2.pack(pady = (0, 5))
        
        self.exitBtn3 = tk.Button(self.subFrame3b, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.exitBtn3.pack(pady = (5, 0))
        
    def stepByStepFrame(self, isAuto): #### Frame 4        
        if self.isResetList:
            self.isResetList = False
            self.move2DContent(self.listLine, self.listRemainLine)
            self.move1Item(self.listRemainLine, self.listLine)
                 
        self.copy1Item(self.listCurSs, self.listLine, constraint = self.listRemainLine)
            
        wth = 600 if len(self.map[0]) > 3 / 2 * len(self.map) else int(400 * len(self.map[0]) / len(self.map))
        hht = 400 if len(self.map) > 2 / 3 * len(self.map[0]) else int(600 * len(self.map) / len(self.map[0]))
        
        cellEdge = int(((wth / len(self.map[0])) + (hht / len(self.map))) / 2)
        self.width = cellEdge * len(self.map[0])
        self.height = cellEdge * len(self.map)
        self.edge = cellEdge
        self.curTxtID = 0
        
        ### Sub frame 4 a
        self.subFrame4a = tk.Frame(self.frame4)
        self.subFrame4a.pack(expand=True, anchor='center', pady = (5, 15))  
        
        ## Sub frame 4 a1
        self.subFrame4a1 = tk.Frame(self.subFrame4a, width = 200)
        self.subFrame4a1.pack(side = tk.LEFT, expand=False, anchor='center', pady = (5, 5))  
        
        self.backBtn3a1 = tk.Button(self.subFrame4a1, text = "Back", command = self.showFrame2, bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
        self.backBtn3a1.pack(side = tk.LEFT, pady = (5, 0), padx = (0, 50))
        
        ## Cur state
        curStep = "Iteration: " + str(self.curNumState)
        self.curState = tk.Canvas(self.subFrame4a, bg = "#F0F0F0", width = 200, height = 30)
        self.curState.pack(side = tk.LEFT, expand=True, anchor='center', pady = (20, 0), padx = (50, 50))     
        self.curState.create_text(100, 10, text = curStep, fill = "black", font = self.font2)
        
        ## Sub frame 4 a2
        self.subFrame4a2 = tk.Frame(self.subFrame4a, width = 200)
        self.subFrame4a2.pack(side = tk.LEFT, expand=False, anchor='center', pady = (5, 5)) 
        
        self.exitBtn4 = tk.Button(self.subFrame4a2, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
        self.exitBtn4.pack(side = tk.LEFT, pady = (5, 0), padx = (50, 0))
        
        ### Sub frame 4 b
        self.subFrame4b = tk.Canvas(self.frame4, bg = "white", width = self.width, height = self.height)
        self.subFrame4b.pack(expand=True, anchor='center', pady = (10, 10))  
        
        self.mapDrawing(self.subFrame4b, self.width, self.height, cellEdge)
        
        ### Sub frame 4 c
        self.subFrame4c = tk.Frame(self.frame4)
        self.subFrame4c.pack(expand=True, anchor='center', pady = (15, 10))  
        
        if not isAuto:
            self.prevBtn1 = tk.Button(self.subFrame4c, state = "disabled", text = "Previous", bg = "lightgray", fg = "white", width = 25, height = 2)
            self.prevBtn2 = tk.Button(self.subFrame4c, text = "Previous", command = lambda: self.prevMap(kwargs = [self.subFrame4b, self.prevBtn1, self.prevBtn2, self.nextBtn1, self.nextBtn2, self.curState]), bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
            self.prevBtn1.pack(side = tk.LEFT, pady = (0, 5), padx = (0, 50))
                
            self.nextBtn1 = tk.Button(self.subFrame4c, state = "disabled", text = "Next", bg = "lightgray", fg = "white", width = 25, height = 2)
            self.nextBtn2 = tk.Button(self.subFrame4c, text = "Next", command = lambda: self.nextMap(isAuto = False, kwargs = [self.subFrame4b, self.prevBtn1, self.prevBtn2, self.nextBtn1, self.nextBtn2, self.curState]), bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
            self.nextBtn2.pack(side = tk.RIGHT, pady = (0, 5), padx = (50, 0))
        else:
            self.slowDown1 = tk.Button(self.subFrame4c, text = "Slow down", command = lambda: self.slowDownFunc(kwargs = [self.slowDown1, self.slowDown2, self.speedUp1, self.speedUp2]), bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
            self.slowDown2 = tk.Button(self.subFrame4c, state = "disabled", text = "Slow down", bg = "lightgray", fg = "white", width = 25, height = 2)
            if self.autoRunTime[0] == 1:
                self.slowDown2.pack(side = tk.LEFT, pady = (0, 5), padx = (0, 50))  
            else:
                self.slowDown1.pack(side = tk.LEFT, pady = (0, 5), padx = (0, 50))  
            
            self.speedUp1 = tk.Button(self.subFrame4c, text = "Speed up", command = lambda: self.speedUpFunc(kwargs = [self.slowDown1, self.slowDown2, self.speedUp1, self.speedUp2]), bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
            self.speedUp2 = tk.Button(self.subFrame4c, state = "disabled", text = "Speed up", bg = "lightgray", fg = "white", width = 25, height = 2)
            if self.autoRunTime[0] != len(self.autoRunTime[1]):
                self.speedUp1.pack(side = tk.RIGHT, pady = (0, 5), padx = (50, 0))  
            else:
                self.speedUp2.pack(side = tk.RIGHT, pady = (0, 5), padx = (50, 0))  
            
        if isAuto:
            self.subFrame4c.after(self.autoRunTime[1][self.autoRunTime[0]], lambda: self.nextMap(isAuto = True, kwargs = [self.subFrame4b, self.subFrame4c, self.curState]))
            
    def mapDrawing(self, canvas, wth, hht, edge):
        self.clearFrame(canvas)
        
        for line in range(0, wth + edge, edge):
            canvas.create_line([(line, 0), (line, hht)], fill='black', tags='grid_line_w')

        for line in range(0, hht + edge, edge):
            canvas.create_line([(0, line), (wth, line)], fill='black', tags='grid_line_h')
            
        n = len(self.map)
        m = len(self.map[0])
        
        # Draw wall cells
        for i in range(n):
            for j in range(m):
                if self.map[i][j] == -1:
                    drawSquare(canvas, j, i, edge, fill="#AEAEAE")
                elif self.map[i][j] > 0:
                    drawSquare(canvas, j, i, edge, fill="lightblue", outline="blue")
                    canvas.create_text(j * edge + edge / 2, i * edge + edge / 2, text = str(self.map[i][j]), fill="black")
        
        # Draw start vertice
        for index, sPoint in enumerate(self.listSs):
            name = "S" if index == 0 else "S" + str(index)
            drawSquare(canvas, sPoint[1], sPoint[0], edge, fill=self.listColorSs[index][0], outline=self.listColorSs[index][1])
            canvas.create_text(sPoint[1] * edge + edge / 2, sPoint[0] * edge + edge / 2, text = name, fill="black")
            
        # Draw goal vertice
        for index, gPoint in enumerate(self.listGs):
            name = "G" if index == 0 else "G" + str(index)
            drawSquare(canvas, gPoint[1], gPoint[0], edge, fill=self.listColorGs[index][0], outline=self.listColorGs[index][1])
            canvas.create_text(gPoint[1] * edge + edge / 2, gPoint[0] * edge + edge / 2, text = name, fill="black")
        
        # Draw fuel cells
        for index, fPoint in enumerate(self.listFs):
            curColor = self.listColorFs[-self.map[fPoint[0]][fPoint[1]] - 1] if -self.map[fPoint[0]][fPoint[1]] - 1 < 9 else self.listColorFs[9]
            name = "F" + str(-self.map[fPoint[0]][fPoint[1]] - 1) if self.map[fPoint[0]][fPoint[1]] < -1 else "F"
            drawSquare(canvas, fPoint[1], fPoint[0], edge, fill=curColor[0], outline=curColor[1])
            canvas.create_text(fPoint[1] * edge + edge / 2, fPoint[0] * edge + edge / 2, text = name, fill="black")
            
        for index, lines in enumerate(self.listLine):
            drawSearchLines(canvas, lines, edge, len(self.listRemainLine[index]))
 
        # Draw current position of the vehicle
        for index, sPoint in enumerate(self.listCurSs):
            if sPoint is None:
                continue
            name = "S" if index == 0 else "S" + str(index)
            drawSquare(canvas, sPoint[1], sPoint[0], edge, fill=self.listColorCurSs[index][0], outline=self.listColorCurSs[index][1])
            canvas.create_text(sPoint[1] * edge + edge / 2, sPoint[0] * edge + edge / 2, text = name, fill="black")
        
        # Draw 4 directions' border
        canvas.create_line([(2, 0), (2, hht)], fill='black', tags='grid_line_w')
        canvas.create_line([(wth, 0), (wth, hht)], fill='black', tags='grid_line_w')
        canvas.create_line([(0, 2), (wth, 2)], fill='black', tags='grid_line_w')
        canvas.create_line([(0, hht), (wth, hht)], fill='black', tags='grid_line_w')
    
    def clearCanvas(self, canvas):
        for item in canvas.find_all():
            canvas.delete(item)
    
    def showFrame1(self):
        self.isResetList = True
        self.unshowAllFrames()
        self.root.title("Delivery system")
        self.frame1.pack(expand=True, anchor='center')  
        self.clearFrame(self.frame1)  
        self.mainFrame()

    def showFrame2(self):
        self.isResetList = True
        self.isHead = True
        self.isTail = False
        self.unshowAllFrames()
        self.root.title("Choose view frame")
        self.frame2.pack(expand=True, anchor='center')  
        self.clearFrame(self.frame2) 
        self.move2DContent(self.listLine, self.listRemainLine)
        
        self.curNumState = 0
        self.listCurSs = [None for _ in range(len(self.listSs))]
        self.chooseViewFrame()
        
    def backFromFrame2(self):
        if self.isLevel1:
            self.eraseAlgo()
            self.showFrame5()
        else:
            self.resetProblem()
        
    def showFrame3(self):
        self.unshowAllFrames()
        self.root.title("Show final result")
        self.frame3.pack(expand=True, anchor='center') 
        self.clearFrame(self.frame3)  
        self.finalResultFrame() 
        
    def showFrame4(self, isAuto = False):
        self.unshowAllFrames()
        self.root.title("Step by step")
        self.frame4.pack(expand=True, anchor='center')
        self.clearFrame(self.frame4)  
        self.curNumState = 0
        self.stepByStepFrame(isAuto)
       
    def showFrame5(self):
        self.unshowAllFrames()
        self.root.title("Choose algorithm")
        self.frame5.pack(expand=True, anchor='center')
        self.clearFrame(self.frame5)  
        self.chooseAlgoFrame()
        
    def unshowAllFrames(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        self.frame5.pack_forget()
    
    def resetProblem(self):
        self.fileName = ""
        self.map = [[0]]
        self.listSs = []
        self.listCurSs = [None for _ in range(len(self.listSs))]
        self.listGs = []
        self.listFs = []
        self.isSolvable = True
        self.isLevel1 = False
        
        self.isHead = True
        self.isTail = False
        self.isResetList = True
        
        self.curNumState = 0
        self.listPath = [[]]
        self.listLine = [[]]
        self.listRemainLine = [[]]
        
        self.autoRunTime[0] = 1
        
        self.showFrame1()   
        
    def eraseAlgo(self):
        self.isSolvable = True
        self.isHead = True
        self.isTail = False
        self.isResetList = True
        
        self.listPath = [[]]
        self.listLine = [[]]
        self.listRemainLine = [[]]
        
    def clearFrame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        
    def getFileName(self):
        self.fileName = self.entry.get("1.0", tk.END).strip()
        
        if self.fileName == "" or self.fileName == self.default_text or self.fileName == self.text1 or self.fileName == self.text2:
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", self.text1)
            self.entry.mark_set("insert", "1.0")
        elif FileHandler.checkOpenFile(self.fileName) == False:
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", self.text2)  
            self.entry.mark_set("insert", "1.0")
        else:
            resultRead = FileHandler.readInput(self.fileName)
            self.map = resultRead[0]
            self.listSs = resultRead[1]
            self.listGs = resultRead[2]
            self.listFs = resultRead[len(resultRead) - 1]
            if len(resultRead) == 4:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs)
                self.isLevel1 = True
                self.showFrame5()
            elif len(resultRead) == 5:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs, resultRead[3])
                self.listPath[0] = BFS_level_2_3(self.problem)
                if isinstance(self.listPath[0], int):
                    self.isSolvable = False
                else:
                    pathLen = len(self.listPath[0])
                    count = 0
                    for index in range(pathLen):
                        if count > 0:
                            count = count - 1
                            continue
                        if self.map[self.listPath[0][index][0]][self.listPath[0][index][1]] > 0:
                            count = self.map[self.listPath[0][index][0]][self.listPath[0][index][1]]
                            for i in range(count):
                                self.listPath[0].insert(index + 1, self.listPath[0][index])
                    self.getListEdgePath()
                self.showFrame2()
            elif len(resultRead) == 6 and len(self.listSs) == 1:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs, resultRead[3], resultRead[4])
                self.listPath[0] = BFS_level_2_3(self.problem)
                if isinstance(self.listPath[0], int):
                    self.isSolvable = False
                else:
                    pathLen = len(self.listPath[0])
                    count = 0
                    index = 0
                    while index < len(self.listPath[0]):
                        if count > 0:
                            count = count - 1
                            index += 1
                            continue
                        if self.map[self.listPath[0][index][0]][self.listPath[0][index][1]] > 0:
                            count = self.map[self.listPath[0][index][0]][self.listPath[0][index][1]]
                            for i in range(count):
                                self.listPath[0].insert(index + 1, self.listPath[0][index])
                        if self.map[self.listPath[0][index][0]][self.listPath[0][index][1]] < -1:
                            count = -self.map[self.listPath[0][index][0]][self.listPath[0][index][1]] - 1
                            for i in range(count):
                                self.listPath[0].insert(index + 1, self.listPath[0][index])
                        index += 1
                    self.getListEdgePath()
                self.showFrame2()
            else:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs, resultRead[3], resultRead[4])
                isTrue, goal, self.listPath = hill_climbing_level_4(self.problem)
                if isinstance(self.listPath[0], int):
                    self.isSolvable = False
                else:
                    self.getListEdgePath()
                self.showFrame2()

    def getListEdgePath(self):
        numVertice = len(self.listPath)
        self.listLine = [[] for _ in range(numVertice)]
        self.listRemainLine = [[] for _ in range(numVertice)]
        self.listCurSs = [None for _ in range(numVertice)]
        for i in range(numVertice):
            curLen = len(self.listPath[i])
            if i == 0 and curLen == 0:
                return False
            
            for point in self.listPath[i]:
                self.listLine[i].append([point, self.listColorLines[i]])
        return True
    
    def moveContent(self, listA, listB):
        while listA:
            cur = listA.pop()
            listB.insert(0, cur)
    
    def move2DContent(self, listA, listB):
        listLen = len(listA)
        for index in range(listLen):
            self.moveContent(listA[index], listB[index])
    
    def move1Item(self, listA, listB):
        listLen = len(listA)
        for i in range(listLen):
            listB[i].append(listA[i].pop(0))
            
    def copy1Item(Self, list1D, list2D, constraint):
        listLen = len(list1D)
        for i in range(listLen):
            list1D[i] = list2D[i][len(list2D[i]) - 1][0] if len(constraint[i]) != 0 else None
    
    def prevMap(self, kwargs = []):
        self.curNumState = self.curNumState - 1
        curStep = "Iteration: " + str(self.curNumState)
        self.clearCanvas(kwargs[5])
        kwargs[5].create_text(100, 10, text = curStep, fill = "black", font = self.font2)
            
        cur = (0, 0)
            
        for index, lines in enumerate(self.listLine):
            if len(lines) >= 2:
                cur = lines.pop()
                self.listRemainLine[index].insert(0, cur)
            
        self.copy1Item(self.listCurSs, self.listLine, constraint = self.listRemainLine)
        
        self.clearCanvas(kwargs[0])
        self.mapDrawing(kwargs[0], self.width, self.height, self.edge)
        
        if len(self.listLine[0]) <= 1:
            kwargs[1].pack(side = tk.LEFT, pady = (0, 5), padx = (0, 50))
            kwargs[2].pack_forget()
        if not len(self.listRemainLine[0]) == 0:
            kwargs[3].pack_forget()
            kwargs[4].pack(side = tk.RIGHT, pady = (0, 5), padx = (50, 0))
            
    def nextMap(self, isAuto = False, kwargs = []):
        self.curNumState = self.curNumState + 1
        curStep = "Iteration: " + str(self.curNumState)
        if isAuto:
            self.clearCanvas(kwargs[2])
            kwargs[2].create_text(100, 10, text = curStep, fill = "black", font = self.font2)
        else:
            self.clearCanvas(kwargs[5])
            kwargs[5].create_text(100, 10, text = curStep, fill = "black", font = self.font2)
        
        cur = (0, 0)
        for index, lines in enumerate(self.listRemainLine):
            if len(lines) >= 1:
                cur = lines.pop(0)
                self.listLine[index].append(cur)
            
        self.copy1Item(self.listCurSs, self.listLine, constraint = self.listRemainLine)
        
        self.clearCanvas(kwargs[0])
        self.mapDrawing(kwargs[0], self.width, self.height, self.edge)
            
        if not isAuto:
            if not len(self.listLine[0]) == 0:
                kwargs[1].pack_forget()
                kwargs[2].pack(side = tk.LEFT, pady = (0, 5), padx = (0, 50))
            if len(self.listRemainLine[0]) == 0:
                kwargs[4].pack_forget()
                kwargs[3].pack(side = tk.RIGHT, pady = (0, 5), padx = (50, 0))
        else:
            if len(self.listRemainLine[0]) != 0:
                temp = kwargs
                kwargs[1].after(self.autoRunTime[1][self.autoRunTime[0]], lambda: self.nextMap(isAuto = True, kwargs = temp))
       
    def slowDownFunc(self, kwargs = []):
        if self.autoRunTime[0] > 1:
            self.autoRunTime[0] = self.autoRunTime[0] - 1
        if self.autoRunTime[0] == 1:
            kwargs[0].pack_forget()
            kwargs[1].pack(side = tk.LEFT, pady = (0, 5), padx = (0, 50))  
        if self.autoRunTime[0] != len(self.autoRunTime[1]):
            kwargs[3].pack_forget()
            kwargs[2].pack(side = tk.RIGHT, pady = (0, 5), padx = (50, 0))  
    
    def speedUpFunc(self, kwargs = []):
        if self.autoRunTime[0] < len(self.autoRunTime[1]):
            self.autoRunTime[0] = self.autoRunTime[0] + 1
        if self.autoRunTime[0] != 1:
            kwargs[1].pack_forget()
            kwargs[0].pack(side = tk.LEFT, pady = (0, 5), padx = (0, 50))  
        if self.autoRunTime[0] == len(self.autoRunTime[1]):
            kwargs[2].pack_forget()
            kwargs[3].pack(side = tk.RIGHT, pady = (0, 5), padx = (50, 0))  
        
    def entryOnFocus(self, event):
        if self.entry.get("1.0", tk.END).strip() == self.default_text:
            self.entry.delete("1.0", tk.END)

    def entryOnBlur(self, event):
        if self.entry.get("1.0", tk.END).strip() == "":
            self.entry.insert("1.0", self.default_text)
        else:
            self.entry.delete("1.0", tk.END)
                
    def resetText(self, event):
        if event.keysym == 'BackSpace' and len(self.entry.get("1.0", tk.END).strip()) == 1:
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", self.default_text)
            self.entry.mark_set("insert", "1.0")
        elif self.entry.get("1.0", tk.END).strip() == self.default_text or self.entry.get("1.0", tk.END).strip() == self.text1 or self.entry.get("1.0", tk.END).strip() == self.text2:
            self.entry.delete("1.0", tk.END)
    
    def exit(self):
        self.root.destroy()