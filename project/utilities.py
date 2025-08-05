from accounts.models import *
from django.db import transaction,models
from django.core.paginator import Paginator
from django.conf import settings
from openpyxl.drawing.image import Image
import pandas as pd
from celery import shared_task
from decimal import Decimal
import os
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.timezone import localtime
from pytz import timezone
from django.utils.timezone import now



def get_time_in_ist(value):     
    if value is None:
        return '' 
    try:
        ist = timezone('Asia/Kolkata')
        return localtime(value, ist).strftime('%Y-%m-%d %H:%M:%S')  
    except:
        return value 

@shared_task
def approval_email_notification(context,recipient_list,from_email=None):    
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    html_content = render_to_string('email_templates/bill_approved.html', context)
    try:
        subject = "Bill approved !"
        #from_email = "your-email@example.com"
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=recipient_list,
        )
        email.content_subtype = "html" 
        email.send(fail_silently=False)  
        print("=====CELERY approval EMAIL TO USER==============")      
    except Exception as e:        
        print(f"Error sending owner email: {e}")
        print("=====CELERY FAILED TO SENT approval EMAIL==============") 

@shared_task
def item_approval_email(context,recipient_list,cc_list,from_email=None):    
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    html_content = render_to_string('email_templates/item_approval.html', context)
    try:
        subject = "Approval Pending for Work order BoQ modification !"
        #from_email = "your-email@example.com"
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=recipient_list,
             cc=cc_list,  
        )
        email.content_subtype = "html" 
        email.send(fail_silently=False)  
        print("=====CELERY item approval EMAIL TO consultant and owner==============")      
    except Exception as e:        
        print(f"Error sending owner email: {e}")
        print("=====CELERY FAILED TO SENT item approval EMAIL==============") 

@shared_task
def send_email_notification(context,recipient_list,from_email=None):    
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    html_content = render_to_string('email_templates/bill_shared.html', context)
    try:
        subject = "Bill shared for approval !"
        #from_email = "your-email@example.com"
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=recipient_list,
        )
        email.content_subtype = "html" 
        email.send(fail_silently=False)  
        print("=====CELERY SENT EMAIL TO USER==============")      
    except Exception as e:        
        print(f"Error sending owner email: {e}")
        print("=====CELERY FAILED TO SENT EMAIL==============") 

@shared_task
def send_user_email(context,usertype,recipient_list,from_email=None):    
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    if usertype == 'owner':
        html_content = render_to_string('email_templates/owner_email.html', context)
    if usertype == 'consultant':
        html_content = render_to_string('email_templates/consultant_email.html', context)
    if usertype == 'project':
        html_content = render_to_string('email_templates/contractor_email.html', context)
    if usertype == 'company':
        html_content = render_to_string('email_templates/company_email.html', context)
    try:
        subject = "Welcome to XXXXXXX Solutions !"
        #from_email = "your-email@example.com"
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=recipient_list,
        )
        email.content_subtype = "html" 
        email.send(fail_silently=False)  
        print("=====CELERY SENT EMAIL TO USER==============")      
    except Exception as e:        
        print(f"Error sending owner email: {e}")
        print("=====CELERY FAILED TO SENT EMAIL==============") 
        



def find_heading_row(file_io,sno_heading,desc_heading,qty_heading,unit_heading):
    temp_df = pd.read_excel(file_io, nrows=20, header=None)  
    for i, row in temp_df.iterrows():
        if sno_heading in row.values or desc_heading in row.values or qty_heading in row.values or unit_heading in row.values : 
            # print('>>>>heading found<<<') 
            # print(row) 
            return i
    return 0

def get_username_password(name):
    new_name_str=name.replace(" ","").upper()
    username=new_name_str[:5]+str(randint(1000,9999))
    print("username = ",username)
    password='M@Ze20RU##Er25'
    return username,password



def CommitToDatabase(df,currentuser):
    projs=Project.objects.filter(user__id=currentuser)
    if projs:
        project=projs[0]
        try:
            itemobjs = [
                WOBOQItem(
                    project=project,
                    serial_no=row['Serial Number'] ,
                    description=row['Item Description'],
                    rate=row['Rate'] ,
                    quantity=row['Quantity'] ,
                    unit=row['Units'] ,
                    amount=row['Amount'],
                    subheading=row['subheading'],
                    work_order_date=row['work_order_date'],
                    heading=row['heading']
                )                
                for _, row in df.iterrows()
            ]
            
            with transaction.atomic():
                WOBOQItem.objects.bulk_create(itemobjs)   
            print("=========SAVED ALL RECORDS TO DB==========")         
            
        except Exception as e:
            print('exception during creation of bulk boq',e)
          


def get_boq_subheadings(page_obj):
    subheadings=[]
    try:
        for rec in page_obj:
            if rec.subheading is not None and not rec.extra_item and rec.subheading not in subheadings:
                subheadings.append(rec.subheading)
    except Exception as e:
        print('exception during get_boq_subheading',e)
            
    return(subheadings)

def get_boq_extra_subheadings(page_obj):
    # recs=WOBOQItem.objects.filter(project=project,extra_item=True).distinct('subheading')
    extra_subheadings=[]
    try:
        
        for rec in page_obj:
            if rec.subheading is not None and rec.extra_item and rec.subheading not in extra_subheadings:
                extra_subheadings.append(rec.subheading)
        
    except Exception as e:
        print('exception during get_boq_extra_subheadings',e)
    return(extra_subheadings)


def get_boq(project,page):
    # subheading=None
    # extra_subheadings=None
    # subheading_list=None
    
    # result={}
    page_obj=None
    try:
        allrecs=WOBOQItem.objects.filter(project=project).order_by('id')
        allrecs_paginator=Paginator(allrecs,100) 
        page_obj=allrecs_paginator.get_page(page)        
    except Exception as e:
        print('exception during get_boq in utilities',e)
    return page_obj   

def save_logo(logo_file,username):
    path=None
    try:
        file_name = username+'.png'    
        print("image file name>>>",file_name)    
        file_path = f'{settings.MEDIA_ROOT}/logos/{file_name}' 
        print('filepath inside save logo=',file_path)  
        path=f'logos/{file_name}'
        with open(file_path, 'wb+') as destination:
            for chunk in logo_file.chunks():
                destination.write(chunk)
    except Exception as e:
        print('exception inside utilities->savelogo,',e)    
    return path

from accounts.models import Bill,Measurement
from django.db.models import F,Sum,functions,ExpressionWrapper,DecimalField
def get_grand_total(bill):
    try:
        woboqitem_totals=Measurement.objects.filter(bill=bill).values('woboqitem__id','woboqitem__rate')\
                    .annotate(total_qty=Sum('quantity'))\
                    .annotate(amount=functions.Round(ExpressionWrapper(F('total_qty')*F('woboqitem__rate'),output_field=DecimalField(max_digits=20,decimal_places=2)),precision=2))
        grand_total=woboqitem_totals.aggregate(gtotal=Sum('amount'))
        if grand_total['gtotal']:
            return Decimal(grand_total['gtotal'])
    
    except Exception as e:
        print('exception during get_grand_total in utilities',e)
    return Decimal(0.0)


def get_taxable_value(total_bill_amount,total_gst,gst_inclusive):
    if gst_inclusive:
        taxable_amount=total_bill_amount/(1+(total_gst/100))
        return taxable_amount,total_bill_amount
    else:
        invoice_amt=total_bill_amount+(total_bill_amount*(total_gst/100))
        return total_bill_amount,invoice_amt
    

def check_sequence(index,row):
    expected_sequence = [1, 2, 3, 4, 5, 6]    
    if not row.iloc[:6].tolist() == expected_sequence:
        return False    
    return True


def is_subheading(row):
    return pd.notna(row['Item Description']) and pd.isna(row['Rate']) and pd.isna(row['Quantity']) and (pd.isna(row['Amount'])or row['Amount']==0)


def is_itemrow(row):
    return pd.notna(row['Item Description']) and pd.notna(row['Rate']) and pd.notna(row['Quantity']) and pd.notna(row['Amount']) and pd.notna(row['Units'])


def filter_headings(df):
    subheading_list = [] 
    filtered_headings=[] 
    try: 
        i = 0
        while i < len(df):
            if is_subheading(df.iloc[i]):
                subheading_count = 1 
                subheading_list = [] 
                row=df.iloc[i]
                if pd.isna(row['Serial Number']):
                    curhead = '#'+'&&&'+str(row['Item Description']).strip()
                else:
                    curhead = str(row['Serial Number']).strip()+'&&&'+str(row['Item Description']).strip()                    
                subheading_list.append(curhead)
                j = i + 1
                while j < len(df) and is_subheading(df.iloc[j]):
                    subheading_count += 1
                    row=df.iloc[j]
                    if pd.isna(row['Serial Number']):
                        curhead = '#'+'&&&'+str(row['Item Description']).strip()
                    else:
                        curhead = str(row['Serial Number']).strip()+'&&&'+str(row['Item Description']).strip()                    
                    subheading_list.append(curhead)
                    j += 1
                    curhead=''
                if is_itemrow(df.iloc[j]) and subheading_count>1:
                    last_subhead=subheading_list.pop()
                    # print(last_subhead," -removed from headings")
                    subheading_list.append(j)
                    filtered_headings.append(subheading_list)            

                i = j+1 
            else:
                i += 1
    except Exception as e:
        print('exception during filter_headings in utilities',e)
    # print(">>>>>>>filtered headings<<<<<<<<<<<<<<<<<<<<")
    # print(filtered_headings)
    return filtered_headings

import io
@shared_task
def process_boq_excel(arg_dict):
    status='failed'
    user=arg_dict['userid']
    file_content=arg_dict['file_content']
    file_io = io.BytesIO(file_content)
    sno_heading=arg_dict['sno_heading']
    desc_heading=arg_dict['desc_heading']
    qty_heading=arg_dict['qty_heading']
    unit_heading=arg_dict['unit_heading']
    rate_heading=arg_dict['rate_heading']
    amt_heading=arg_dict['amt_heading']
    dateofentry=arg_dict['dateofentry']
    try:
        print("===============================================")
        print("CELERY STARTED THE TASK -process_boq_excel()")
        print("===============================================")
        columns_to_extract = [sno_heading, desc_heading, qty_heading,unit_heading,rate_heading,amt_heading]
        headingrow=find_heading_row(file_io,sno_heading,desc_heading,qty_heading,unit_heading)
        
        print("Extracting Data Frame...........") 
        
        df = pd.read_excel(file_io,skiprows=headingrow,usecols=columns_to_extract, header=0)
        df[sno_heading] = df[sno_heading].apply(lambda x: "{:.15g}".format(x) if isinstance(x, float) else str(x))
        column_mapping = {
            sno_heading: 'Serial Number',
            desc_heading: 'Item Description',
            qty_heading: 'Quantity', 
            unit_heading: 'Units',
            rate_heading: 'Rate',
            amt_heading: 'Amount'
            
        }
        df = df.rename(columns=column_mapping)
        
        df['subheading'] = None
        df['heading'] = True
        df['work_order_date'] = dateofentry
        cur_sub_head=None
        for index, row in df.iterrows():
            if check_sequence(index,row):
                df = df.drop([index])  
                continue 
            if sno_heading in row.values or desc_heading in row.values or qty_heading in row.values or unit_heading in row.values : 
                df = df.drop([index])                
                continue 
            if row[['Serial Number', 'Item Description', 'Quantity', 'Units', 'Rate']].isna().all():
                # print("blank row passed>>>>>",index)
                df = df.drop([index])  
                continue 
            if pd.notna(row['Amount']) and pd.notna(row['Item Description']) and row[['Serial Number','Quantity', 'Units', 'Rate']].isna().all():
                                 
                df = df.drop([index])  
                continue
        df.reset_index(drop=True, inplace=True)
        for index, row in df.iterrows():
            # print(row)            
            
            if pd.notna(row['Item Description']) and pd.isna(row['Rate']) and pd.isna(row['Quantity']) and (pd.isna(row['Amount'])or row['Amount']==0):
                
                if pd.isna(row['Serial Number']):
                    cur_sub_head = '#'+'&&&'+str(row['Item Description']).strip()
                else:
                    cur_sub_head = str(row['Serial Number']).strip()+'&&&'+str(row['Item Description']).strip()
                #print(index,"subheading changed to",cur_sub_head)
                #df = df.drop([index]) 
                df.at[index, 'subheading'] = None
                df.at[index, 'Units'] = None
                df.at[index, 'Quantity'] = float(0)
                df.at[index, 'Rate'] = float(0)
                df.at[index, 'Amount'] = float(0)
                if pd.isna(row['Serial Number']):
                    df.at[index, 'Serial Number'] = '#'                             
                continue  
            
            
            if pd.notna(row['Item Description']) and pd.notna(row['Rate']) and pd.notna(row['Quantity']) and pd.notna(row['Amount']) and pd.notna(row['Units']):
                df.loc[index, 'subheading'] = cur_sub_head
                # print("item row >>>>>",index)
                if row['Rate'] == 0 or row['Rate'] == 0.00:
                    df.loc[index, 'Rate']  = 1.00
                if row['Quantity'] == 0 or row['Quantity'] == 0.00:
                    df.loc[index, 'Quantity']  = 1.00 
                
                if row['Rate'] is not None:
                    try:
                        temp_rate=row['Rate']
                        df.loc[index, 'Rate']  = float(temp_rate)
                    except:
                        df.loc[index, 'Rate']  = 1.00
                else:
                    df.loc[index, 'Rate']  = 1.00
                if row['Quantity'] is not None:
                    try:
                        temp_qty=row['Quantity']
                        df.loc[index, 'Quantity']  = float(temp_qty)
                    except:
                        df.loc[index, 'Quantity']  = 1.00
                else:
                    df.loc[index, 'Quantity']  = 1.00

                if row['Amount'] is not None:
                    try:
                        temp_amt=row['Amount']
                        df.loc[index, 'Amount']  = float(temp_amt)
                    except:
                        df.loc[index, 'Amount']  = 1.00
                else:
                    df.loc[index, 'Amount']  = 1.00
                df.loc[index, 'heading']  = False                
                continue
            if pd.notna(row["Item Description"]):                
                if any(pd.isna(row[col]) for col in ["Quantity", "Units", "Rate", "Amount"]):
                    # print("subheading,row dropped>>>>>",index)
                    if pd.isna(row['Serial Number']):
                        cur_sub_head = '#'+'&&&'+str(row['Item Description']).strip()
                    else:
                        cur_sub_head = str(row['Serial Number']).strip()+'&&&'+str(row['Item Description']).strip()
                    # print(index,"2.subheading changed to",cur_sub_head)
                    #df = df.drop([index]) 
                    df.at[index, 'subheading'] = None
                    df.at[index, 'Units'] = None
                    df.at[index, 'Quantity'] = float(0)
                    df.at[index, 'Rate'] = float(0)
                    df.at[index, 'Amount'] = float(0)
                    if pd.isna(row['Serial Number']):
                        df.at[index, 'Serial Number'] = '#'                             
                    continue  
            print("no match>>>>>",row)
            df = df.drop([index])          
        # print("**********************************")                           
        df.reset_index(drop=True, inplace=True) 
        df = df.where(pd.notnull(df), None)
        df = df.map(lambda x: None if pd.isna(x) else x)    
        print("Extracted Data Frame Successfully.......")  
         
        projs=Project.objects.filter(user__id=user)
        if projs:
            project=projs[0]
        
            itemobjs = [
                WOBOQItem(
                    project=project,
                    serial_no=row['Serial Number'] ,
                    description=row['Item Description'],
                    rate=row['Rate'] ,
                    quantity=row['Quantity'] ,
                    unit=row['Units'] ,
                    amount=row['Amount'],
                    subheading=row['subheading'],
                    work_order_date=row['work_order_date'],
                    heading=row['heading']
                )                
                for _, row in df.iterrows()
            ]
            
            print("SAVING RECORDS TO DB............")  
            with transaction.atomic():
                WOBOQItem.objects.bulk_create(itemobjs)   
            print("SAVED ALL RECORDS TO DB..........")                  
    
    except Exception as e:        
        print("error inside task=",e)
        
    print("===============================================")
    print("CELERY COMPLETED THE TASK -process_boq_excel()")
    print("===============================================")


def is_not_first_bill(project):
    return Bill.objects.filter(project=project).exists()

def find_bill_heading_row(file_io,sno_heading,desc_heading,qty_heading):
    temp_df = pd.read_excel(file_io, nrows=20, header=None)  
    for i, row in temp_df.iterrows():
        if sno_heading in row.values or desc_heading in row.values or qty_heading in row.values: 
            # print('>>>>heading found<<<') 
            # print(row) 
            return i
    return 0

@shared_task
def process_bill_excel(arg_dict):
    status='failed'
    projectid=arg_dict['projectid']
    file_content=arg_dict['file_content']
    file_io = io.BytesIO(file_content)
    desc_heading=arg_dict['desc_heading']
    qty_heading=arg_dict['qty_heading']
    sno_heading=arg_dict['sno_heading']
    currentbillno=arg_dict['currentbillno']
    
    try:
        print("===============================================")
        print("CELERY STARTED THE TASK -process_bill_excel()")
        print("===============================================")        
        columns_to_extract = [sno_heading,desc_heading, qty_heading]
        headingrow=find_bill_heading_row(file_io,sno_heading,desc_heading,qty_heading)
        
        print("Extracting Data Frame...........") 
        
        df = pd.read_excel(file_io,skiprows=headingrow,usecols=columns_to_extract, header=0)
        df[sno_heading] = df[sno_heading].apply(lambda x: "{:.15g}".format(x) if isinstance(x, float) else str(x))
        column_mapping = {
            sno_heading: 'Serial Number',
            desc_heading: 'Item Description',
            qty_heading: 'Quantity', 
                       
        }
        df = df.rename(columns=column_mapping)   
        print("Extracting Data Frame..519......")       
        
        for index, row in df.iterrows():
            if check_sequence(index,row):
                df = df.drop([index])  
                continue 
            if sno_heading in row.values or desc_heading in row.values or qty_heading in row.values : 
                df = df.drop([index])                
                continue 
            if row[['Serial Number', 'Item Description', 'Quantity']].isna().all():
                # print("blank row passed>>>>>",index)
                df = df.drop([index])  
                continue 
            if pd.notna(row['Item Description']) and row[['Serial Number','Quantity']].isna().all():
                                 
                df = df.drop([index])  
                continue
        df.reset_index(drop=True, inplace=True)
        print("Extracting Data Frame........537...") 
        for index, row in df.iterrows():           
            if pd.notna(row['Item Description']) and pd.notna(row['Quantity']) :
                continue            
            df = df.drop([index])          
        # print("**********************************")                           
        df.reset_index(drop=True, inplace=True) 
        df = df.where(pd.notnull(df), None)
        df = df.map(lambda x: None if pd.isna(x) else x) 
        print("Extracting Data Frame...546........")    
        projs=Project.objects.filter(id=projectid)
        if projs:
            project=projs[0]
            current_datetime = now()           
            formatted_date = current_datetime.strftime('%Y-%m-%d')
            print('currentbillno',type(currentbillno))
            cumulativebill=Bill(
                bill_name=f'cumulative-bill-from-1to{int(currentbillno)-1}',
                bill_number=1,
                project=project,
                submitted=True,
                bill_date=formatted_date,
                shared_to_consultant=current_datetime,
                shared_to_owner=current_datetime,
                consultant_approved=current_datetime,
                owner_approved=current_datetime,    
                other_details='This is auto generated cumulative bill'

            )
            
            print("Extracting Data Frame.....566......") 
            boqitems=WOBOQItem.objects.filter(project=project,heading=False)
            itemobjs = []
            for index, row in df.iterrows():
                print('inside for')
                serialno = row['Serial Number']
                quantity = row['Quantity']
                description=row['Item Description']


                print("Extracting Data Frame.........577..") 
                matchitems = boqitems.filter(serial_no=serialno, description=description)
                if matchitems:
                    item=matchitems[0]  
                    measure=None      
                    measure=Measurement(
                        woboqitem=item,
                        bill=cumulativebill ,
                        count=1,
                        length=1,
                        breadth=1,
                        height=1,
                        number=quantity,
                        quantity=quantity ,                        
                        entry_date=formatted_date,
                        consultant_approved=current_datetime,
                        owner_approved=current_datetime, 
                        other_details='Auto generated measurement'
                    ) 
                    itemobjs.append(measure)        
            
            print("SAVING RECORDS TO DB............")  
            with transaction.atomic():
                cumulativebill.save()
                Measurement.objects.bulk_create(itemobjs)   
            print("SAVED ALL RECORDS TO DB..........")                  
    
    except Exception as e:        
        print("error inside task=",e)
        
    print("===============================================")
    print("CELERY COMPLETED THE TASK -process_boq_excel()")
    print("===============================================")


