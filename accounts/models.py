from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.timezone import now
'''
super admin ->add and manage company
admin -> create login for projects of companies
company -> has many projects and can view staus of each project
project-> project owned by a comapny and does all project related actions such as billing
'''
class User(AbstractUser):
    
    user_types = [
        ('super_admin', 'super_admin'),
        ('admin', 'admin'),
        ('project'  , 'project'),
        ('company', 'company'),
        ('consultant', 'consultant'),
        ('owner', 'owner'),
    ]
    
    user_type = models.CharField(max_length=30,choices=user_types)    
    added_by = models.CharField(max_length=30,default='super_admin')
    # def __str__(self):
    #     return "username = {}, user_type ={}".format(self.username, self.user_type)

    class Meta:
        db_table = 'User'


class Company(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=200,null=True)
    company_address=models.CharField(max_length=500,null=True)
    company_email=models.EmailField(null=True)
    country_code=models.CharField(max_length=4,default='+91')
    company_phone=models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], help_text="Phone number without Country Code",null=True)
    # company_logo=models.CharField(max_length=500,null=True,blank=True)
    other_details=models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return "company_name = {}, companyuser ={}".format(self.company_name, self.user.username)

    class Meta:
        db_table = 'Company'


class Owner(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    owner_name=models.CharField(max_length=200,null=True,blank=True)
    owner_address=models.CharField(max_length=500,null=True,blank=True)
    owner_email=models.EmailField(null=True,blank=True)
    country_code=models.CharField(max_length=4,default='+91')
    owner_phone=models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], help_text="Phone number without Country Code",null=True,blank=True)
    # consultant_logo=models.CharField(max_length=500,null=True,blank=True)
    other_details=models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return "owner = {}, owneruser ={}".format(self.owner_name, self.user.username)

    class Meta:
        db_table = 'Owner'

class Consultant(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    owner=models.ForeignKey(Owner,on_delete=models.CASCADE,null=True,blank=True)
    consultant_name=models.CharField(max_length=200,null=True,blank=True)
    consultant_address=models.CharField(max_length=500,null=True,blank=True)
    consultant_email=models.EmailField(null=True,blank=True) 
    country_code=models.CharField(max_length=4,default='+91')
    consultant_phone=models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], help_text="Phone number without Country Code",null=True,blank=True)
    # consultant_logo=models.CharField(max_length=500,null=True,blank=True)
    other_details=models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return "Consultant = {}, consultantuser ={}".format(self.consultant_name, self.user.username)

    class Meta:
        db_table = 'Consultant'  




class Project(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    project_name=models.CharField(max_length=500,null=True,blank=True)    
    owner=models.ForeignKey(Owner,on_delete=models.CASCADE,null=True)
    consultant=models.ForeignKey(Consultant,on_delete=models.CASCADE,null=True)
    contractor=models.CharField(max_length=500,default='self',null=True,blank=True)
    location=models.CharField(max_length=500,null=True,blank=True)
    work_order_no=models.CharField(max_length=150,null=True,blank=True)
    other_details=models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return "project = {}, projectuser= {}, company ={}".format(self.project_name,self.user.username, self.company.company_name)

    class Meta:
        db_table = 'Project'


class Bill(models.Model):
    bill_name=models.CharField(max_length=100,default='1')
    bill_number=models.IntegerField(default=1)
    project=models.ForeignKey(Project, on_delete= models.CASCADE)
    submitted=models.BooleanField(default=False)
    bill_date=models.DateField()
    shared_to_consultant=models.DateTimeField(null=True,blank=True,default=None)
    shared_to_owner=models.DateTimeField(null=True,blank=True,default=None)
    consultant_approved=models.DateTimeField(null=True,blank=True,default=None)
    owner_approved=models.DateTimeField(null=True,blank=True,default=None)
    
    other_details=models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return "{}th bill of {} project Bill Name : {}".format(self.bill_number,self.project.project_name,self.bill_name)

    def clean(self):        
        existing_bills = Bill.objects.filter(project=self.project, bill_name=self.bill_name)
        if self.pk:
            existing_bills = existing_bills.exclude(pk=self.pk)
        if existing_bills.exists():
            raise ValidationError('A bill with this name already exists for the project.')

    class Meta:
        db_table = 'Bill'
        constraints = [
            models.UniqueConstraint(fields=['project', 'bill_name'], name='unique_project_bill')
        ]



class WOBOQItem(models.Model):
    project=models.ForeignKey(Project, on_delete= models.CASCADE)
    serial_no=models.CharField(max_length=100,null=True,default=None)# enters '##' when no serialno for row
    description=models.CharField(max_length=100000,null=True,blank=True)
    unit=models.CharField(max_length=50,null=True,blank=True)
    rate=models.DecimalField(max_digits=12,decimal_places=2,null=True,default=None)
    quantity=models.DecimalField(max_digits=15,decimal_places=2,null=True,default=None)
    amount=models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    heading=models.BooleanField(null=True,default=True) 
    subheading=models.CharField(max_length=10,null=True,blank=True) # serialno+'&&&'+subheading if subheading found above a row
    work_order_date=models.DateField()
    extra_item=models.BooleanField(default=False)#if item is added later as extra
    other_details=models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return "{},project={} ,{},{},{},{},{},{},{}".format(self.pk,self.project.project_name,self.serial_no,self.description,self.rate,self.unit,self.quantity,self.amount,self.subheading)
    
    class Meta:
        db_table = 'WOBOQItem'
        
class Measurement(models.Model):
    woboqitem=models.ForeignKey(WOBOQItem,on_delete=models.CASCADE)
    bill=models.ForeignKey(Bill,on_delete=models.CASCADE)
    m_description=models.CharField(max_length=500,null=True,blank=True)
    count=models.IntegerField(default=1,help_text="the number of items with this measurement")
    number=models.DecimalField(max_digits=10,decimal_places=3,null=True,default=1.000)
    length=models.DecimalField(max_digits=16,decimal_places=3,null=True,default=1.000)
    breadth=models.DecimalField(max_digits=16,decimal_places=3,default=1.000,null=True)
    height=models.DecimalField(max_digits=16,decimal_places=3,default=1.000,null=True)
    quantity=models.DecimalField(max_digits=16,decimal_places=3,default=0.000,null=True)
    entry_date=models.DateField() 
    consultant_approved=models.DateTimeField(null=True,blank=True,default=None)
    owner_approved=models.DateTimeField(null=True,blank=True,default=None)     
    other_details=models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return "{} : {}".format(self.woboqitem.description,self.quantity)
    
    class Meta:
        db_table = 'Measurement'

class Consultant_Comments(models.Model):
    measurement=models.ForeignKey(Measurement,on_delete=models.CASCADE)
    commented_on=models.DateTimeField(default=now) 
    comment=models.CharField(max_length=1000,null=True,blank=True)
    measurement_backup=models.CharField(max_length=500,null=True,blank=True)
    status=models.CharField(max_length=10,null=True,default='open') #open,closed
    read_by_project=models.BooleanField(null=True,default=False) 
    def __str__(self):
        return "{},{}".format(self.comment,self.measurement_backup)
    
    class Meta:
        db_table = 'Consultant_Comments'


class Owner_Comments(models.Model):
    measurement=models.ForeignKey(Measurement,on_delete=models.CASCADE)
    commented_on=models.DateTimeField(default=now)    
    comment=models.CharField(max_length=1000,null=True,blank=True)
    measurement_backup=models.CharField(max_length=500,null=True,blank=True)
    status=models.CharField(max_length=10,null=True,default='open') #open or closed, status by owner
    read_by_project=models.BooleanField(null=True,default=False) 
    read_by_consultant=models.BooleanField(null=True,default=False)
    consultant_status=models.CharField(max_length=10,null=True,default='open') #staus by consultant
    def __str__(self):
        return "{}".format(self.measurement_backup)
     
    class Meta:
        db_table = 'Owner_Comments' 

class COPMaster(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)     
    company_logo=models.CharField(max_length=500,null=True,blank=True)
    gst_no=models.CharField(max_length=50,null=True,blank=True)

    state=models.CharField(max_length=100,null=True,blank=True)
    bank=models.CharField(max_length=200,null=True,blank=True)
    branch=models.CharField(max_length=200,null=True,blank=True)
    ifsc=models.CharField(max_length=50,null=True,blank=True)
    acno=models.CharField(max_length=50,null=True,blank=True)

    receiver_name=models.CharField(max_length=200,null=True,blank=True)
    receiver_address=models.CharField(max_length=800,null=True,blank=True)
    receiver_gst_no=models.CharField(max_length=50,null=True,blank=True)
    receiver_state=models.CharField(max_length=100,null=True,blank=True)
    receiver_code=models.CharField(max_length=50,null=True,blank=True)
           
    order_acceptance_no=models.CharField(max_length=100,null=True,blank=True)
    terms_of_payment=models.CharField(max_length=250,null=True,blank=True)
    hsn_sa_code=models.CharField(max_length=50,null=True,blank=True)
    uom=models.CharField(max_length=50,null=True,blank=True) 
        
    def __str__(self):
        return "COPMaster for sender={} receiver= {}".format(self.project.company.company_name,self.receiver_name)
    
    class Meta:
        db_table = 'COPMaster'  


class COP(models.Model):
    copmaster=models.ForeignKey(COPMaster,on_delete=models.CASCADE) 
    bill=models.ForeignKey(Bill,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=50,null=True,blank=True)
    sgst=models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    cgst=models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    igst=models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    ugst=models.DecimalField(max_digits=5,decimal_places=2,default=0.00)

    supply_of_goods=models.BooleanField(default=False)
    supply_of_services=models.BooleanField(default=False)
    stock_transfer=models.BooleanField(default=False)
    debit_credit_notes=models.BooleanField(default=False)
    other_supplies=models.BooleanField(default=False)
    gst_inclusive=models.BooleanField(default=False)

    date_of_bill=models.DateField()

    def __str__(self):
        return "COP for bill={} ".format(self.bill.bill_name)
    
    class Meta:
        db_table = 'COP'  

class Pending_Item(models.Model):
    project=models.ForeignKey(Project, on_delete= models.CASCADE)
    serial_no=models.CharField(max_length=100,null=True,default=None)# enters '##' when no serialno for row
    description=models.CharField(max_length=100000,null=True,blank=True)
    unit=models.CharField(max_length=50,null=True,blank=True)
    rate=models.DecimalField(max_digits=12,decimal_places=2,null=True,default=None)
    quantity=models.DecimalField(max_digits=15,decimal_places=3,null=True,default=None)
    amount=models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    heading=models.BooleanField(null=True,default=True) 
    subheading=models.CharField(max_length=10,null=True,blank=True) 
    work_order_date=models.DateField()
    extra_item=models.BooleanField(default=False)#if item is added later as extra
    other_details=models.CharField(max_length=500,null=True,blank=True)
    consultant_approved=models.BooleanField(default=False)
    owner_approved=models.BooleanField(default=False)
    existing=models.BigIntegerField(default=0)
    
    class Meta:
        db_table = 'Pending_Item'
        
    

