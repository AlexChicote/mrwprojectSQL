import sqlite3
import ids_and_more as im

#create a database or connect to one
conn=sqlite3.connect('./database/ot_clients.db')
#conn.row_factory=sqlite3.Row
#create a cursor
c=conn.cursor()
#create a table
c.execute("SELECT *,oid from children; ")

records=c.fetchall()
print_records=''
for record in records:
    print_records+=str(record[0])+' '+record[1]+'\n'
#close connection
conn.commit()
conn.close()
''', 'name', 'last_name', 'middle_nam', 'ei_numbet', 'month', 'day', 'year', 'address',
 'apt', 'city', 'zip', 'parent', 'agency']'''
