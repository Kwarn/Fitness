import sqlite3
import datetime
import time

conn = sqlite3.connect("fooddatabase.db")
conn2 = sqlite3.connect("historydatabase.db")
c = conn.cursor()
c2 = conn2.cursor()
unix = time.time()
date = str(datetime.datetime.fromtimestamp(unix).strftime("%y-%m-%d %H:%M:%S"))

class Database():
    def create_tables(mode):
        print("create_tables(",mode,")")
        if mode == 1:
            c.execute("CREATE TABLE IF NOT EXISTS fooddatabase(Foodname TEXT, Calories REAL, Protein REAL, Fats REAL, Carbs REAL)")
            conn.commit()
        elif mode == 2:
            c2.execute("CREATE TABLE IF NOT EXISTS historydatabase(Datestamp TEXT, Foodnames TEXT, Foodamounts TEXT, Totalvalues TEXT)")
            conn2.commit()
    def add_to_db(foodname,cals,pros,fats,carbs):  
        c.execute("INSERT INTO fooddatabase (Foodname, Calories, Protein, Fats, Carbs) VALUES(?,?,?,?,?)",
                  (foodname,cals,pros,fats,carbs))
        conn.commit()       
        print("Added to database: " + foodname,cals,pros,fats,carbs)

    def edit_to_db(originalName, newFoodName,cals,pros,fats,carbs):  
        c.execute("UPDATE fooddatabase SET Foodname = ? WHERE Foodname = ?", (newFoodName, originalName))       
        c.execute("UPDATE fooddatabase SET Calories = ? WHERE Foodname = ?", (cals, newFoodName))       
        c.execute("UPDATE fooddatabase SET Protein = ? WHERE Foodname = ?", (pros, newFoodName))       
        c.execute("UPDATE fooddatabase SET Fats = ? WHERE Foodname = ?", (fats, newFoodName))       
        c.execute("UPDATE fooddatabase SET Carbs = ? WHERE Foodname = ?", (carbs, newFoodName))
        conn.commit()       
        print("Replaced "+ originalName + " with ",newFoodName,cals,pros,fats,carbs)
              
    def get_all_names():
        c.execute("SELECT Foodname FROM fooddatabase")
        names = c.fetchall()
        return names

    def get_values_from_name(fn):
        c.execute("SELECT Calories, Protein, Fats, Carbs FROM fooddatabase WHERE Foodname == (?)",(fn,))
        values = c.fetchall()
        return values

    def get_all_inc_name(fn):
        c.execute("SELECT Foodname, Calories, Protein, Fats, Carbs FROM fooddatabase WHERE Foodname == (?)",(fn,))
        values = c.fetchall()
        return values

    def delete_row(fn):
        c.execute("DELETE FROM fooddatabase WHERE Foodname = ?", (fn,))
        conn.commit()

    def get_history():
        pass
        #c2.excute("SELECT")

    def insert_history(foodnames,foodamounts,totalvalues):
        c2.execute("INSERT INTO historydatabase(Datestamp, Foodnames, Foodamounts, Totalvalues) VALUES(?,?,?,?)",
                   (date,foodnames,foodamounts,totalvalues))
        conn2.commit()

    def get_history():
        c2.execute("SELECT Datestamp, Foodnames, Foodamounts, Totalvalues FROM historydatabase")
        history_unsorted = c2.fetchall()
        return history_unsorted


