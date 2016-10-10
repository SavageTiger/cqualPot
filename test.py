
from mysql import connector

conn = connector.connect(user='sven', password='test', port=3309, database='mysql')

cursor = conn.cursor()
#cursor.execute('select \'a\' as id, *, (select id from customer where id like \'%\' || substr(company.id, 1, 4) || \'%\' limit 1) as custId from company left join customer on company.id = customer.id left join user_agent on company.id = user_agent.id')
cursor.execute('select * from test')


print(cursor.description)

row = cursor.fetchone()

while row != None:
    print(row)
    row = cursor.fetchone()