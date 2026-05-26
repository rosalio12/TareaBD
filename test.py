import sqlite3


conn = sqlite3.connect('chalio.db')
cursor = conn.cursor()
cursor.execute('''create table if not exists users (id int  primary key AUTOINCREMENT, name text NOT NULL,telefono TEXT)''')
cursor.execute("insert into users (name, telefono) values ('Rosalio', '1234567890')")
conn.commit()


def select_01():
   conn = conectar()
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM users")
    for r in  cursor.fetchall():
       print(r)
    clonn.close()
   
   def select_02():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    for r in  cursor.fetchall():
       print(r)
       clon.close()

conn.close()