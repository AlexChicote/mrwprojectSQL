import tkinter as tk
import pickle
import tkinter.messagebox as tkmb
import datetime
"""import pdfrw
import fpdf
"""
import io
import shutil

import pandas as pd


from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from google_drive import service
import ids_and_more as im
import os

"""
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        if type(data_dict[key]) == bool:
                            if data_dict[key] == True:
                                annotation.update(pdfrw.PdfDict(
                                    AS=pdfrw.PdfName('Yes')))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=''))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

def fill_TelhealthEval_pdf_file(data,
                                template_output,
                                template_input=im.documents["TelehealthConsent"]):
  data['full_name']=data['name']+' '+data['middle_name']+' '+data['last_name']

  data_dict = {
      'Child|FormattedName': data.get('full_name', ''),
      'Child|CurrentProgramEnrollment*ProgramId': data.get('ei_number', ''),
      'Child|DateOfBirth*ToShortDateString': data.get('dob',''),
      'Child|Address1': data.get('address1', ''),
      'Child|Address2': data.get('address2', ''),
      'Child|Zip': data.get('zip', ''),
      'Child|City': data.get('city',''),
      'Assignment|Provider*FormattedTherapistName_FirstLast':im.ot_therapist,
      'Assignment|PatientOngoingService*TherapistTypeCode': 'OT evaluation',
      'Child|ServiceCoordinator*AgencyName': data.get('agency',''),
      'untitled18': 'OT evaluation',
      'untitled20': data.get('parent','')
  }
  return fill_pdf(template_input, template_output, data_dict)

def fill_EvalConsent_pdf_file(data,
                              template_output,
                                template_input=im.documents["EvalConsent"]):

    data_dict = {


        'Child|PatientLastName':data.get('last_name',''),
        'Child|PatientFirstName':data.get('name',''),
        'Child|PatientMiddleName': data.get('Child|MiddleName', ''),
        'Child|CurrentProgramEnrollment*ProgramId': data.get('ei_number',''),
        'Child|DateOfBirth*Month': data.get('dob', '').split('/')[0],
        'Child|DateOfBirth*Day': data.get('dob','').split('/')[1],
        'Child|DateOfBirth*Year':data.get('dob','').split('/')[2],
        'Evaluation Site|AgencyName': data.get('agency',''),
        'untitled8':data.get('today','')

    }
    return fill_pdf(template_input, template_output, data_dict)
"""

def diff_month(old_date, ara):
    correction=0
    if old_date.day>ara.day:
      correction=1
    return abs((old_date.year - ara.year) * 12 + old_date.month - ara.month+correction)


def create_folder(child_dict,month_age):

    new_folder=im.url_consents+child_dict['name']+'_'+child_dict['last_name']+'_'+str(month_age)+'m'
    try:
      os.makedirs(new_folder)
    except:
      print("Folder Already exists")
    return new_folder

def resetting_documents():
    if consent.get() ==1:
        documents_requested['EvalConsent']=True
    if telehealth.get()==1:
        documents_requested['TelehealthConsent']=True
    if delay.get()==1:
        documents_requested['DelayForm']=True

def creating_folder_gd(child_dict,month_age,service,parent=im.automation_folder):
    """Based on the name given it will create a folder in """
    file_metadata = {
        'name': child_dict['name']+'_'+child_dict['last_name']+'_'+str(month_age)+'m',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents':[parent]
    }
    query = f"""parents in '{file_metadata['parents'][0]}'
    and trashed = False
    and mimeType='application/vnd.google-apps.folder'"""
    llista =service.files().list(q =query,pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = llista.get('files', [])
    for f in range(0, len(items)):
        fname = items[f].get('name')
        if fname ==file_metadata['name']:
            new_id=items[f].get('id')
            return new_id
            break

    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    new_id=file.get('id')
    return new_id

def upload_files_gd(folder_id,from_folder=im.temp_consents_folder):

    for fitxer in os.listdir(from_folder):

        file_metadata = {'name': fitxer,
                        'parents': [folder_id]}
        media = MediaFileUpload(from_folder+'/'+fitxer, mimetype='application/pdf')
        file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        os.remove(from_folder+'/'+fitxer)
        print('File ID: %s' % file.get('id'))

def upload_invoices_gd(folder_id):

    for fitxer in os.listdir(im.temp_invoices_folder):
    #from getfilelistpy import getfilelist

        file_metadata = {'name': fitxer,
                        'parents': [folder_id]}
        media = MediaFileUpload(im.temp_invoices_folder+'/'+fitxer, mimetype='application/pdf')
        file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        os.remove(im.temp_invoices_folder+'/'+fitxer)
        print('File ID: %s' % file.get('id'))

def getting_data(service,file_id):
#file_id = '1JJIztrUTFoOL14x0UxASgbKRDf1h11Iiuc8qJ32PYro'
    request = service.files().export(fileId=file_id, mimeType='text/tab-separated-values')

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%" % int(status.progress() * 100))

    # The file has been downloaded into RAM, now save it in a file
    fh.seek(0)

    with open('profilers.txt', 'wb') as f:
        shutil.copyfileobj(fh, f)#, length=131072)
    file1 = open(im.profilers_file, 'r')
    Lines = file1.readlines()
    print(len(Lines))
    columns=Lines[0].split('\t')
    data=[line.split('\t') for line in Lines[1:]]
    profilers=pd.DataFrame(data, columns=columns)
    profilers['Timestamp']=pd.to_datetime(profilers['Timestamp'])
    predata=profilers.sort_values('Timestamp',).tail().reset_index(drop=True)
    llista=[]
    for idx, v in predata.iterrows():
        child=[]
        child.append(str(idx))
        child.extend(v[:5].values)
        llista.append(child)
    return llista,predata

def getting_data_sensory_profile(service,SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME):

    result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
    profilers_data=result.get('values',[])
    columns=profilers_data[0]
    data=profilers_data[1:]
    profilers_df=pd.DataFrame(data,columns=columns)
    profilers_df['Timestamp']=pd.to_datetime(profilers_df['Timestamp'])
    predata=profilers_df.sort_values('Timestamp').tail().reset_index(drop=True)
    llista=[]
    for idx, v in predata.iterrows():
        child=[]
        child.append(idx)
        child.extend(v[:5].values)
        llista.append(child)
    return llista,predata


def getting_invoice(service,SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
    outcome=result.get('values',[])
    df=pd.DataFrame(outcome[4:],)
    columnes=outcome[2][2:11]
    df=df.iloc[:,2:11]
    df.columns=columnes
    df=df[df.Tipus.isin(['Avaluacio', 'On-going'])]
    new_df=pd.DataFrame()
    for year in range(22,26):
        new_df=pd.concat([new_df,df[df['Data Execucio'].str.endswith(str(year))]])

    return new_df.reset_index(drop=True)

def creating_invoice(outcome,Agency,Month, Year):

    def NumTomonth(shortMonth):
        return {
                1:'jan',
                2: 'feb',
                3:'mar',
                4:'apr',
                5:'may',
                6:'jun',
                7:'jul',
                8:'aug',
                9:'sep',
                10:'oct',
                11:'nov',
                12:'dec'
        }[shortMonth]
    month=NumTomonth(int(Month)).capitalize()



    Year=2000+int(Year)
    agency='EE' if Agency=='Early Sprouts' else 'OWL'
    ong_fee=61 if agency=='EE' else 59
    evals_fee=155 if agency=='EE' else 150
    outcome=outcome.rename(columns={'Data Execucio':'DOE'})
    outcome['DOE']=pd.to_datetime(outcome['DOE'],format='%m/%d/%y')
    outcome['day_of_month']=outcome['DOE'].dt.day
    df=outcome[(outcome['Agencia']==agency)&(outcome['DOE'].dt.month==int(Month))&(outcome['DOE'].dt.year==Year)]

    if 'On-going' in list(df.Tipus.unique()):
        ongoing=True
        ongoing_df=df[df.Tipus=='On-going']

        kids_df=pd.DataFrame(columns=[str(x) for x in range(1,32)])
        column_name_list=list(kids_df.columns)
        ongoing_kids=list(ongoing_df.Nom.unique())
        for kid in ongoing_kids:
            llista=list(ongoing_df[ongoing_df.Nom==kid]['day_of_month'])
            kids_df.loc[kid]=['X' if x in llista else ' ' for x in range(1,32)]
        TBS=len(ongoing_df)#Total Basic Sessions

    else:
        print('Not ongoing this month')
        ongoing=False
        TBS=0


    if 'Avaluacio' in list(df.Tipus.unique()):

        evals_df=df[df.Tipus=='Avaluacio']
        TEF=len(evals_df)
        evals=True
    else:
        print('No evals this month')
        evals=False



    pdf = fpdf.FPDF('L', 'mm', 'A4') #Landscape, measure in milimeters and format A4
    pdf.add_page()
    pdf.set_margins(3, 3, 3)
    epw = pdf.w - 2*pdf.l_margin
    pdf.rect(235.0, 20.0, 50.0,20.0,'D')#x, y, w,h
    pdf.set_font('Arial', 'B', 16) #Using Arial, Bold and size 16

    pdf.cell(0, 8, im.agency_address, border=0,ln=1,align='C')

    pdf.set_font('Arial', 'B', 14) #Using Arial, Bold and size 16
    pdf.cell(0,8,im.therapist_name,border=0,ln=0, align='L')
    pdf.set_font('Arial', 'I', 14)
    pdf.cell(-40)
    pdf.cell(30,12,'FOR OFFICIAL USE',border=0,ln=1,align='R')
    pdf.cell(230)
    pdf.cell(25,10,'TOTAL $',border=0,align='R',ln=1)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, month+' '+str(Year), 0,align='C',ln=1)
    pdf.ln(3)
    th = pdf.font_size
    count=0

    if ongoing:
        th = pdf.font_size
        count=0

        for num,kid in enumerate(ongoing_kids):
            if (num+1)%3!=0:
                pdf.cell(epw,8,f"Childs Name: {kid}       Discipline:  OT       #Basic: {TBS}      #Extended: {0}",ln=1,align='C')
                for header in column_name_list[:-1]:
                    pdf.cell(epw/32,th*1.5,header,1,0,'C')
                pdf.cell(epw/32,th*1.5,column_name_list[-1],1,1,'C')
                for col in pd.DataFrame(kids_df.loc[kid,:]).T.columns:
                    pdf.cell(epw/32,th*1.5,kids_df.loc[kid,col],1,0,'C')
                pdf.ln(3*th)
                count+=1
            else:
                pdf.add_page()
                count=0
                pdf.set_xy(10.0, 10.0)
                pdf.cell(epw,8,f"Childs Name: {kid}       Discipline:  OT        #Basic: {TBS}       #Extended: {0}",ln=1)
                for header in column_name_list[:-1]:
                    pdf.cell(epw/32,th*1.5,header,1,0,'C')
                pdf.cell(epw/32,th*1.5,column_name_list[-1],1,1,'C')
                for col in pd.DataFrame(kids_df.loc[kid,:]).T.columns:
                    pdf.cell(epw/32,th*1.5,kids_df.loc[kid,col],1,0,'C')
                pdf.ln(3*th)
                count+=1
        pdf.cell(0,10,f'Total Basic Sessions{TBS}@ ${ong_fee}= ${TBS*ong_fee}   Total Extended Sessions  {0} @${0}= ${0}    Total Evaluations Fee: {TEF*evals_fee}  Total Site Rep:{0}')

        pdf.ln(3*th)
    if evals:
        num=0
        for eva in  evals_df[['Nom','DOE']].iterrows():

            pdf.cell(epw,8,f"{num+1}) Childs Name:{eva[1].Nom}               DOE:{str(eva[1].DOE)[0:10]}          Fee:${evals_fee}",ln=1,align='L')
            num+=1


    pdf.output(im.temp_invoices_folder+'/Invoice'+agency+month+str(Year)+'.pdf')

def selecting_folder_in_gd(child_dict):

    month=child_dict['month_age']
    agency=child_dict['agency']
    if int(month)<13:
        return im.folders_info[agency]['0-12']
    elif int(month) <25:
        return im.folders_info[agency]['13-24']
    else:
        return im.folders_info[agency]['25-36']
