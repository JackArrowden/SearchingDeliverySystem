# Supporting library
import problem
import FileHandler
import tkinter as tk
import FileHandler

# Searching algorithm
from UCS_level_2_3 import UCS_level_2_3
from source_level_1.A_star import a_star_search
from source_level_1.BFS import BFS
from source_level_1.DFS import DFS
from source_level_1.UCS import UCS
from source_level_1.GBFS import GBFS

def drawSquare(canvas, x, y, edge, **kwargs):
    canvas.create_rectangle(x * edge, y * edge, x * edge + edge, y * edge + edge, **kwargs)
    
def drawSearchLines(canvas, array, edge,):
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
            if index != len(array) - 2:
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
            
        self.fileName = ""
        self.map = [[0]]
        self.listSs = []
        self.listGs = []
        self.listFs = []
        self.isSolvable = True
        self.isLevel1 = False
        
        self.isHead = True
        self.isTail = False
        self.isResetList = True
        
        self.listPath = []
        self.listLine = []
        self.listRemainLine = []
        
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame3 = tk.Frame(self.root)
        self.frame4 = tk.Frame(self.root)
        self.frame5 = tk.Frame(self.root)
        
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
        if not self.isSolvable:
            self.unsolvableFrame = tk.Canvas(self.frame2, bg = "#F0F0F0", width = 600, height = 400)
            self.unsolvableFrame.pack(expand=True, anchor='center', pady = (10, 10))     
            self.unsolvableFrame.create_text(300, 200, text = "This problem is unsolvable!", fill="black", font = self.font2)
        
        ## Back button 1
        self.backBtn1 = tk.Button(self.frame2, text = "Back", command = self.backFromFrame2, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.backBtn1.pack(pady = (5, 10))
        
        if (self.isSolvable):
            ## Final result
            self.finalResultBtn = tk.Button(self.frame2, text = "Show final result", command = self.showFrame3, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
            self.finalResultBtn.pack(pady = (10, 10))
            
            ## Step by step manually
            self.stepByStepManuBtn = tk.Button(self.frame2, text = "Show step by step manually", command = self.showFrame4, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
            self.stepByStepManuBtn.pack(pady = (10, 10))
            
            ## Step by step automatically
            self.stepByStepAutoBtn = tk.Button(self.frame2, text = "Show step by step automatically", command = self.showFrame4, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
            self.stepByStepAutoBtn.pack(pady = (10, 10))

        ## Exit button 2
        self.exitBtn2 = tk.Button(self.frame2, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.exitBtn2.pack(pady = (10, 5))
    
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
        
        self.algoBtn1 = tk.Button(self.subFrame5b1, text = "Breadth first search", command = lambda : self.runAlgo(1), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
        self.algoBtn1.pack(side = tk.LEFT, pady = (10, 0), padx = (10, 12))
        
        self.algoBtn2 = tk.Button(self.subFrame5b1, text = "Depth first search", command = lambda : self.runAlgo(2), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
        self.algoBtn2.pack(side = tk.LEFT, pady = (10, 0), padx = (12, 12))

        self.algoBtn3 = tk.Button(self.subFrame5b1, text = "Uniform cost search", command = lambda : self.runAlgo(3), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
        self.algoBtn3.pack(side = tk.LEFT, pady = (10, 0), padx = (12, 10))
        
        ## Frame b2
        self.subFrame5b2 = tk.Frame(self.subFrame5b)
        self.subFrame5b2.pack(expand=True, anchor='center', pady = (10, 12)) 
        
        self.algoBtn4 = tk.Button(self.subFrame5b2, text = "Greedy best first search", command = lambda : self.runAlgo(4), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
        self.algoBtn4.pack(side = tk.LEFT, pady = (10, 10), padx = (12, 10))

        self.algoBtn5 = tk.Button(self.subFrame5b2, text = "A* search", command = lambda : self.runAlgo(5), bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
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
        self.listPath = listAlgo[numAlgo](self.problem)
        if self.listPath is None:
            self.isSolvable = False
        else:
            self.getListEdgePath()
        self.showFrame2()
    
    def finalResultFrame(self): #### Frame 3
        self.moveContent(self.listRemainLine, self.listLine)
        
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
        
    def stepByStepFrame(self): #### Frame 4        
        if self.isResetList:
            self.isResetList = False
            self.moveContent(self.listLine, self.listRemainLine)
            
        wth = 600 if len(self.map[0]) > 3 / 2 * len(self.map) else int(400 * len(self.map[0]) / len(self.map))
        hht = 400 if len(self.map) > 2 / 3 * len(self.map[0]) else int(600 * len(self.map) / len(self.map[0]))
        
        cellEdge = int(((wth / len(self.map[0])) + (hht / len(self.map))) / 2)
        wth = cellEdge * len(self.map[0])
        hht = cellEdge * len(self.map)
        
        ### Sub frame 4 a
        self.subFrame4a = tk.Frame(self.frame4)
        self.subFrame4a.pack(expand=True, anchor='center', pady = (5, 15))  
        
        ## Sub frame 4 a1
        self.subFrame4a1 = tk.Frame(self.subFrame4a, width = 410)
        self.subFrame4a1.pack(side = tk.LEFT, expand=False, anchor='center', pady = (5, 5))  
        
        self.backBtn3a1 = tk.Button(self.subFrame4a1, text = "Back", command = self.showFrame2, bg = "#323232", fg = "#FAFAFA", width = 20, height = 2, cursor = "hand2")
        self.backBtn3a1.pack(side = tk.LEFT, pady = (5, 0), padx = (0, 200))
        
        ## Sub frame 4 a2
        self.subFrame4a2 = tk.Frame(self.subFrame4a, width = 410)
        self.subFrame4a2.pack(side = tk.RIGHT, expand=False, anchor='center', pady = (5, 5)) 
        
        self.exitBtn4 = tk.Button(self.subFrame4a2, text = "Exit", command = self.exit, bg = "#FF4B4B", fg = "black", width = 20, height = 2, cursor = "hand2")
        self.exitBtn4.pack(side = tk.RIGHT, pady = (5, 0), padx = (200, 0))
        
        ### Sub frame 4 b
        self.subFrame4b = tk.Canvas(self.frame4, bg = "white", width = wth, height = hht)
        self.subFrame4b.pack(expand=True, anchor='center', pady = (10, 10))  
        
        self.mapDrawing(self.subFrame4b, wth, hht, cellEdge)
        
        ### Sub frame 4 c
        self.subFrame4c = tk.Frame(self.frame4)
        self.subFrame4c.pack(expand=True, anchor='center', pady = (15, 10))  
        
        if self.isHead:
            self.backBtn3 = tk.Button(self.subFrame4c, state = "disabled", text = "Previous", bg = "lightgray", fg = "white", width = 25, height = 2)
            self.backBtn3.pack(side = tk.LEFT, pady = (0, 5), padx = (0, 50))
        else:
            self.backBtn3 = tk.Button(self.subFrame4c, text = "Previous", command = self.prevMap, bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
            self.backBtn3.pack(side = tk.LEFT, pady = (0, 5), padx = (0, 50))
        
        if self.isTail:
            self.backBtn3 = tk.Button(self.subFrame4c, state = "disabled", text = "Next", bg = "lightgray", fg = "white", width = 25, height = 2)
            self.backBtn3.pack(side = tk.LEFT, pady = (0, 5), padx = (50, 0))
        else:
            self.backBtn3 = tk.Button(self.subFrame4c, text = "Next", command = self.nextMap, bg = "#323232", fg = "#FAFAFA", width = 25, height = 2, cursor = "hand2")
            self.backBtn3.pack(side = tk.LEFT, pady = (0, 5), padx = (50, 0))
    
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
                    drawSquare(canvas, j, i, edge, fill="lightgray")
                elif self.map[i][j] > 0:
                    drawSquare(canvas, j, i, edge, fill="lightblue", outline="blue")
                    canvas.create_text(j * edge + edge / 2, i * edge + edge / 2, text = str(self.map[i][j]), fill="black")
        
        # Draw start vertice
        for index, sPoint  in enumerate(self.listSs):
            name = "S" if index == 0 else "S" + str(index)
            drawSquare(canvas, sPoint[1], sPoint[0], edge, fill="lightgreen", outline="green")
            canvas.create_text(sPoint[1] * edge + edge / 2, sPoint[0] * edge + edge / 2, text = name, fill="black")
        
        # Draw goal vertice
        for index, gPoint  in enumerate(self.listGs):
            name = "G" if index == 0 else "G" + str(index)
            drawSquare(canvas, gPoint[1], gPoint[0], edge, fill="red", outline="darkred")
            canvas.create_text(gPoint[1] * edge + edge / 2, gPoint[0] * edge + edge / 2, text = name, fill="black")
        
        # Draw fuel cells
        for index, fPoint  in enumerate(self.listFs):
            name = "F" + str(index + 1)
            drawSquare(canvas, fPoint[1], fPoint[0], edge, fill="yellow", outline="black")
            canvas.create_text(fPoint[1] * edge + edge / 2, fPoint[0] * edge + edge / 2, text = name, fill="black")
 
        drawSearchLines(canvas, self.listLine, edge)
        
        # Draw 4 directions' border
        canvas.create_line([(2, 0), (2, hht)], fill='black', tags='grid_line_w')
        canvas.create_line([(wth, 0), (wth, hht)], fill='black', tags='grid_line_w')
        canvas.create_line([(0, 2), (wth, 2)], fill='black', tags='grid_line_w')
        canvas.create_line([(0, hht), (wth, hht)], fill='black', tags='grid_line_w')
    
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
        self.moveContent(self.listLine, self.listRemainLine)
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
        
    def showFrame4(self):
        self.unshowAllFrames()
        self.root.title("Step by step")
        self.frame4.pack(expand=True, anchor='center')
        self.clearFrame(self.frame4)  
        self.stepByStepFrame()
       
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
        self.listGs = []
        self.listFs = []
        self.isSolvable = True
        self.isLevel1 = False
        
        self.isHead = True
        self.isTail = False
        self.isResetList = True
        
        self.listPath = []
        self.listLine = []
        self.listRemainLine = []
        
        self.showFrame1()   
        
    def eraseAlgo(self):
        self.isSolvable = True
        self.isHead = True
        self.isTail = False
        self.isResetList = True
        
        self.listPath = []
        self.listLine = []
        self.listRemainLine = []
        
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
            self.listFs = resultRead[5] if len(resultRead) == 6 else []
            if len(resultRead) == 3:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs)
                self.isLevel1 = True
                self.showFrame5()
            elif len(resultRead) == 4:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs, resultRead[3])
                self.listPath = UCS_level_2_3(self.problem)
                if self.listPath is None:
                    self.isSolvable = False
                else:
                    self.getListEdgePath()
                self.showFrame2()
            elif len(resultRead) == 6 and len(self.listSs) == 1:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs, resultRead[3], resultRead[4])
                self.listPath = UCS_level_2_3(self.problem)
                if self.listPath is None:
                    self.isSolvable = False
                else:
                    self.getListEdgePath()
                self.showFrame2()
            else:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs)
                # Choose another algorithm to run
                # self.listPath = UCS_level_2_3(self.problem)
                self.showFrame2()

    def getListEdgePath(self):
        curLen = len(self.listPath)
        if curLen == 0:
            return False
        
        for point in self.listPath:
            self.listLine.append([point, "green"])
        return True
    
    def moveContent(self, listA, listB):
        while listA:
            cur = listA.pop()
            listB.insert(0, cur)
    
    def prevMap(self):
        cur = (0, 0)
        isHead = True
            
        if len(self.listLine) >= 1:
            isHead = False
            cur = self.listLine.pop()
            self.listRemainLine.insert(0, cur)
            
        self.isHead = isHead
        if not len(self.listRemainLine) == 0:
            self.isTail = False
            
        self.showFrame4()
    
    def nextMap(self):
        cur = (0, 0)
        isTail = True
        
        if len(self.listRemainLine) >= 1:
            isTail = False
            cur = self.listRemainLine.pop(0)
            self.listLine.append(cur)
            
        self.isTail = isTail
        if not len(self.listLine) == 0:
            self.isHead = False
        
        self.showFrame4()
        
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

# ./test_level_3/input5_level3.txt
# ./test_level_1/input5_level1.txt
if __name__ == "__main__":
    root = tk.Tk()
    app = SystemGUI(root)
    root.mainloop()