
from mysql import connector

conn = connector.connect(user='sven', password='test', port=3309, database='mysql')

cursor = conn.cursor()
cursor.execute('SELECT * FROM company WHERE name like \'co%\'')
#cursor.execute('select \'a\' as test limit 1')

print(cursor.column_names)

row = cursor.fetchone()

while row != None:
    print(row)
    row = cursor.fetchone()