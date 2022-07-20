#!/usr/bin/env python
#import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

import pickle
from datetime import datetime,date
#import pdfrw
import functions as f
from google_drive import service
from google_sheets import sheet
#import sensory_profile_2 as sp
import credentials.ids_and_more as im

import sqlite3

from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload


LARGE_FONT = ['Verdana', 20]


class MRWapp(tk.Tk):

    def __init__(self,*args,**kwargs): #variables(args) dictionaries kwargs

        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self)
        #container.geometry('500x1000')
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure((1,2,3,4,5), weight=1, uniform="row")
        container.grid_columnconfigure((1,2,3,4), weight=1, uniform="column")
        self.OPTIONS=['ei_number','oid']
        self.shared_data = {
            'options': tk.StringVar(self,self.OPTIONS[0]),
            "value": tk.StringVar()
            }
        #self.shared_data['options']
        self.frames = {}
        for F in (StartPage, ManageRecords,DeleteRecord,EditRecord):#, ManageRecords, ManageFees,AddActivity,ManageActivity):

            frame = F(container, self)
            self.frames[F] = frame


            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(StartPage)



    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

    def callback(self,cont):
        sensory_profile_for_TKinter_Testing.main()
        frame = self.frames[cont]
        frame.tkraise()




class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)  ##parent refers to our main class MRWapp
        label = tk.Label(self, text='Choose Activity', font = LARGE_FONT).grid(row=0,column=0,pady=10,padx=10,sticky='ew')

        button1 = tk.Button(self, text ='Manage Children', font=("bold", 16),command= lambda:\
                            controller.show_frame(ManageRecords)).grid(row=2,column=0,sticky='ew')

        button2 = tk.Button(self, text ='Sensory Profile', font=("bold", 16),command= lambda:\
                            controller.show_frame(SensoryProfile)).grid(row=3,column=0,sticky='ew')

        button3 = tk.Button(self, text ='Invoices', font=("bold", 16),command= lambda:\
                            controller.show_frame(Invoices)).grid(row=4,column=0,sticky='ew')



class ManageRecords(tk.Frame): ###Consent and Delay Forms



    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)  ##parent refers to our main class MRWapp

        self.controller = controller

        def add_kid():


            child_dob=datetime.strptime(self.dob.get(),'%m/%d/%Y').date()

            age=f.diff_month(child_dob,date.today())
            avui=date.today()
            #print("AGE", age,child_dob,self.email.get(),'AVUI',avui)

            #create a database or connect to one
            conn=sqlite3.connect('./database/ot_clients.db')
            #create a cursor
            c=conn.cursor()
            #Insert Into table


            sqlite_query="""INSERT INTO clients
                          (first_name, last_name, middle_name,ei_number,dob,age,address,apt,city,zip_code,parent, agency,email,reception_date)
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
            data_tuple = (self.first_name.get(),self.last_name.get(), self.middle_name.get(), self.ei_number.get(), child_dob, age,self.address.get(),
                        self.apt.get(),self.city.get(),self.zip_code.get(),self.parent.get(),self.agency.get(),self.email.get(),date.today())
            c.execute(sqlite_query,data_tuple)


            #commit changes
            conn.commit()
            #close connection
            conn.close()

            [ent.delete(0, tk.END) for ent in self.winfo_children() if isinstance(ent, tk.Entry)]




        label_0 = tk.Label(self, text="Adding a record",width=20,font=("bold", 22)).grid(row=0,columnspan=5,padx=10,pady=20)


        labels=['First Name','Last Name','Middle Name','EI number','DOB mm/dd/yy','address',
                'Apt','city',"zip code",'Parent','Agency','email']

        self.first_name,self.last_name,self.middle_name,self.ei_number=tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()
        self.address,self.apt,self.city,self.zip_code,self.parent,self.agency=tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()
        self.dob, self.email=tk.StringVar(),tk.StringVar()

        entries=[self.first_name,self.last_name,self.middle_name,self.ei_number,self.dob,
                self.address,self.apt,self.city,self.zip_code,self.parent,self.agency,self.email]


        for n in range(len(labels)):
            if labels[n]!='DOB mm/dd/yy':
                my_label=tk.Label(self,text=labels[n],width=20,font=("bold", 16)).grid(row=n+1,column=0)
                tk.Entry(self,width=25,textvariable=entries[n]).grid(row=n+1,column=1)
            else:
                my_label=tk.Label(self,text=labels[n],width=20,font=("bold", 16)).grid(row=n+1,column=0)
                DateEntry(self,width=25,locale='en_US', date_pattern='mm/dd/y',textvariable=entries[n]).grid(row=n+1,column=1)



        tk.Button(self,text='Back to Home',command=\
                           lambda: controller.show_frame(StartPage)).grid(row=len(labels)+1,columnspan=2)
        tk.Button(self, text='Add Record',width=10,bg='brown',
                fg='black',font=("bold",16),
                command=add_kid).grid(row=len(labels)+2,columnspan=3)

        tk.Button(self,text='Delete/Edit Record',command=\
                           lambda: controller.show_frame(DeleteRecord)).grid(row=len(labels)+3,columnspan=2)


class DeleteRecord(tk.Frame): ###Consent and Delay Forms



    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)  ##parent refers to our main class MRWapp

        self.controller = controller


        def delete_kid():



            #create a database or connect to one
            conn=sqlite3.connect('./database/ot_clients.db')
            #create a cursor
            c=conn.cursor()
            #Insert Into table
            global value, options
            options = self.controller.shared_data["options"].get()
            value=self.controller.shared_data["value"].get()

            print('options',options)
            print('value',value)

            if options=='ei_number':

                sqlite_query=f"""SELECT cast(oid as text),cast(ei_number as text),first_name,last_name FROM clients where cast(ei_number as text)={value};"""
                sqlite_out=f"""DELETE FROM clients WHERE cast(ei_number as text)={value};"""
            elif options=='oid':

                sqlite_query=f"""SELECT cast(oid as text), first_name, last_name FROM clients where oid={value};"""
                sqlite_out=f"""DELETE FROM clients WHERE oid={value};"""
            print(sqlite_query)
            c.execute(sqlite_query)
            for record in c.fetchall():
                print(record)
                answer=tk.messagebox.askyesno('Yes|No', message=' '.join(record) +'\n'+'Do you want to proceed?')
                if answer:
                    print("Ves A Cagar")

                    c.execute(sqlite_out)

                    #sp.scoring_sensory_profile(predata,item['values'])

            #commit changes
            conn.commit()
            #close connection
            conn.close()

            [ent.delete(0, tk.END) for ent in self.winfo_children() if isinstance(ent, tk.Entry)]

        def update():

            options = self.controller.shared_data["options"].get()
            value=self.controller.shared_data["value"].get()
            print('Updating', options,value)
            print('First Name',first_name_editor.get())
            print('Last Name',last_name_editor.get())
            #create connection
            conn=sqlite3.connect('./database/ot_clients.db')
            #create a cursor
            c=conn.cursor()

            c.execute("""UPDATE clients SET
                        first_name = :first,
                        last_name  = :last,
                        middle_name = :middle,
                        dob= :dob,
                        address= :address,
                        apt=:apt,
                        city=:city,
                        zip_code= :zip_code,
                        parent=:parent,
                        agency=:agency,
                        email=:email
                        where ei_number=:ei_number""",
                        {'first': first_name_editor.get(),
                        'last':last_name_editor.get(),
                        'middle':middle_name_editor.get(),
                        'dob':dob_date_editor.get(),
                        'address':address_editor.get(),
                        'apt':apt_editor.get(),
                        'city':city_editor.get(),
                        'zip_code':zip_editor.get(),
                        'parent':parent_editor.get(),
                        'agency':agency_editor.get(),
                        'email':email_editor.get(),
                        'ei_number':value
                        })

            #Comit your changes
            conn.commit()
            #Close the connection
            conn.close()

            editor.destroy()







        def edit():
            global editor
            editor=Tk()
            editor.title("Update a record")
            editor.geometry("500x500")

            self.options = controller.shared_data['options'].get()
            self.value=controller.shared_data['value'].get()

            conn=sqlite3.connect('./database/ot_clients.db')
            #create a cursor
            c=conn.cursor()

            print('VALUE',self.value,'OPTION',self.options)


            if self.value:

                if self.options=='ei_number':

                    sqlite_query=f"""SELECT first_name,last_name,middle_name,ei_number,dob,address,apt,
                                        city,zip_code,parent,agency,email FROM clients where cast(ei_number as text)={self.value};"""
                    #sqlite_out=f"""DELETE FROM clients WHERE cast(ei_number as text)={self.choice}"""
                elif self.options=='oid':
                    sqlite_query=f"""SELECT first_name,last_name,middle_name,ei_number,dob,address,apt,
                                        city,zip_code,parent,agency,email FROM clients where oid={self.value};"""

                c.execute(sqlite_query)
                records=c.fetchall()
                if len(records)>0:
                    print(records[0])
                else:
                    print("No such ei_number")
            else:
                print('NO VALUE?')

            #Comit your changes
            conn.commit()
            #Close the connection
            conn.close()


            # editor_labels=['First Name','Last Name','Middle Name','EI number','DOB mm/dd/yy','address',
            #         'Apt','city',"zip code",'Parent','Agency','email']
            # #
            # self.first_name,self.last_name,self.middle_name,self.ei_number=tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()
            # self.address,self.apt,self.city,self.zip_code,self.parent,self.agency=tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()
            # self.dob, self.email=tk.StringVar(),tk.StringVar()
            # self.first_name.trace('w', self.update)
            #
            # self.entries=[self.first_name,self.last_name,self.middle_name,self.ei_number,self.dob,
            #         self.address,self.apt,self.city,self.zip_code,self.parent,self.agency,self.email]
            #
            # if records:
            #     for n in range(len(self.labels)):
            #         if self.labels[n]!='DOB mm/dd/yy':
            #             self.my_label=tk.Label(editor,text=self.labels[n],width=20,font=("bold", 16)).grid(row=n+2,column=0)
            #             self.my_entry=tk.Entry(editor,width=25,textvariable=self.entries[n])
            #             self.my_entry.insert(0,records[0][n])
            #             self.my_entry.grid(row=n+2,column=1)
            #
            #
            #         else:
            #             self.my_label=tk.Label(editor,text=self.labels[n],width=20,font=("bold", 16)).grid(row=n+2,column=0)
            #             self.date_entry=DateEntry(editor,width=25,date_pattern='y-mm-dd',textvariable=self.entries[n])
            #             self.date_entry.set_date(records[0][n])
            #             #self.date_entry.insert(0,records[0][n])
            #             self.date_entry.grid(row=n+2,column=1)
            # entries=self.entries
            # print('ENTRIES IN EDIT BEFORE GOING TO UPDATE',entries)
            # print('FIRST ENTRY',entries[0].get())

            global first_name_editor
            global last_name_editor
            global middle_name_editor
            global dob_date_editor
            global address_editor
            global apt_editor
            global city_editor
            global zip_editor
            global parent_editor
            global agency_editor
            global email_editor


            first_name_editor=tk.Entry(editor,width=25)
            first_name_editor.grid(row=2,column=1)
            first_name_editor.insert(0,records[0][0])
            lfirst_name_abel=tk.Label(editor,text='First Name',width=20,font=("bold", 16)).grid(row=2,column=0)
            last_name_editor=tk.Entry(editor,width=25)
            last_name_editor.grid(row=3,column=1)
            last_name_editor.insert(0,records[0][1])
            last_name_label=tk.Label(editor,text='Last Name',width=20,font=("bold", 16)).grid(row=3,column=0)
            middle_name_editor=tk.Entry(editor,width=25)
            middle_name_editor.grid(row=4,column=1)
            middle_name_editor.insert(0,records[0][2])
            middle_name_label=tk.Label(editor,text='Middle Name',width=20,font=("bold", 16)).grid(row=4,column=0)
            dob_date_editor=tk.Entry(editor,width=25)
            dob_date_editor.grid(row=5,column=1)
            dob_date_editor.insert(0,records[0][4])
            dob_date_label=tk.Label(editor,text='dob',width=20,font=("bold", 16)).grid(row=5,column=0)
            address_editor=tk.Entry(editor,width=25)
            address_editor.grid(row=6,column=1)
            address_editor.insert(0,records[0][5])
            address_label=tk.Label(editor,text='Address',width=20,font=("bold", 16)).grid(row=6,column=0)
            apt_editor=tk.Entry(editor,width=25)
            apt_editor.grid(row=7,column=1)
            apt_editor.insert(0,records[0][6])
            apt_label=tk.Label(editor,text='Apt',width=20,font=("bold", 16)).grid(row=7,column=0)
            city_editor=tk.Entry(editor,width=25)
            city_editor.grid(row=8,column=1)
            city_editor.insert(0,records[0][7])
            city_label=tk.Label(editor,text='City',width=20,font=("bold", 16)).grid(row=8,column=0)
            zip_editor=tk.Entry(editor,width=25)
            zip_editor.grid(row=10,column=1)
            zip_editor.insert(0,records[0][8])
            zip_label=tk.Label(editor,text='Zip code',width=20,font=("bold", 16)).grid(row=10,column=0)
            parent_editor=tk.Entry(editor,width=25)
            parent_editor.grid(row=11,column=1)
            parent_editor.insert(0,records[0][9])
            parent_label=tk.Label(editor,text='Parent',width=20,font=("bold", 16)).grid(row=11,column=0)
            agency_editor=tk.Entry(editor,width=25)
            agency_editor.grid(row=12,column=1)
            agency_editor.insert(0,records[0][10])
            Agency_label=tk.Label(editor,text='Agency',width=20,font=("bold", 16)).grid(row=12,column=0)
            email_editor=tk.Entry(editor,width=25)
            email_editor.grid(row=13,column=1)
            email_editor.insert(0,records[0][11])
            email_label=tk.Label(editor,text='Email',width=20,font=("bold", 16)).grid(row=13,column=0)



            tk.Button(editor,text='Back to Home',command=\
                               lambda: controller.show_frame(StartPage)).grid(row=18,columnspan=2)
            tk.Button(editor, text='Update Record',width=10,bg='brown',
                    fg='black',font=("bold",16),
                    command=update).grid(row=19,columnspan=3)


            #
            # tk.Button(editor,text='Back to Home',command=\
            #                    lambda: controller.show_frame(StartPage)).grid(row=len(self.labels)+6,columnspan=2)
            # tk.Button(editor, text='Update Record',width=10,bg='brown',
            #         fg='black',font=("bold",16),
            #         command=lambda: update(entries)).grid(row=len(self.labels)+7,columnspan=3)

        label_0 = tk.Label(self, text="Deleting a record",width=20,font=("bold", 22)).grid(row=0,columnspan=5,padx=10,pady=20)

        OPTIONS=['ei_number','oid']
        #self.last_name=tk.StringVar()
        #self.variable=tk.StringVar(self,OPTIONS[0])

        #entries=[self.last_name,self.value]


        #tk.Label(self,text='Last Name',width=20,font=("bold", 16)).grid(row=1,column=0)
        tk.Label(self,text='Choose filter',width=20,font=("bold", 16)).grid(row=1,column=0)
        tk.OptionMenu(self,self.controller.shared_data["options"],*self.controller.OPTIONS).grid(row=1,column=1)
        #tk.Entry(self,width=15,textvariable=self.last_name).grid(row=1,column=1)
        tk.Entry(self,width=6,textvariable=self.controller.shared_data["value"]).grid(row=1,column=2)
        #tk.OptionMenu(self,variable, *OPTIONS,width=20,font=("bold", 16)).grid(row=3,column=1)


        tk.Button(self,text='Manage Records',command=\
                           lambda: controller.show_frame(ManageRecords)).grid(row=5,columnspan=2)
        tk.Button(self,text='Delete Record',command=delete_kid).grid(row=6,columnspan=3)
        tk.Button(self,text='Edit record',command=edit).grid(row=7,columnspan=3)
        tk.Button(self,text='Back Home',command=\
                           lambda: controller.show_frame(StartPage)).grid(row=8,columnspan=3)

class EditRecord(tk.Frame): ###Consent and Delay Forms



    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)  ##parent refers to our main class MRWapp

        self.controller = controller
        self.options = controller.shared_data['options'].get()
        self.value=controller.shared_data['value'].get()
        # #create a database or connect to one
        # conn=sqlite3.connect('./database/ot_clients.db')
        # #create a cursor
        # c=conn.cursor()
        # #Insert Into table
        # print('VALUE',self.value,'OPTION',self.options)
        #
        # if self.value:
        #
        #     if self.options=='ei_number':
        #
        #         sqlite_query=f"""SELECT * FROM clients where cast(ei_number as text)={self.value};"""
        #         #sqlite_out=f"""DELETE FROM clients WHERE cast(ei_number as text)={self.choice}"""
        #     elif options=='oid':
        #         sqlite_query=f"""SELECT * FROM clients where oid={value};"""
        #
        #     c.execute(sqlite_query)
        # else:
        #     print('NO VALUE?')
        #
        #
        #
        #
        #
        #
        #
        #
        # print('GOT IT',self.options)
        #
        # def edit_kid():
        #
        #     #create a database or connect to one
        #     conn=sqlite3.connect('./database/ot_clients.db')
        #     #create a cursor
        #     c=conn.cursor()
        #     #Insert Into table
        #
        #     if self.options=='ei_number':
        #
        #         sqlite_query=f"""SELECT * FROM clients where cast(ei_number as text)={self.value};"""
        #         #sqlite_out=f"""DELETE FROM clients WHERE cast(ei_number as text)={self.value}"""
        #     elif self.options=='oid':
        #         sqlite_query=f"""SELECT * FROM clients where oid={self.value};"""
        #
        #     else:
        #         print('No correct value')
        #
        #     if sqlite_query:
        #
        #         c.execute(sqlite_query)
        #         record=c.fetchall()[0]
        #
        # label_0 = tk.Label(self, text="Editing a record",width=20,font=("bold", 22)).grid(row=0,columnspan=5,padx=10,pady=20)
        # labels=['First Name','Last Name','Middle Name','EI number','DOB mm/dd/yy','address',
        #         'Apt','city',"zip code",'Parent','Agency','email']
        #
        # self.first_name,self.last_name,self.middle_name,self.ei_number=tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()
        # self.address,self.apt,self.city,self.zip_code,self.parent,self.agency=tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()
        # self.dob, self.email=tk.StringVar(),tk.StringVar()
        #
        # entries=[self.first_name,self.last_name,self.middle_name,self.ei_number,self.dob,
        #         self.address,self.apt,self.city,self.zip_code,self.parent,self.agency,self.email]
        # #self.first_name.set(0,record[8])
        #
        # for n in range(len(labels)):
        #     if labels[n]!='DOB mm/dd/yy':
        #         my_label=tk.Label(self,text=labels[n],width=20,font=("bold", 16)).grid(row=n+1,column=0)
        #         tk.Entry(self,width=25,textvariable=entries[n]).grid(row=n+1,column=1)
        #     else:
        #         my_label=tk.Label(self,text=labels[n],width=20,font=("bold", 16)).grid(row=n+1,column=0)
        #         DateEntry(self,width=25,locale='en_US', date_pattern='mm/dd/y',textvariable=entries[n]).grid(row=n+1,column=1)
        #
        #
        #
        # tk.Button(self,text='Back to Home',command=\
        #                    lambda: controller.show_frame(StartPage)).grid(row=len(labels)+1,columnspan=2)
        # tk.Button(self, text='Update Record',width=10,bg='brown',
        #         fg='black',font=("bold",16),
        #         command=edit_kid).grid(row=len(labels)+2,columnspan=3)



app = MRWapp()
app.geometry('500x500')
app.title('MRW Application')
app.iconbitmap('logo.ico')
app.mainloop()
