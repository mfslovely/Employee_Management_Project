from django.db import models
from datetime import datetime
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone




class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name
    
class Designation(models.Model):
    title = models.CharField(max_length=100, unique=True)  
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions') 
    def __str__(self):
        return f"{self.title} ({self.department.name})"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    job_title = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    # New fields for account details
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=11, blank=True, null=True)

    # Address fields
    current_street = models.CharField(max_length=255, blank=True, null=True)
    current_city = models.CharField(max_length=100, blank=True, null=True)
    current_state = models.CharField(max_length=100, blank=True, null=True)
    current_country = models.CharField(max_length=100, blank=True, null=True)
    current_pincode = models.CharField(max_length=10, blank=True, null=True)

    permanent_street = models.CharField(max_length=255, blank=True, null=True)
    permanent_city = models.CharField(max_length=100, blank=True, null=True)
    permanent_state = models.CharField(max_length=100, blank=True, null=True)
    permanent_country = models.CharField(max_length=100, blank=True, null=True)
    permanent_pincode = models.CharField(max_length=10, blank=True, null=True)


    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    spouse_name = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    high_school = models.FileField(upload_to='high_school/', blank=True, null=True)
    intermediate = models.FileField(upload_to='intermediate/', blank=True, null=True)
    graduation = models.FileField(upload_to='graduation/', blank=True, null=True)
    post_graduation = models.FileField(upload_to='post_graduation/', blank=True, null=True)
    other_qualification = models.FileField(upload_to='other_qualification/', blank=True, null=True)
    # Communication details    
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True)
    internal_email = models.EmailField(blank=True, null=True)
    personal_email = models.EmailField(blank=True, null=True)

    # Document section
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)
    aadhar_doc = models.FileField(upload_to='documents/', blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    pan_doc = models.FileField(upload_to='documents/', blank=True, null=True)
    offer_letter = models.FileField(upload_to='documents/', blank=True, null=True)
    relieving_letter = models.FileField(upload_to='documents/', blank=True, null=True)
    resignation_letter = models.FileField(upload_to='documents/', blank=True, null=True)
    appointment_letter = models.FileField(upload_to='documents/', blank=True, null=True)
    bank_statement = models.FileField(upload_to='documents/', blank=True, null=True)
    salary_slip1 = models.FileField(upload_to='documents/', blank=True, null=True)
    salary_slip2 = models.FileField(upload_to='documents/', blank=True, null=True)
    salary_slip3 = models.FileField(upload_to='documents/', blank=True, null=True)

    # Previous employment details
    previous_company_name = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    previous_role = models.CharField(max_length=100, blank=True, null=True)
    reference_name = models.CharField(max_length=100, blank=True, null=True)
    reference_email = models.EmailField(blank=True, null=True)
    reference_mobile = models.CharField(max_length=15, blank=True, null=True)
    reference_role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
    
    work_preference = models.CharField(
        max_length=10, 
        choices=[('WFH', 'Work From Home'), ('WFO', 'Work From Office')], 
        default='WFO'
    )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees') 
    position = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, related_name='employees') 

class LoginLogoutHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time} to {self.logout_time}"
class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) 
    leave_type = models.CharField(max_length=50, choices=[('sick', 'Sick'), ('casual', 'Casual'), ('earned', 'Earned')])
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')  
    

    def __str__(self):
        return f"{self.employee} - {self.leave_type}"

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    employees = models.ManyToManyField(Employee, related_name='holidays', blank=True)
    leave = models.ManyToManyField(Leave, related_name='holidays', blank=True)

    def __str__(self):
        return self.name

class Claim(models.Model):
    
    CATEGORY_CHOICES = [
        ('broadband', 'Broadband'),
        ('mobile', 'Mobile'),
        ('travel_allowance', 'Travel Allowance'),
        ('other', 'Other'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES) 
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    description = models.TextField(blank=True, null=True) 
    claim_file = models.FileField(upload_to='claims/', blank=True, null=True)  
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    last_action = models.DateTimeField(auto_now=True)
    date_from = models.DateField(default=timezone.now)
    date_to = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.employee} - {self.category} - {self.amount}"


class BasicInformation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length  = 10 ,choices = [('male','Male'),('female','Female'),('other','Other')])
    blood_group = models.CharField(max_length = 10)
    date_of_joining = models.DateField()
    employee_type = models.CharField(max_length  = 100)
    employee_band = models.CharField(max_length  = 100)
    job_title  = models.CharField(max_length  = 100)
    shift = models.CharField(max_length  = 100)

class AccountDetails(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    account_number = models.IntegerField()
    bank_name = models.CharField(max_length  = 100)
    branch_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length  = 100)

class CurrentAddress(models.Model):
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE)
    address_line_1 = models.CharField(max_length  = 100)
    address_line_2 = models.CharField(max_length  = 100)
    city = models.CharField(max_length  = 100)
    state = models.CharField(max_length  = 100)
    pincode = models.IntegerField()

class PermanentAddress(models.Model):  
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE)
    address_line_1 = models.CharField(max_length  = 100)
    address_line_2 = models.CharField(max_length  = 100)
    city = models.CharField(max_length  = 100)
    state = models.CharField(max_length  = 100)
    pincode = models.IntegerField()

class FamilyDetails(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='family_details')
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    spouse_name = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=15)

class EducationDetails(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='education_details')
    high_school = models.CharField(max_length=100)
    intermediate = models.CharField(max_length=100)
    graduation = models.CharField(max_length=100)
    post_graduation = models.CharField(max_length=100, blank=True, null=True)

class CommunicationDetails(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='communication_details')
    mobile_number = models.CharField(max_length=15)
    company_email = models.EmailField()
    internal_email = models.EmailField(blank=True, null=True)
    personal_email = models.EmailField()

class DocumentSection(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='document_section')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    aadhar_number = models.CharField(max_length=12)
    aadhar_doc = models.FileField(upload_to='documents/aadhar/', blank=True, null=True)
    pan_number = models.CharField(max_length=10)
    pan_doc = models.FileField(upload_to='documents/pan/', blank=True, null=True)
    offer_letter = models.FileField(upload_to='documents/offer_letters/', blank=True, null=True)
    relieving_letter = models.FileField(upload_to='documents/relieving_letters/', blank=True, null=True)
    resignation_letter = models.FileField(upload_to='documents/resignation_letters/', blank=True, null=True)
    appointment_letter = models.FileField(upload_to='documents/appointment_letters/', blank=True, null=True)
    bank_statement = models.FileField(upload_to='documents/bank_statements/', blank=True, null=True)
    salary_slip1 = models.FileField(upload_to='documents/salary_slips/', blank=True, null=True)
    salary_slip2 = models.FileField(upload_to='documents/salary_slips/', blank=True, null=True)
    salary_slip3 = models.FileField(upload_to='documents/salary_slips/', blank=True, null=True)

class PreviousEmploymentDetails(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='previous_employment_details')
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    previous_role = models.CharField(max_length=100)
    reference_name = models.CharField(max_length=100)
    reference_email = models.EmailField()
    reference_mobile = models.CharField(max_length=15)
    reference_role = models.CharField(max_length=100)


class SalarySlip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.employee} - {self.month}/{self.year}"

class HRPolicy(models.Model):
    policy_type = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.policy_type
    
class TimeSheet(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    work_hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.employee} - {self.date}"

class project(models.Model):  
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20)

class Training(models.Model):
    timesheet  = models.OneToOneField(TimeSheet, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20)

class WorkFromHome(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='wfh_status')
    wfh_date = models.DateField()

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - WFH on {self.wfh_date}"
    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20)
    check_in = models.TimeField()
    check_out = models.TimeField()
    work_mode = models.CharField(max_length=20)

    def __str__(self):  
        return f"{self.employee.first_name} {self.employee.last_name} - {self.date}"

