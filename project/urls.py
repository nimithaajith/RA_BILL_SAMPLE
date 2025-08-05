from django.urls import path,include
from . views import *
app_name='project'
urlpatterns = [
    path('',dashboard,name='Dashboard'),
    path('manage',manage_project,name='ManageProject'),    
    path('edit',edit_project,name='EditProject'),   
    path('change_password',change_password,name='ChangePassword'),
    path('ajax_get_headings',ajax_get_headings,name='AjaxGetHeadings'),
    path('upload-status',get_upload_status, name='GetUploadStatus'),
    path('get_billupload_status',get_billupload_status, name='GetBillUploadStatus'),

    path('search_BoQ/<int:page>',search_boq_item,name='SearchItem'), 
    path('bill_of_quantities/<int:page>',manage_bill_of_quantities,name='ManageBOQ'),
    path('confirm_delete/<int:id>',confirm_delete_boq,name='ConfirmRemoveBOQ'),
    path('bill_of_quantities/delete',delete_bill_of_quantities,name='RemoveBOQ'),
    path('manage_item/<int:itemid>',manage_boq_item,name='ManageItem'), 
    path('remove_item/<int:itemid>',remove_boq_item,name='DeleteItem'), 

    path('boq_approvals',view_boq_approvals,name='ViewBoqApprovals'),
    path('remove_boq_update/<int:id>',remove_boq_update,name='RemoveBoqItemUpdate'),

    path('get_owners',ajax_get_owners,name='AjaxGetOwners'),
    path('get_companies',ajax_get_companies,name='AjaxGetCompanies'),
    path('get_consultants',ajax_get_consultants,name='AjaxGetConsultants'),

    path('add_consultant',add_consultant,name='AddConsultant'), 
    path('add_company',add_company,name='AddCompany'), 
    path('add_owner',add_owner,name='AddOwner'), 
    
    path('owner_comments/<int:measureid>',view_owner_comments,name='ViewOwnerComments'), 
    path('measurements/<int:itemid>/<int:page>',manage_measurements,name='Measurements'),
    path('edit_measurement/<int:measurementid>',edit_measurement,name='EditMeasurement'),
    path('remove_measurement/<int:measurementid>',remove_measurement,name='DeleteMeasurement'),
    path('workorder_boq/',upload_workorder_boq,name='UpLoadWOBOQ'),     
    path('bills/',create_bill,name='CreateBill'),
    path('create_new_bill/',create_new_bill,name='CreateNewBill'), 
    path('current_bill/<int:page>',current_bill,name='CurrentBill'), 
    path('save_current_bill',save_current_bill,name='SaveCurrentBill'),

    path('previous_bills',previous_bills,name='PreviousBills'), 
    path('previous_bills/<int:billid>/<int:page>',previous_bill,name='PreviousBill'), 
    path('previous_bills/measurements/<int:billid>/<int:itemid>/<int:page>',previous_bill_measurements,name='PreviousMeasurements'),
    path('edit_measurement/<int:measurementid>',edit_measurement,name='EditMeasurement'),
    path('remove_previous_measurement/<int:billid>/<int:measurementid>',remove_prev_measurement,name='DeletePreviousMeasurement'),
    path('search_item/<int:billid>/<int:page>',search_bill_item,name='SearchBillItem'), 
    path('share_to_consultant/<int:billid>',share_to_consultant,name='ShareToConsultant'),

    

    path('view_abstract/<int:billid>/<int:page>',viewAbstract,name='ViewAbstract'),
    path('generate_documents',generate_documents,name='Documents'),
    path('measurement_book/<int:billid>',downloadMBook,name='DownloadMBook'),
    
    path('logout_project/',userlogout,name='LogOutUser'),  
]


