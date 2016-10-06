
from mysql import connector

conn = connector.connect(user='Sven', password='test', port=3309, database='plopjes')

print(conn.cmd_query('SELECT * FROM company WHERE name like \'co%\''))

for row in conn.get_row():
    print(row)