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
import ids_and_more as im

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
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.OPTIONS=['ei_number','oid']
        self.shared_data = {
            'options': tk.StringVar(self,self.OPTIONS[0]),
            "choice": tk.StringVar()
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
        label = tk.Label(self, text='Choose Activity', font = LARGE_FONT).grid(row=0,columnspan=3,pady=10,padx=10)

        button1 = tk.Button(self, text ='Manage Children', font=("bold", 16),command= lambda:\
                            controller.show_frame(ManageRecords)).grid(row=2,column=2)

        button2 = tk.Button(self, text ='Sensory Profile', font=("bold", 16),command= lambda:\
                            controller.show_frame(SensoryProfile)).grid(row=3,column=2)

        button3 = tk.Button(self, text ='Invoices', font=("bold", 16),command= lambda:\
                            controller.show_frame(Invoices)).grid(row=4,column=2)




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

            if self.variable.get()=='ei_number':

                sqlite_query=f"""SELECT cast(oid as text),cast(ei_number as text),first_name,last_name FROM clients where cast(ei_number as text)={self.choice.get()};"""
                sqlite_out=f"""DELETE FROM clients WHERE cast(ei_number as text)={self.choice}"""
            elif self.variable.get()=='oid':

                sqlite_query=f"""SELECT cast(oid as text), first_name, last_name FROM clients where oid={self.choice.get()};"""
                sqlite_out=f"""DELETE FROM clients WHERE oid={self.choice.get()}"""
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


        label_0 = tk.Label(self, text="Deleting a record",width=20,font=("bold", 22)).grid(row=0,columnspan=5,padx=10,pady=20)

        OPTIONS=['ei_number','oid']
        self.last_name=tk.StringVar()
        #self.variable=tk.StringVar(self,OPTIONS[0])

        #entries=[self.last_name,self.choice]


        tk.Label(self,text='Last Name',width=20,font=("bold", 16)).grid(row=1,column=0)
        tk.Label(self,text='Choose filter',width=20,font=("bold", 16)).grid(row=2,column=0)
        tk.OptionMenu(self,self.controller.shared_data["options"],*self.controller.OPTIONS).grid(row=2,column=1)
        tk.Entry(self,width=15,textvariable=self.last_name).grid(row=1,column=1)
        tk.Entry(self,width=6,textvariable=self.controller.shared_data["choice"]).grid(row=2,column=2)
        #tk.OptionMenu(self,variable, *OPTIONS,width=20,font=("bold", 16)).grid(row=3,column=1)


        tk.Button(self,text='Manage Records',command=\
                           lambda: controller.show_frame(ManageRecords)).grid(row=5,columnspan=2)
        tk.Button(self,text='Delete!!!',command=delete_kid).grid(row=6,columnspan=3)
        tk.Button(self,text='Edit Child',command=\
                           lambda: controller.show_frame(EditRecord)).grid(row=7,columnspan=3)
        tk.Button(self,text='Back Home',command=\
                           lambda: controller.show_frame(StartPage)).grid(row=8,columnspan=3)

class EditRecord(tk.Frame): ###Consent and Delay Forms



    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)  ##parent refers to our main class MRWapp

        self.controller = controller
        options = self.controller.shared_data["options"].get()
        choice=self.controller.shared_data["choice"].get()
        #create a database or connect to one
        conn=sqlite3.connect('./database/ot_clients.db')
        #create a cursor
        c=conn.cursor()
        #Insert Into table
        print('CHOICE',choice,'OPTION',options)

        if choice:

            if options=='ei_number':

                sqlite_query=f"""SELECT * FROM clients where cast(ei_number as text)={choice};"""
                #sqlite_out=f"""DELETE FROM clients WHERE cast(ei_number as text)={self.choice}"""
            elif options=='oid':
                sqlite_query=f"""SELECT * FROM clients where oid={choice};"""

            c.execute(sqlite_query)

            for record in c.fetcall():
                print(record)



        print('GOT IT',options)

        def edit_kid():

            #create a database or connect to one
            conn=sqlite3.connect('./database/ot_clients.db')
            #create a cursor
            c=conn.cursor()
            #Insert Into table

            if options=='ei_number':

                sqlite_query=f"""SELECT * FROM clients where cast(ei_number as text)={choice};"""
                #sqlite_out=f"""DELETE FROM clients WHERE cast(ei_number as text)={self.choice}"""
            elif options=='oid':
                sqlite_query=f"""SELECT * FROM clients where oid={choice};"""

            c.execute(sqlite_query)

            pass

        label_0 = tk.Label(self, text="Editing a record",width=20,font=("bold", 22)).grid(row=0,columnspan=5,padx=10,pady=20)
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
        tk.Button(self, text='Update Record',width=10,bg='brown',
                fg='black',font=("bold",16),
                command=edit_kid).grid(row=len(labels)+2,columnspan=3)



app = MRWapp()
app.title('MRW Application')
app.geometry('500x500')
app.iconbitmap('logo.ico')
app.mainloop()
