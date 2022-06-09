




##Create a table
c.execute('''CREATE TABLE clients
        (ID INT PRIMARY KEY     NOT NULL,
         name           TEXT    NOT NULL,
         last_name      text    NOT NULL,
         middle_nam     text     NOT NULL,
         ei_numbet       text    NOT NULL,
         month          char(2)  NOT NULL,
         day            char(2) NOT NULL,
         year           char(2)  NOT NULL,
         address        varchar(30) NOT NULL,
         apt            varchar(10) NOT NULL,
         city           varchar(20) NOT NULL,
         zip            char(6)  NOT NULL,
         parent         varchar(25) NOT NULL,
         agency         varchar(20) NOT NULL); ''')



"""c.execute("""create table clients (
        first_name text,
        last_name text,
        address1 text,
        apt text,
        city text,
        zip_code integer,
        parent_name text
        )""")"""

c.execute("""create table activity (
                client text,
                agency text,
                fee float,
                type text,
                date execution)""")



c.execute("""create table fees (
                        fee_name text,
                        agency text,
                        service text,
                        fee float)""")



c.execute("""alter table clients add column
                                ei_number integer""")



c.execute("SELECT name FROM sqlite_master WHERE type='table';")
                                print(c.fetchall())#commit changes
data=c.execute("SELECT * from clients; ")
print(list(map(lambda x: x[0],c.description)))
"""for num, line in enumerate(data.description):
    print(num,line[0], '\n')
"""
"""
clients columns
['index', 'agency', 'activity', 'reception_date', 'dob', 'ei_number', 'age', 'execution_date', 'first_name', 'last_name', 'middle_name', 'address', 'ap
t', 'city', 'zip_code', 'parent', 'email']
"""
"""
            c.execute("INSERT INTO  clients VALUES (:first_name,:last_name,:middle_name,
                        :ei_number,:dob,:age,:address,:apt,:city,:zip_code,:parent,:agency,:email,:reception_date",
                    {'first_name':self.first_name.get(),
                    'last_name':self.last_name.get(),
                    'middle_name':self.middle_name.get(),
                    'ei_number':self.ei_number.get(),
                    'dob':self.dob.get(),
                    'age':age,
                    'address':self.address.get(),
                    'apt':self.apt.get(),
                    'city':self.city.get(),
                    'zip':self.zip_code.get(),
                    'parent':self.parent.get(),
                    'agency':self.agency.get(),
                    'email':self.email.get(),
                    'reception_date': date.today()
                    })
"""


"""
cursor.execute("SELECT first_name,last_name,oid
    FROM    clients where oid in (select oid from clients order by oid desc limit 5);")
print(cursor.fetchall())
"""
