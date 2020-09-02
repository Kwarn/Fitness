from tkinter import *
import fooddatabase

class History:
    def __init__(self,master):
        self.master = master
        self.frame = Frame(self.master)

        self.dateLabels=[]
        self.foodLabels=[]
        self.amountLabels=[]
        self.totalLabels=[]

        self.date = Label(self.frame,text="Date")
        self.date.grid(row=0,column=0,columnspan=1,sticky="w")
        self.food = Label(self.frame,text="Food")
        self.food.grid(row=0,column=1,columnspan=1)
        self.totals = Label(self.frame,text="Totals")
        self.totals.grid(row=0,column=3, columnspan=1)      
        self.frame.pack()
        self.show_history()

    def show_history(self):
        '''
        needs eval()
        sort out formatting of str "{} chicken, {} ," 


        '''
        dates = []
        food = []
        amount = []
        total = []
        results = fooddatabase.Database.get_history()
        for row in results:
            dates.append(row[0])
            food.append(eval(row[1]))
            print("this is the print: ",food[0][0]) # works, need to append and match food and amount to a dictionary/list 
            amount.append(eval(row[2]))
            total.append(eval(row[3]))

        for i in dates:
            self.dateLabels.append(Label(self.frame,text=i))
        for i in food:
            self.foodLabels.append(Label(self.frame,text="")) ## how to set depending on the amount of food names
       # for i in amount:
       #     self.amountLabels.append(Label(self.frame,text=i))
        for i in total:
            self.totalLabels.append(Label(self.frame,text=i))

        for i in range(len(self.dateLabels)):
            self.dateLabels[i].grid(row=i+1,column=0)
            self.foodLabels[i].grid(row=i+1,column=1)
            self.amountLabels[i].grid(row=i+1,column=2)
            self.totalLabels[i].grid(row=i+1,column=3)
            
    def set_labels(self,food):
       pass

        

        #    self.dateLabels.append(Label(self.frame,text=row))
        #for label in self.dateLabels:
        #    for i in range(len(self.dateLabels)):
        #        label.grid(row=i)

if __name__ == '__main__':
    main()






