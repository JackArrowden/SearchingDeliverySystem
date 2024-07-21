import problem
import FileHandler
import tkinter as tk
import FileHandler
from UCS_level_2_3 import UCS_level_2_3

def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)

def drawSquare(canvas, x, y, edge, **kwargs):
    canvas.create_rectangle(x * edge, y * edge, x * edge + edge, y * edge + edge, **kwargs)
    
def drawOneQuater(canvas, array, edge, type):
    x = None
    y = None
    coorVDict = {
        1 : [lambda x : (x + 1 / 2) * edge, lambda y : y * edge, lambda x : (x + 1 / 2) * edge, lambda y :  (y + 1 / 2) * edge],
        2 : [lambda x : (x + 1 / 2) * edge, lambda y : y * edge, lambda x : (x + 1 / 2) * edge, lambda y : (y + 1 / 2) * edge],
        3 : [lambda x : (x + 1 / 2) * edge, lambda y : (y + 1 / 2) * edge, lambda x : (x + 1 / 2) * edge, lambda y : (y + 1) * edge],
        4 : [lambda x : (x + 1 / 2) * edge, lambda y : (y + 1 / 2) * edge, lambda x : (x + 1 / 2) * edge, lambda y : (y + 1) * edge]
    }
    coorHDict = {
        1 : [lambda x : (x + 1 / 2) * edge, lambda y : (y + 1 / 2) * edge, lambda x : (x + 1) * edge, lambda y : (y + 1 / 2) * edge],
        2 : [lambda x : x * edge, lambda y : (y + 1 / 2) * edge, lambda x : (x + 1 / 2) * edge, lambda y : (y + 1 / 2) * edge],
        3 : [lambda x : x * edge, lambda y : (y + 1 / 2) * edge, lambda x : (x + 1 / 2) * edge, lambda y : (y + 1 / 2) * edge],
        4 : [lambda x : (x + 1 / 2) * edge, lambda y : (y + 1 / 2) * edge, lambda x : (x + 1) * edge, lambda y : (y + 1 / 2) * edge]
    }
    for point in array:
        x = point[0][1]
        y = point[0][0]
        canvas.create_line([(coorVDict[type][0](x), coorVDict[type][1](y)), (coorVDict[type][2](x), coorVDict[type][3](y))], fill = point[1])
        canvas.create_line([(coorHDict[type][0](x), coorHDict[type][1](y)), (coorHDict[type][2](x), coorHDict[type][3](y))], fill = point[1])

class SystemGUI():
    def __init__(self, root):
        self.root = root
        self.root.geometry('820x560')
        self.root.title("Delivery system")
        self.default_text = "Enter input file..."
        self.text1 = "The file's name must not be left blank"
        self.text2 = "An error occur while opening input file\nPlease enter another file's name"
        self.root.protocol("WM_DELETE_WINDOW", self.exit)    
            
        self.fileName = ""
        self.map = [[0]]
        self.listSs = []
        self.listGs = []
        self.listFs = []
        self.isSolvable = True
        
        self.listPath = []
        self.listVerLine = [] # Các cạnh chung một S và G sẽ có cùng màu
        self.numV = [] # Lưu số lượng cạnh dọc được thêm vào ở từng bước chạy
        self.listHorLine = []
        self.numH = [] # Lưu số lượng cạnh ngang được thêm vào ở từng bước chạy
        self.list1stQuater = []
        self.num1Q = [] # Lưu số lượng cạnh tạo ra góc phần tư thứ nhất được thêm vào ở từng bước chạy
        self.list2ndQuater = []
        self.num2Q = [] # Lưu số lượng cạnh tạo ra góc phần tư thứ hai được thêm vào ở từng bước chạy
        self.list3rdQuater = []
        self.num3Q = [] # Lưu số lượng cạnh tạo ra góc phần tư thứ ba được thêm vào ở từng bước chạy
        self.list4thQuater = []
        self.num4Q = [] # Lưu số lượng cạnh tạo ra góc phần tư thứ tư được thêm vào ở từng bước chạy
        self.listRemainVerLine = [] # Những cạnh chưa được thêm sẽ lưu ở đây
        self.listRemainHorLine = [] 
        self.listRemain1Q = [] 
        self.listRemain2Q = [] 
        self.listRemain3Q = [] 
        self.listRemain4Q = [] 
        
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame3 = tk.Frame(self.root)
        self.frame4 = tk.Frame(self.root)
        
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
        ## Back button 1
        self.backBtn1 = tk.Button(self.frame2, text = "Back", command = self.showFrame1, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.backBtn1.pack(pady = (5, 10))
        
        ## Final result
        self.finalResultBtn = tk.Button(self.frame2, text = "Show final result", command = self.showFrame3, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.finalResultBtn.pack(pady = (10, 10))
        
        ## Step by step
        self.stepByStepBtn = tk.Button(self.frame2, text = "Show step by step", command = self.showFrame4, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.stepByStepBtn.pack(pady = (10, 10))

        ## Exit button 2
        self.exitBtn2 = tk.Button(self.frame2, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.exitBtn2.pack(pady = (10, 5))
    
    def finalResultFrame(self): #### Frame 3
        wth = 600 if len(self.map[0]) > 3 / 2 * len(self.map) else int(400 * len(self.map[0]) / len(self.map))
        hht = 400 if len(self.map) > 2 / 3 * len(self.map[0]) else int(600 * len(self.map) / len(self.map[0]))
        
        cellEdge = int(((wth / len(self.map[0])) + (hht / len(self.map))) / 2)
        wth = cellEdge * len(self.map[0])
        hht = cellEdge * len(self.map)
        
        ### Sub frame 3 a
        self.subFrame3a = tk.Canvas(self.frame3, bg = "white", cursor = "hand2", width = wth, height = hht)
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
        wth = 600 if len(self.map[0]) > 3 / 2 * len(self.map) else int(400 * len(self.map[0]) / len(self.map))
        hht = 400 if len(self.map) > 2 / 3 * len(self.map[0]) else int(600 * len(self.map) / len(self.map[0]))
        
        cellEdge = int(((wth / len(self.map[0])) + (hht / len(self.map))) / 2)
        wth = cellEdge * len(self.map[0])
        hht = cellEdge * len(self.map)
        
        ### Sub frame 4 a
        self.subFrame4a = tk.Canvas(self.frame4, bg = "white", cursor = "hand2", width = wth, height = hht)
        self.subFrame4a.pack(expand=True, anchor='center', pady = (10, 10))  
        
        self.mapDrawing(self.subFrame4a, wth, hht, cellEdge)
        
        ### Sub frame 4 b
        self.subFrame4b = tk.Frame(self.frame4)
        self.subFrame4b.pack(expand=True, anchor='center', pady = (10, 10))  
        
        self.backBtn3 = tk.Button(self.subFrame4b, text = "Back", command = self.showFrame2, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.backBtn3.pack(pady = (0, 5))
        
        self.exitBtn4 = tk.Button(self.subFrame4b, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.exitBtn4.pack(pady = (5, 0))
    
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
        
        # Draw search lines
        for vPoint in self.listVerLine:
            canvas.create_line([(vPoint[0][1] * edge + edge / 2, vPoint[0][0] * edge), 
                                         (vPoint[0][1] * edge + edge / 2, vPoint[0][0] * edge + edge)], 
                                        fill=vPoint[1])
        for hPoint in self.listHorLine:
            canvas.create_line([(hPoint[0][1] * edge, hPoint[0][0] * edge + edge / 2), 
                                         (hPoint[0][1] * edge + edge, hPoint[0][0] * edge + edge / 2)], 
                                        fill=hPoint[1])
        
        drawOneQuater(canvas, self.list1stQuater, edge, type=1)
        drawOneQuater(canvas, self.list2ndQuater, edge, type=2)
        drawOneQuater(canvas, self.list3rdQuater, edge, type=3)
        drawOneQuater(canvas, self.list4thQuater, edge, type=4)
        
        # Draw top and right border
        canvas.create_line([(2, 0), (2, hht)], fill='black', tags='grid_line_w')
        canvas.create_line([(wth, 0), (wth, hht)], fill='black', tags='grid_line_w')
        canvas.create_line([(0, 2), (wth, 2)], fill='black', tags='grid_line_w')
        canvas.create_line([(0, hht), (wth, hht)], fill='black', tags='grid_line_w')
    
    def showFrame1(self):
        self.unshowAllFrames()
        self.root.title("Delivery system")
        self.frame1.pack(expand=True, anchor='center')  
        self.clearFrame(self.frame1)  
        self.mainFrame()

    def showFrame2(self):
        self.unshowAllFrames()
        self.root.title("Choose view frame")
        self.frame2.pack(expand=True, anchor='center')  
        self.clearFrame(self.frame2)  
        self.chooseViewFrame()
        
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
        
    def unshowAllFrames(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        
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
            self.showFrame2()
            resultRead = FileHandler.readInput(self.fileName)
            self.map = resultRead[0]
            self.listSs = resultRead[1]
            self.listGs = resultRead[2]
            self.listFs = resultRead[5] if len(resultRead) == 6 else []
            if len(resultRead) == 3:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs)
                # Choose an algorithm to run
                # self.listPath = UCS_level_2_3(self.problem)
            elif len(resultRead) == 4:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs, resultRead[3])
                self.listPath = UCS_level_2_3(self.problem)
                if self.getListEdgePath() == False:
                    self.isSolvable = False
            elif len(resultRead == 6) and len(self.listSs) == 1:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs, resultRead[3], resultRead[4], resultRead[5])
                self.listPath = UCS_level_2_3(self.problem)
            else:
                self.problem = problem.Problem(self.map, self.listSs, self.listGs)
                # Choose another algorithm to run
                # self.listPath = UCS_level_2_3(self.problem)
        
    def getListEdgePath(self):
        curLen = len(self.listPath)
        if curLen == 0:
            return False
        
        for index, point in enumerate(self.listPath):
            if index == 0 or index == curLen - 1:
                continue
            if index + 1 < curLen: # Check whether this is an edge that creates an angle in the path
                if self.listPath[index - 1][0] == point[0] == self.listPath[index + 1][0]:
                    self.listHorLine.append([point, "green"])
                elif self.listPath[index - 1][1] == point[1] == self.listPath[index + 1][1]:
                    self.listVerLine.append([point, "green"])
                else:
                    if ((self.listPath[index - 1][0] == point[0] - 1 
                            and point[1] + 1 == self.listPath[index + 1][1]) 
                        or (self.listPath[index - 1][1] == point[1] + 1 
                            and point[0] - 1 == self.listPath[index + 1][0])):
                        self.list1stQuater.append([point, "green"])
                    elif ((self.listPath[index - 1][0] == point[0] - 1 
                            and point[1] - 1 == self.listPath[index + 1][1]) 
                        or (self.listPath[index - 1][1] == point[1] - 1 
                            and point[0] - 1 == self.listPath[index + 1][0])):
                        self.list2ndQuater.append([point, "green"])
                    elif ((self.listPath[index - 1][0] == point[0] + 1 
                            and point[1] - 1 == self.listPath[index + 1][1]) 
                        or (self.listPath[index - 1][1] == point[1] - 1 
                            and point[0] + 1 == self.listPath[index + 1][0])):
                        self.list3rdQuater.append([point, "green"])
                    elif ((self.listPath[index - 1][0] == point[0] + 1 
                            and point[1] + 1 == self.listPath[index + 1][1]) 
                        or (self.listPath[index - 1][1] == point[1] + 1 
                            and point[0] + 1 == self.listPath[index + 1][0])):
                        self.list4thQuater.append([point, "green"])
            else:
                if self.listPath[index - 1][0] == point[0]:
                    self.listHorLine.append([point, "green"])
                elif self.listPath[index - 1][1] == point[1]:
                    self.listVerLine.append([point, "green"])
        return True
        
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

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemGUI(root)
    root.mainloop()