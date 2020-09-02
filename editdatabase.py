from tkinter import *
from tkinter import messagebox
import fooddatabase
import sqlite3
import fitness
     
'''
allow 0 value input for food values

'''

def doNothing():
    print("nothing")
def test(evt):
    print("test")

class EditDatabase():
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.db = fooddatabase.Database
        self.ListBoxTotal = 0
        self.foodValuesSorted = []
        self.nameList = []
        self.noMatch = 0
        self.noDoubleMatch = 0
        self.lastSelected = ""
        self.addToListButton = Button(self.frame,text="add",command=self.pre_db_screen)
        self.clear = Button(self.frame,text="Clear All", command=self.clear_fields)
        self.clear.grid(row=3,column=2)
        self.addToListButton.grid(row=2,column=2)       
        self.foodL = Label(self.frame,text="Enter Name")
        self.calL = Label(self.frame,text="Enter Calories")
        self.proL = Label(self.frame,text="Enter Protein")
        self.fatL = Label(self.frame,text="Enter Fats")
        self.carbL = Label(self.frame,text="Enter Carbs")
        self.foodL.grid(row=1,column=0)
        self.calL.grid(row=2,column=0)
        self.proL.grid(row=3,column=0)
        self.fatL.grid(row=4,column=0)
        self.carbL.grid(row=5,column=0)       
        self.enterFoodName = Entry(self.frame)
        self.enterFoodName.grid(row=1,column=1)
        self.enterCals = Entry(self.frame)
        self.enterCals.grid(row=2,column=1)
        self.enterPros = Entry(self.frame)
        self.enterPros.grid(row=3,column=1)
        self.enterFats = Entry(self.frame)
        self.enterFats.grid(row=4,column=1)
        self.enterCarbs = Entry(self.frame)
        self.enterCarbs.grid(row=5,column=1)
        self.refreshButton = Button(self.frame,text="refresh all", command=self.refreshAll)
        self.refreshButton.grid(row=10)
        self.printButton = Button(self.frame,text="Print all", command=self.printAll)
        self.printButton.grid(row=10, column=1)
        self.frame.pack(side=LEFT)
        
        ## RIGHT FRAME ##
        self.rightFrame = Frame(self.master)
        self.scrollbar = Scrollbar(self.rightFrame)
        self.foodListBox = Listbox(self.rightFrame,height=10,selectmode=BROWSE,yscrollcommand=self.scrollbar.set)
        self.foodListBox.bind("<<ListBoxSelect>>", test) #self.edit_selected
        self.scrollbar.config(command=self.foodListBox.yview)
        self.foodListBox.grid(row=1,column=0,columnspan=10, sticky="EW")
        self.scrollbar.grid(row=1,column=1, columnspan=10, sticky="NWS")
        self.editButton = Button(self.rightFrame,text="Edit Selected", command=self.edit_selected)
        self.deleteButton = Button(self.rightFrame,text="Delete Selected", command=self.delete_from_db)
        self.editButton.grid(row=11,column=0)
        self.deleteButton.grid(row=11,column=1)    
        self.rightFrame.pack(side=RIGHT)
        self.populate_listbox()

    def clear_fields(self):
        self.enterFoodName.delete(0, 'end')
        self.enterCals.delete(0, 'end')
        self.enterPros.delete(0, 'end')
        self.enterFats.delete(0, 'end')
        self.enterCarbs.delete(0, 'end')
        
    def pre_db_screen(self):
        if len(self.enterFoodName.get()) != 0:
            if len(self.enterCals.get()) != 0 and len(self.enterPros.get()) != 0 and len(self.enterFats.get()) != 0 and len(self.enterCarbs.get()) != 0:              
                if float(self.enterCals.get()) != 0 and float(self.enterPros.get()) != 0 and float(self.enterFats.get()) != 0 and float(self.enterCarbs.get()) != 0:               
                    if self.lastSelected in self.nameList:
                        if self.enterFoodName.get() in self.nameList:
                            if self.message_handler(2) == True:
                                self.db.edit_to_db(self.enterFoodName.get(),self.enterFoodName.get(),self.enterCals.get(),self.enterPros.get(),self.enterFats.get(),self.enterCarbs.get())
                                self.populate_listbox(1)
                            else: return
                        else:
                            if self.message_handler(3) == True:
                                self.db.edit_to_db(self.lastSelected,self.enterFoodName.get(),self.enterCals.get(),self.enterPros.get(),self.enterFats.get(),self.enterCarbs.get())
                                self.populate_listbox(1)
                            else: return
                    elif self.enterFoodName.get() in self.nameList:
                        if self.message_handler(3) == True:
                            self.db.edit_to_db(self.enterFoodName.get(),self.enterFoodName.get(),self.enterCals.get(),self.enterPros.get(),self.enterFats.get(),self.enterCarbs.get())
                            self.populate_listbox(1) 
                        else: return
                    else:                        
                        self.db.add_to_db(self.enterFoodName.get(),self.enterCals.get(),self.enterPros.get(),self.enterFats.get(),self.enterCarbs.get())
                        self.lastSelected = ""
                        self.populate_listbox(2)               
                else:        
                    print("Food values cannot be 0")   
                    return
            else:
                print("Enter value for all fields")   
                return
        else:
            print("Food name field is blank") 
            return
        self.clear_fields()
        self.lastSelected = ""
        
    def populate_listbox(self,mode = 1):
        if mode == 1:
            self.foodListBox.delete(0,END)
            self.nameList.clear()
            self.names = self.db.get_all_names()
            for tuple in range(0,len(self.names)):
                for name in self.names[tuple]:
                    self.nameList.append(name)
            for name in self.nameList:
                self.foodListBox.insert(END,name)
        if mode == 2:
                self.foodListBox.insert(END,self.enterFoodName.get())
                self.nameList.append(self.enterFoodName.get())
        self.foodListBox.update_idletasks()

    def edit_selected(self):
        self.lastSelected = self.foodListBox.get(ANCHOR)
        self.clear_fields()
        self.name = self.lastSelected
        values = self.db.get_all_inc_name(self.name)
        counter = 0    
        for i in range(0,len(values)):
            for value in values[i]:
                if counter==0:
                    self.enterFoodName.insert(0,value)
                    counter+=1
                elif counter==1:
                    self.enterCals.insert(0,value)
                    counter+=1
                elif counter==2:
                    self.enterPros.insert(0,value)
                    counter+=1
                elif counter==3:
                    self.enterFats.insert(0,value)
                    counter+=1
                elif counter==4:
                    self.enterCarbs.insert(0,value)
                    counter+=1
        
    def delete_from_db(self):
        if self.message_handler(1) == True:
            self.db.delete_row(self.foodListBox.get(ANCHOR))
            self.ListBoxTotal -= 1
            self.foodListBox.delete(ANCHOR)
            self.clear_fields()
        else:
            print("not deleted")

    def message_handler(self,mode):
        if mode == 1:
            result = messagebox.askyesno("Confirm Delete", "Deleting {} is permanent, confirm delete?".format(self.foodListBox.get(ANCHOR)))
            if result == True:
                return True
            else:
                return False
        if mode == 2:
            result = messagebox.askyesno("Confirm Overwrite", "{} already exists, confirm overwrite?".format(self.enterFoodName.get()))
            if result == True:
                return True
            else:
                return False
        if mode == 3:
            result = messagebox.askyesno("Confirm Overwrite", "This will replace {} with {}; confirm overwrite?".format(self.lastSelected,self.enterFoodName.get()))
            if result == True:
                return True
            else:
                return False

    def refreshAll(self):
        self.foodListBox.delete(0,END)
        self.enterFoodName.delete(0, 'end')
        self.enterCals.delete(0, 'end')
        self.enterPros.delete(0, 'end')
        self.enterFats.delete(0, 'end')
        self.enterCarbs.delete(0, 'end')
        self.ListBoxTotal = 0
        self.foodValuesSorted.clear()
        self.nameList.clear()
        self.noMatch = 0
        self.noDoubleMatch = 0
        self.lastSelected = ""
        self.populate_listbox()
        self.foodListBox.update_idletasks()

    def printAll(self):
        print("--------------------------")
        print("nameList: ",self.nameList)
        print("noMatch: ",self.noMatch)
        print("noDoubleMatch: ",self.noDoubleMatch)
        print("lastSelected: ", self.lastSelected)
        print("--------------------------")




