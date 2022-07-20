import sqlite3
#import ids_and_more as im
import credentials.ids_and_more as im
#create a database or connect to one
conn=sqlite3.connect('./database/ot_clients.db')
#conn.row_factory=sqlite3.Row
#create a cursor
c=conn.cursor()

# c.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(c.fetchall())
#c.execute("SELECT *,ei_number,oid from clients; ")
data=c.execute("SELECT * from clients; ")
print(list(map(lambda x: x[0],c.description)))
records=c.fetchall()
for num, line in enumerate(data.description):
    print(num,line[0], '\n')

# for record in records:
#     print(record[10],record[5])#print_records+=str(record[0])+' '+record[1]+'\n')
#close connection
conn.commit()
conn.close()
''', 'name', 'last_name', 'middle_nam', 'ei_numbet', 'month', 'day', 'year', 'address',
 'apt', 'city', 'zip', 'parent', 'agency']'''
