import sqlite3
connection = sqlite3.connect("view.db")
print("Database opened successfully")
cursor = connection.cursor()
#delete
#cursor.execute('''DROP TABLE Student_Info;''')
connection.execute("create table V (id INTEGER PRIMARY KEY ,view INTEGER  NOT NULL)")
print("Table created successfully")
connection.close()   
