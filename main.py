import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
import mouse
import keyboard
import pickle
import turtle

filetypes = (('CSV Files', '*.csv'),
             ('All Files', "*.*"))

macroFileTypes = (('Pickle File', '*.p'),
                  ('All Files', '*.*'))

bgColour = "white"
root = tkinter.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.overrideredirect(True)
root.state('zoomed')

root.configure(background=bgColour)
root.wm_attributes("-transparentcolor",bgColour)
root.lift()
root.wm_attributes("-topmost",True)

canvas = tkinter.Canvas(root,width=screen_width,height=screen_height,highlightthickness=0)
t = turtle.RawTurtle(canvas)

screen = t.getscreen()
canvas.pack()
screen.setworldcoordinates(0,screen_height,screen_width,0)

t.color("red")
t.hideturtle()

class Application():
    def __init__(self):
        self.listOfAutos = []
        self.window = tk.Tk()
        self.window.geometry("415x350")
        self.window.resizable(False,False)
        self.window.title("Macro Run")

        self.treeFrame = tk.LabelFrame(self.window,text="Sheet: ")
        self.treeFrame.place(x=5,y=70,width=300,height=225)

        self.fileContents = ttk.Treeview(self.treeFrame,show="headings")

        self.runFrame = tk.LabelFrame(self.window,text="Run")
        self.runFrame.place(x=5,y=0,width=85,height=70)
        
        self.runButton = tk.Button(self.runFrame,text="Run",command=self.runItems)
        self.runButton.place(x=5,y=0,width=70,height=45)
        
        self.buttonsFrame = tk.LabelFrame(self.window,text="Buttons: ")
        self.buttonsFrame.place(x=95,y=0,width=210,height=70)

        self.addClickButton = tk.Button(self.buttonsFrame,text="Left Click",command=self.addClick)
        self.addClickButton.place(x=5,y=0,width=70,height=20)

        self.addSelectAllButton = tk.Button(self.buttonsFrame,text="Select All",command=self.addSelectAll)
        self.addSelectAllButton.place(x=80,y=0,width=70,height=20)
        
        self.addBackspaceButton = tk.Button(self.buttonsFrame,text="Back",command=self.addBack)
        self.addBackspaceButton.place(x=155,y=0,width=45,height=20)
        
        self.addRClickButton = tk.Button(self.buttonsFrame,text="Right Click",command=self.addRClick)
        self.addRClickButton.place(x=5,y=25,width=90,height=20)
        
        self.addEnterButton = tk.Button(self.buttonsFrame,text="Enter",command=self.addEnter)
        self.addEnterButton.place(x=110,y=25,width=90,height=20)

        
        self.mouseFrame = tk.LabelFrame(self.window,text="Mouse Position: ")
        self.mouseFrame.place(x=310,y=0,width=100,height=70)
        
        self.xLabel = tk.Label(self.mouseFrame,text="X: ")
        self.xEntry = tk.Entry(self.mouseFrame)
        self.xLabel.place(x=0,y=0)
        self.xEntry.place(x=20,y=0,width=70)
        
        self.yLabel = tk.Label(self.mouseFrame,text="Y: ")
        self.yEntry = tk.Entry(self.mouseFrame)
        self.yLabel.place(x=0,y=25)
        self.yEntry.place(x=20,y=25,width=70)

        self.grooveFrame = tk.Frame(self.window,relief=tk.GROOVE)
        self.grooveFrame.place(x=310,y=70,width=100,height=165)

        self.addPosButton = tk.Button(self.grooveFrame,text="Add Pos",command=self.addPos)
        self.addPosButton.place(x=5,y=10,width=90,height=20)
        self.removeButton = tk.Button(self.grooveFrame,text="Remove",command=self.removeFromList)
        self.removeButton.place(x=5,y=35,width=90,height=20)
        self.loadButton = tk.Button(self.grooveFrame,text="Load File",command=self.loadFile)
        self.loadButton.place(x=5,y=60,width=90,height=20)

        self.listbox = tk.Listbox(self.window)
        self.listbox.place(x=310,y=155,width=100,height=140)
        self.listbox.bind("<Double-1>",lambda e:self.displayPos("Select"))

        self.loadAutoButton = tk.Button(self.window,text="Load Auto",command=self.loadAuto)
        self.loadAutoButton.place(x=315,y=300,width=90,height=20)
        self.saveAutoButton = tk.Button(self.window,text="Save Auto",command=self.saveAuto)
        self.saveAutoButton.place(x=315,y=325,width=90,height=20)
        
        self.additionalSettings = tk.LabelFrame(self.window,text="Settings: ")
        self.additionalSettings.place(x=5,y=295,width=300,height=50)

        self.delayLabel = tk.Label(self.additionalSettings,text="Delay: ")
        self.delayLabel.place(x=130,y=0)
        self.delayEntry = tk.Entry(self.additionalSettings)
        self.delayEntry.insert(tk.END,'0.2')
        self.delayEntry.place(x=170,y=0,width=60)

        self.headerLabel = tk.Label(self.additionalSettings,text="First row as Header: ")
        self.headerLabel.place(x=0,y=0)
        self.headerVar = tk.IntVar()
        self.headerEntry = tk.Checkbutton(self.additionalSettings,variable=self.headerVar)
        self.headerEntry.place(x=110,y=0,width=15)
        
        keyboard.add_hotkey("alt+x", self.addCurPos)
        self.xEntry.bind("<Key-Return>", self.displayPos)
        self.yEntry.bind("<Key-Return>", self.displayPos)
        self.window.mainloop()

    def displayPos(self,event):
        x = -1
        y = -1
        t.clear()
        t.up()
        widgetName = self.window.focus_get().widgetName
        if widgetName != "listbox":
            try:
                x = int(self.xEntry.get())
                y = int(self.yEntry.get())
            except:
                pass
        else:
            selection = self.listbox.curselection()
            item = self.listOfAutos[selection[0]]
            if item.startswith("moveTo"):
                itemSplit = item.split(",")
                x = int(itemSplit[1])
                y = int(itemSplit[2])
        t.goto(x,y)
        t.down()
        t.dot(6)
        
    def loadAuto(self):
        self.listbox.delete(0,tk.END)
        readFile = tkinter.filedialog.askopenfilename(initialdir="C:",filetypes=macroFileTypes)
        if readFile is None:
            return
        self.listOfAutos = pickle.load(open(readFile,'rb'))
        for item in self.listOfAutos:
            itemSplit = item.split(",")
            if item.startswith("moveTo"):
                x = itemSplit[1]
                y = itemSplit[2]
                self.listbox.insert(tk.END,f"{x},{y}")
            elif item.startswith("SendKeys"):
                column = itemSplit[1]
                self.listbox.insert(tk.END,f"SendKeys,{column}")
            elif item.startswith("PressKeys"):
                self.listbox.insert(tk.END,"SelectAll")
            elif item.startswith("PressKey"):
                column = itemSplit[1]
                if column == "\\b":
                    column = "Backspace"
                self.listbox.insert(tk.END,f"{column}")
            else:
                self.listbox.insert(tk.END,item)

    def saveAuto(self):
        saveFile = tkinter.filedialog.asksaveasfile(initialdir="C:",filetypes=macroFileTypes)
        saveFile = f"{saveFile.name}.p"
        if saveFile is None:
            return
        pickle.dump(self.listOfAutos,open(saveFile,"wb"))
    
    def runItems(self):
        t.clear()
        self.runButton.config(state="disable")
        try:
            delay = float(self.delayEntry.get())
        except:
            delay = 0.5

        try:
            for line in self.fileContents.get_children():
                values = self.fileContents.item(line)["values"]
                for item in self.listOfAutos:
                    time.sleep(delay)
                    itemSplit = item.split(",")
                    if item.startswith("moveTo"):
                        mouse.move(itemSplit[1],itemSplit[2])
                    elif item.startswith("RClick"):
                        mouse.right_click()
                    elif item.startswith("LClick"):
                        mouse.click()
                    elif item.startswith("SendKeys"):
                        index = int(itemSplit[1])
                        keyboard.write(f"{values[index-1]}")
                    elif item.startswith("PressKeys"):
                        for i in range(len(itemSplit)):
                            if i != 0:
                                keyboard.press(itemSplit[i])
                        for i in range(len(itemSplit)):
                            if i != 0:
                                keyboard.release(itemSplit[i])
                    elif item.startswith("PressKey"):
                        key = itemSplit[1]
                        keyboard.press_and_release(key)
                self.fileContents.item(line, tags="runOver")
        except Exception as e:
            print(e)
            self.runButton.config(state="active")
            pass
        self.runButton.config(state="active")

    def getListPosition(self):
        try:
            selection = self.listbox.curselection()
            position = selection[0]
        except:
            position = len(self.listOfAutos)
        self.listbox.selection_clear(0, tk.END)
        return position
    
    def addCurPos(self):
        try:
            mousePos = mouse.get_position()
            x, y = mousePos

            y = int(y)
            x = int(x)
            position = self.getListPosition()
            self.listOfAutos.insert(position,f"moveTo,{x},{y}")
            self.listbox.insert(position,f"{x},{y}")
        except Exception as e:
            print(e)

    def addSelectAll(self):
        position = self.getListPosition()
        self.listOfAutos.insert(position,f"PressKeys,ctrl,a")
        self.listbox.insert(position,f"SelectAll")
        
    def addPos(self):
        try:
            x, y = self.xEntry.get(), self.yEntry.get()
            y = int(y)
            x = int(x)
            position = self.getListPosition()
            
            self.listOfAutos.insert(position,f"moveTo,{x},{y}")
            self.listbox.insert(position,f"{x},{y}")
        except:
            pass

    def addRClick(self):
        position = self.getListPosition()
        self.listOfAutos.insert(position,"RClick")
        self.listbox.insert(position,"RClick")
        
    def addClick(self):
        position = self.getListPosition()
        self.listOfAutos.insert(position,"LClick")
        self.listbox.insert(position,"LClick")

    def addEnter(self):
        position = self.getListPosition()
        self.listOfAutos.insert(position,"PressKey,Enter")
        self.listbox.insert(position,"Enter")

    def addBack(self):
        position = self.getListPosition()
        self.listOfAutos.insert(position,"PressKey,\\b")
        self.listbox.insert(position,"Backspace")
        
    def removeFromList(self):
        selection = self.listbox.curselection()
        for item in selection:
            self.listOfAutos.pop(item)
            self.listbox.delete(item)

    def addColumn(self,event):
        column = self.fileContents.identify_column(event.x).replace("#","")
        position = self.getListPosition()
        self.listOfAutos.insert(position,f"SendKeys,{column}")
        self.listbox.insert(position,f"SendKeys,{column}")
        
    def loadFile(self):
        try:
            self.fileContents.unbind("<Double-1>",self.addColumn)
            self.fileContents.destroy()
        except:
            pass

        self.fileContents = ttk.Treeview(self.treeFrame,show="headings")
        readFile = tkinter.filedialog.askopenfilename(initialdir="C:",filetypes=filetypes)
        firstRowHeader = self.headerVar.get()
        count = 0
        with open(readFile,'r') as f_:
            lines = f_.read()[3:].split('\n')
            
            headerTuple = ()
            header = lines[0].split(",")
            for item in range(len(header)):
                if firstRowHeader:
                    headerTuple += (header[item],)
                else:
                    headerTuple += (item,)

            self.fileContents['columns'] = headerTuple
            for item in range(len(header)):
                width = int(235/len(header))
                if firstRowHeader:
                    self.fileContents.column(header[item],width=width,anchor=tk.CENTER)
                else:
                    self.fileContents.column(item,width=width,anchor=tk.CENTER)
            
            for heading in headerTuple:
                self.fileContents.heading(heading,text=heading)

            if firstRowHeader:
                lines.pop(0)
                
            for line in lines:
                lineTuple = ()
                for item in line.split(","):
                    lineTuple += (item,)
                self.fileContents.insert("",count,values=lineTuple)
                count += 1
        self.fileContents.place(x=5,y=5,width=285,height=195)
        self.fileContents.bind("<Double-1>",self.addColumn)
        
Application()
