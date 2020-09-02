from tkinter import *
import editdatabase as edb
import history as h
import fooddatabase as db
import sqlite3

def doNothing():
    pass

'''
Testing commit
repr() then eval() to save list to string and then "de-string" back to object
save totals needs to "de-list" food names as its unsupported type of type "TEXT" in sqlite. Save as string
'''

class MainMenu():
    def __init__(self, master):
        self.master = master
        self.Mainframe = Frame(self.master)
        self.Mainframe.pack()
        self.m_menu = Menu(self.Mainframe)
        self.master.config(menu=self.m_menu)
        self.subMenu = Menu(self.m_menu)
        self.m_menu.add_cascade(label="File", menu=self.subMenu)
        self.subMenu.add_command(label="New", command=doNothing)
        self.subMenu.add_command(label="Open", command=doNothing)
        self.subMenu.add_command(label="Edit Food Database", command=lambda:self.open_editDb())
        self.subMenu.add_separator()
      
    def open_editDb(self):
        self.editb = Toplevel(self.master)
        self.run = self.edb.EditDatabase(self.editDb)       

class ToolBar():
    def __init__(self,master):
        self.master = master
        self.toolbar = Frame(self.master)
        self.cal_counter = Button(self.toolbar, text="Calorie Counter", command=self.open_cal_count)
        self.cal_counter.pack(side=LEFT, padx=2, pady=2)
        self.workout_tracker=Button(self.toolbar,text="Workout Tracker", command=doNothing)
        self.workout_tracker.pack(side=LEFT, padx=2, pady=2)
        self.toolbar.pack()
    def open_cal_count(self):
        self.cal_count = Toplevel(self.master)
        self.run = CalCounter(self.cal_count)

class StatusBar():
    def __init__(self, master):
        self.master = master
        self.Statusframe = Frame(self.master)
        self.status = Label(self.master,text="Preped for nothing..",bd=1,relief=SUNKEN,anchor=W)
        self.status.pack(fill=X)
        self.Statusframe.pack(side=BOTTOM, fill=X)
        
class MainWindow():
    def __init__(self,master):
        getMenu = MainMenu(master)
        getToolbar = ToolBar(master)
        getStatus = StatusBar(master)
     
class CalCounter():
    def __init__(self, master):
        self.master = master
        getMenu = MainMenu(self.master)
        # *******************************LEFT FRAME****************************
        self.frame = Frame(self.master,relief=SUNKEN,bg="blue")
        self.times_clicked = 0
        self.uniqueItems = 0
        self.lastLabelNumber = 0
        self.ListBoxTotal = 0
        self.calCalcTitle = Label(self.frame,text="Select Food & Enter Amount")
        self.calCalcTitle.grid(row=0,column=0) 
        self.scrollbar = Scrollbar(self.frame)
        self.foodListBox = Listbox(self.frame,height=4,yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.foodListBox.yview)
        self.foodListBox.grid(row=2,column=0, sticky="EW")
        self.scrollbar.grid(row=2,column=1, columnspan=4, sticky="NWS")
        self.populate_listbox()
        self.inputAmount = Entry(self.frame)
        self.inputAmount.grid(row=3,column=0,sticky="EW")
        self.add_food = Button(self.frame,text="add to list",command= lambda:self.add_to_listbox())
        self.add_food.grid(row=4,column=0,sticky="EW")       
        self.saveButton = Button(self.frame,text="Save", command=self.save_totals)
        self.saveButton.grid(row=5)
        self.viewHistory = Button(self.frame,text="View All History", command=self.open_history)
        self.viewHistory.grid(row=6)
        self.createDatabaseButton = Button(self.frame,text="Create History Database", command= lambda:db.Database.create_tables(2))
        self.createDatabaseButton.grid(row=7)
        
        self.frame.pack(side=LEFT,fill=Y)    

        # *******************************RIGHT FRAME****************************
        self.right_frame = Frame(self.master,relief=SUNKEN,bg="green")     
        self.amountLabels = []
        self.foodNameLabels = []
        self.foodValuesSorted= []
        self.clearButtonList = []
        self.SubtotalCalsLabelList=[]
        self.SubtotalProsLabelList=[]
        self.SubtotalFatsLabelList=[]
        self.SubtotalCarbsLabelList=[]
        self.totalsLabel = Label(self.right_frame,text="Totals")
        self.totalsLabel.grid(row=0, column=0, columnspan=4, sticky="NEW")        
        self.totalsLabelCals = Label(self.right_frame,text="Calories")
        self.totalsLabelCals.grid(row=1, column=0,sticky="WE")
        self.totalCals = Label(self.right_frame,text="0")
        self.totalCals.grid(row=2, column=0,sticky="WE")       
        self.totalsLabelPros = Label(self.right_frame,text="Protein")
        self.totalsLabelPros.grid(row=1, column=1,sticky="WE")
        self.totalPros = Label(self.right_frame,text="0")
        self.totalPros.grid(row=2, column=1,sticky="WE")     
        self.totalsLabelFats = Label(self.right_frame,text="Fats")
        self.totalsLabelFats.grid(row=1, column=2,sticky="WE")
        self.totalFats = Label(self.right_frame,text="0")
        self.totalFats.grid(row=2, column=2,sticky="WE")      
        self.totalsLabelCarbs = Label(self.right_frame,text="Carbs")
        self.totalsLabelCarbs.grid(row=1, column=3,sticky="WE")
        self.totalCarbs = Label(self.right_frame,text="0")
        self.totalCarbs.grid(row=2, column=3,sticky="WE")               
        self.foodsLabel = Label(self.right_frame,text="Food")
        self.foodsLabel.grid(row=4, column=0, columnspan=4)
        self.foodAmountLabel = Label(self.right_frame,text="#",relief=SUNKEN)
        self.foodAmountLabel.grid(row=5,column=0,sticky="EW")
        self.foodNameLabel = Label(self.right_frame,text="Food Name",relief=SUNKEN)
        self.foodNameLabel.grid(row=5,column=1,columnspan=3,sticky="WE")
        self.right_frame.pack(side=RIGHT,fill=Y)

    def open_history(self):
        self.history = Toplevel(self.master)
        self.run = h.History(self.history)
        
    def clear_totals(self):
        self.clearButton.grid_remove()
        self.totalCals['text'] = "0"
        self.totalPros['text'] = "0"
        self.totalFats['text'] = "0"  
        self.totalCarbs['text'] = "0"
        for i in range(0,self.times_clicked):
            self.foodNameLabels[i].grid_remove()
            self.amountLabels[i].grid_remove()
            self.SubtotalCalsLabelList[i].grid_remove()
            self.SubtotalProsLabelList[i].grid_remove()
            self.SubtotalFatsLabelList[i].grid_remove()
            self.SubtotalCarbsLabelList[i].grid_remove()
        del self.SubtotalCalsLabelList[:]
        del self.SubtotalProsLabelList[:]
        del self.SubtotalFatsLabelList[:]
        del self.SubtotalCarbsLabelList[:]
        del self.amountLabels[:]
        del self.foodNameLabels[:]
        del self.foodValuesSorted[:]
        self.times_clicked=0

    def populate_listbox(self):
        self.names = db.Database.get_all_names()
        nameList = []   
        for tuple in range(0,len(self.names)):
            for name in self.names[tuple]:
                nameList.append(name)
        if self.ListBoxTotal == 0:
            for name in nameList:
                self.foodListBox.insert(END,name)
                self.ListBoxTotal += 1
        if self.ListBoxTotal < len(nameList):
            for name in nameList[self.ListBoxTotal:]:
                self.foodListBox.insert(END,name)
                self.ListBoxTotal += 1
         
    def add_to_listbox(self):       #### FIX THIS YOU FUCKING CUNT, USE LIST COMPREHSION
        self.noMatches = 0
        print("add_to_listbox")
        if len(self.inputAmount.get()) >0 and float(self.inputAmount.get()) > 0 and len(self.foodListBox.get(ANCHOR)) > 0:
            if len(self.foodNameLabels) == 0: #check if any labels are created, if none exist match foodselected to food in list and pass to foodmaths
                self.food_maths()        
            else:  # IF food labels exist and IF food selected match Food Label in list
                #self.add_to_existing([i for i in range(0,len(self.foodNameLabels)) if self.foodNameLabels[i]["text"]== self.foodListBox.get(ANCHOR)])
                for i in range(0,len(self.foodNameLabels)):
                  if self.foodNameLabels[i]["text"]== self.foodListBox.get(ANCHOR):    
                      self.add_to_existing(i)
                  else:
                      self.noMatches +=1 # if nothing matches then create new labels
            if self.noMatches == len(self.foodNameLabels):
                print("noMatch == len(foodNameLabels)")
                self.food_maths() 
        else:
            print("Select food and amount before pressing add")   
                  
    def food_maths(self):
        values = db.Database.get_values_from_name(self.foodListBox.get(ANCHOR))
        self.cals = 0
        self.protein = 0
        self.fat= 0
        self.carbs= 0
        counter = 0   
        for i in range(0,len(values)):
            for value in values[i]:
                if counter==0:
                    self.cals+= float(value)
                    counter+=1
                elif counter==1:
                    self.protein+=float(value)
                    counter+=1
                elif counter==2:
                    self.fat+=float(value)
                    counter+=1
                elif counter==3:
                    self.carbs+=float(value)
        self.foodValuesSorted.append((self.cals,self.protein,self.fat,self.carbs))
        self.create_new_labels()

    def add_to_existing(self,labelNumber):
        self.labelNumber = labelNumber
        self.newTotalMultiplier = float(self.amountLabels[self.labelNumber].cget("text")) + float(self.inputAmount.get())                    
        self.amountLabels[self.labelNumber]["text"] = self.newTotalMultiplier  
        self.SubtotalCalsLabelList [self.labelNumber]['text'] = "{0:.1f}".format((self.foodValuesSorted[self.labelNumber][0]*self.newTotalMultiplier))                
        self.SubtotalProsLabelList [self.labelNumber]['text'] = "{0:.1f}".format((self.foodValuesSorted[self.labelNumber][1]*self.newTotalMultiplier))                     
        self.SubtotalFatsLabelList [self.labelNumber]['text'] = "{0:.1f}".format((self.foodValuesSorted[self.labelNumber][2]*self.newTotalMultiplier))                      
        self.SubtotalCarbsLabelList[self.labelNumber]['text'] = "{0:.1f}".format((self.foodValuesSorted[self.labelNumber][3]*self.newTotalMultiplier))
        self.calculate_totals()
                                                                                        
    def create_new_labels(self):
        if self.times_clicked == 0:  # move clear button down each time label is added
             self.clearButton = Button(self.right_frame,text="Clear",command=self.clear_totals)
             self.clearButton.grid(row=8+self.times_clicked,columnspan=4)
        elif self.times_clicked > 0: 
             self.clearButton.grid_remove()
             self.clearButton = Button(self.right_frame,text="Clear",command=self.clear_totals)
             self.clearButton.grid(row=9+self.times_clicked,columnspan=4)     
        
                        #Create labels addressed by times_clicked 
        self.SubtotalCalsLabelList.append(Label(self.right_frame,relief=SUNKEN,text= "{0:.1f}".format((self.foodValuesSorted[self.times_clicked][0])*float(self.inputAmount.get()))))
        self.SubtotalProsLabelList.append(Label(self.right_frame,relief=SUNKEN,text= "{0:.1f}".format((self.foodValuesSorted[self.times_clicked][1])*float(self.inputAmount.get()))))
        self.SubtotalFatsLabelList.append(Label(self.right_frame,relief=SUNKEN,text= "{0:.1f}".format((self.foodValuesSorted[self.times_clicked][2])*float(self.inputAmount.get()))))
        self.SubtotalCarbsLabelList.append(Label(self.right_frame,relief=SUNKEN,text="{0:.1f}".format((self.foodValuesSorted[self.times_clicked][3])*float(self.inputAmount.get()))))

                        #Place Labels in grid(row) depending on times_clicked
        self.amountLabels.append(Label(self.right_frame,relief=SUNKEN,text=self.inputAmount.get()))
        self.amountLabels[self.times_clicked].grid(row=5+self.times_clicked,sticky="EW")
        self.foodNameLabels.append(Label(self.right_frame,relief=SUNKEN,text=self.foodListBox.get(ANCHOR)))
        self.foodNameLabels[self.times_clicked].grid(row=5+self.times_clicked,column=1,columnspan=3,sticky="WE")                        
        self.SubtotalCalsLabelList[self.times_clicked].grid(row=5+self.times_clicked,column=5,sticky="WE")
        self.SubtotalProsLabelList[self.times_clicked].grid(row=5+self.times_clicked,column=6,sticky="WE")
        self.SubtotalFatsLabelList[self.times_clicked].grid(row=5+self.times_clicked,column=7,sticky="WE")
        self.SubtotalCarbsLabelList[self.times_clicked].grid(row=5+self.times_clicked,column=8,sticky="WE")      
        self.times_clicked +=1      
        self.calculate_totals()

    def calculate_totals(self):
        self.newTotalCals = 0
        self.newTotalPros = 0
        self.newTotalFats = 0
        self.newTotalCarbs= 0
        for i in range(0,len(self.amountLabels)):
            self.newTotalCals +=  float(self.SubtotalCalsLabelList[i].cget("text"))           
            self.newTotalPros +=  float(self.SubtotalProsLabelList[i].cget("text"))        
            self.newTotalFats +=  float(self.SubtotalFatsLabelList[i].cget("text"))          
            self.newTotalCarbs += float(self.SubtotalCarbsLabelList[i].cget("text"))           
        self.totalCals['text'] = "{0:.2f}".format(self.newTotalCals)
        self.totalPros['text'] = "{0:.2f}".format(self.newTotalPros)
        self.totalFats['text'] = "{0:.2f}".format(self.newTotalFats)
        self.totalCarbs['text'] = "{0:.2f}".format(self.newTotalCarbs)
                                        
    def save_totals(self): 
        preSaveNames = []
        preSaveAmounts = []
        preSaveTotals = [self.totalCals.cget("text"),self.totalPros.cget("text"),self.totalFats.cget("text"),self.totalCarbs.cget("text")]
        for i in range(0,len(self.foodNameLabels)):
            preSaveNames.append(self.foodNameLabels[i].cget(str("text")))
            preSaveAmounts.append(self.amountLabels[i].cget("text"))
        print(repr(preSaveNames))

        db.Database.insert_history(repr(preSaveNames),repr(preSaveAmounts),repr(preSaveTotals))
                       

def main(): 
    root = Tk()
    run = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
