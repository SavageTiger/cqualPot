
from mysql import connector

conn = connector.connect(user='sven', password='test', port=3309, database='mysql')

cursor = conn.cursor()
#cursor.execute('SELECT * FROM company WHERE name like \'co%\'')
cursor.execute('show databases')

row = cursor.fetchone()

while row != None:
    print(row)
    row = cursor.fetchone()