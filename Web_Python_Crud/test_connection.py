import pyodbc

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=EDITOZ-ROCKET;'
                      'DATABASE=db_biblioteca;'
                      'UID=Django_Web;'
                      'PWD=12345678')

cursor = conn.cursor()
cursor.execute('SELECT 1')
print(cursor.fetchone())