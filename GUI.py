import problem
import tkinter as tk
import FileHandler

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
        self.map = [[0, 0, 5], [0, -1, 0], [0, -1, 0]]
        self.listSs = []
        self.listGs = []
        self.listFs = []
        self.listPath = []
        
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame3 = tk.Frame(self.root)
        self.frame4 = tk.Frame(self.root)
        
        self.mainFrame()
        self.chooseViewFrame()
        self.finalResultFrame()
        self.stepByStepFrame()
        
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
        self.backBtn2 = tk.Button(self.frame3, text = "Back", command = self.showFrame2, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.backBtn2.pack(pady = (5, 10))
        
        self.exitBtn3 = tk.Button(self.frame3, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.exitBtn3.pack(pady = (5, 10))
        
    def stepByStepFrame(self): #### Frame 4
        wth = 600 if len(self.map[0]) > 3 / 2 * len(self.map) else int(400 * len(self.map[0]) / len(self.map))
        hht = 400 if len(self.map) > 2 / 3 * len(self.map[0]) else int(600 * len(self.map) / len(self.map[0]))
        
        cellEdge = int(((wth / len(self.map[0])) + (hht / len(self.map))) / 2)
        wth = cellEdge * len(self.map[0])
        hht = cellEdge * len(self.map)
        
        ### Sub frame 4 a
        self.subFrame4a = tk.Canvas(self.frame4, bg = "white", cursor = "hand2", width = wth, height = hht)
        self.subFrame4a.pack(expand=True, anchor='center', pady = (10, 10))  
        
        # Clear all widgets
        self.clearFrame(self.subFrame4a)
        
        for line in range(0, wth + cellEdge, cellEdge):
            self.subFrame4a.create_line([(line, 0), (line, hht)], fill='black', tags='grid_line_w')

        for line in range(0, hht + cellEdge, cellEdge):
            self.subFrame4a.create_line([(0, line), (wth, line)], fill='black', tags='grid_line_h')
            
        n = len(self.map)
        m = len(self.map[0])
        
        # Draw wall cells
        for i in range(n):
            for j in range(m):
                if self.map[i][j] == -1:
                    drawSquare(self.subFrame4a, j, i, cellEdge, fill="lightgray")
                elif self.map[i][j] > 0:
                    drawSquare(self.subFrame4a, j, i, cellEdge, fill="lightblue", outline="blue")
                    self.subFrame4a.create_text(j * cellEdge + cellEdge / 2, i * cellEdge + cellEdge / 2, text = str(self.map[i][j]), fill="black")
        
        # Draw start vertice
        
        # Draw goal vertice
        
        # Draw fuel cells
        
        # Draw search lines
        
        # Draw top and right border
        self.subFrame4a.create_line([(2, 0), (2, hht)], fill='black', tags='grid_line_w')
        self.subFrame4a.create_line([(0, 2), (wth, 2)], fill='black', tags='grid_line_w')
        
        ### Sub frame 4 b
        self.subFrame4b = tk.Frame(self.frame4)
        self.subFrame4b.pack(expand=True, anchor='center', pady = (10, 10))  
        
        self.backBtn3 = tk.Button(self.subFrame4b, text = "Back", command = self.showFrame2, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.backBtn3.pack(pady = (0, 5))
        
        self.exitBtn4 = tk.Button(self.subFrame4b, text = "Exit", command = self.exit, bg = "#323232", fg = "#FAFAFA", width = 40, height = 2, cursor = "hand2")
        self.exitBtn4.pack(pady = (5, 0))
    
    def showFrame1(self):
        self.unshowAllFrames()
        self.root.title("Delivery system")
        self.frame1.pack(expand=True, anchor='center')  

    def showFrame2(self):
        self.unshowAllFrames()
        self.root.title("Choose view frame")
        self.frame2.pack(expand=True, anchor='center')  
        
    def showFrame3(self):
        self.unshowAllFrames()
        self.root.title("Show final result")
        self.frame3.pack(expand=True, anchor='center')  
        
    def showFrame4(self):
        self.unshowAllFrames()
        self.root.title("Step by step")
        self.frame4.pack(expand=True, anchor='center')  
        
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
            #### Run algorithm here!
        
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