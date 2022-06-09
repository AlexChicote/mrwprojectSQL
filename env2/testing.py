#from google_sheets import sheet
import pickle
import pandas as pd

import sqlite3
import functions_sql as fsql

#df=fsql.sqltable_to_dataframe('clients')
#fsql.changing_column_dtype('clients','ei_number','string')
#fsql.dataframe_to_sqltable('/Users/fcbnyc/mystuff/mrwprojectSQL/env2/text_files/dataframe_in_process.csv','children')
#fsql.get_tables_in_database(fsql.database)
#fsql.get_n_last_records_from_table('clients',5)
#fsql.change_datatype_column('clients','ei_number','text')
#fsql.get_records_with_filter('clients','first_name','Isona')
#fsql.drop_sql_table('clients')
#fsql.rename_table('children','clients')
#fsql.get_column_names_in_table('children')
#Connecting to sqlite
conn = sqlite3.connect('./database/ot_clients.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()
sqlite_query=f"""DELETE FROM clients where oid=58;"""

cursor.execute(sqlite_query)
cursor.execute("""SELECT oid,ei_number,last_name from clients""")
print(cursor.fetchall())

for record in cursor.fetchall():
    print('_'.join(record))
#commit changes
conn.commit()
#close connection
conn.close()



# SAMPLE_SPREADSHEET_ID='10CTuENnyMgjEgzDXSGR8jo-R19NslhSDIcdWGAL4d_k'
# SAMPLE_RANGE_NAME='Totals des de Nov. 07'
#
#
# result = sheet.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                 range=SAMPLE_RANGE_NAME).execute()
# profilers_data=result.get('values',[])
# #print(type(profilers_data))
# pickle.dump(profilers_data, open( "big_sheet.pkl", "wb" ))
#
# df=pd.read_csv('./text_files/dataframe_in_process.csv')
# for col in df:
#     if 'Unnamed' in col:
#         df=df.drop(col,axis=1)
#
# df['execution_date']=pd.to_datetime(df['execution_date'])
#
# #print(df.execution_date.dt.year.unique())"""
# profilers_df['Timestamp']=pd.to_datetime(profilers_df['Timestamp'])
# predata=profilers_df.sort_values('Timestamp').tail().reset_index(drop=True)
# llista=[]
# for idx, v in predata.iterrows():
#     child=[]
#     child.append(idx)
#     child.extend(v[:5].values)
#     llista.append(child)
