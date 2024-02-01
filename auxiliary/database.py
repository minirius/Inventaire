import sqlite3

CON = sqlite3.connect("res/database.db")
CUR = CON.cursor()

def creer_table():
    CUR.execute("CREATE TABLE matable(id INTEGER PRIMARY KEY NOT NULL, name MEDIUMTEXT, amount INTEGER, price INTEGER, category MEDIUMTEXT);")

def insert():
    users = [
        ('Per1', 149, 50,'CaLa'),
        ('Per2', 173, 50,'LaCa'), 
        ('Per3', 48, 50,'CaLa'),
        ('Per4', 56, 50,'LaCa'), 
    ]
    CON.execute("DELETE FROM matable")
    CON.executemany("INSERT INTO matable (name, amount, price, category) VALUES(?, ?, ?, ?)", users)
    CON.commit()

def search(yes):
    CUR.execute(f'SELECT * FROM matable WHERE name LIKE "%{yes}%"')
    rows = CUR.fetchall() 
    for row in rows:
        print(row)
    CON.close()
insert()