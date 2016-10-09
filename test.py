
from mysql import connector

conn = connector.connect(user='sven', password='test', port=3309, database='mysql')

cursor = conn.cursor()
cursor.execute('select *, (select id from customer where id like \'%\' || substr(company.id, 1, 4) || \'%\' limit 1) as custId from company')
#cursor.execute('select \'a\' as test limit 1')

print(cursor.column_names)

row = cursor.fetchone()

while row != None:
    print(row)
    row = cursor.fetchone()