from celery import shared_task
from django.utils.timezone import now
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Employee
from decimal import Decimal
import pdb
from decimal import Decimal
from django.utils.timezone import now
from .models import Employee, SalarySlip, TimeSheet, Leave
from django.utils import timezone
from datetime import timedelta,date
import datetime 
from dateutil.relativedelta import relativedelta

@shared_task
def check_login_and_notify(user_id):
    """
    Task to check if the given user has logged in today. 
    If not, send them an email reminder.
    """
    try:
        employee = Employee.objects.get(user_id=user_id)
        user = employee.user  # Get the associated user object

        # Continue with your task as before
        last_login = user.last_login
        current_time = now()

        # if last_login is None or last_login.date() < current_time.date() or True:
        if current_time.hour >= 10 and (last_login is None or last_login.date()) < current_time.date():
            # Send email logic here
            html_message = render_to_string(
                'bluethinkincapp/login_reminder_email.html', 
                {'employee': employee}
            )
            plain_message = strip_tags(html_message)
            
            # Send email (make sure settings are configured for email sending)
            send_mail(
                subject="Login Reminder",
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[employee.email],
                fail_silently=False,
                html_message=html_message,
            )
    except Employee.DoesNotExist:
        print(f"Employee with user ID {user_id} does not exist.")





@shared_task
def generate_salary_slips():
    today = date.today()
    employees = Employee.objects.all()

    for employee in employees:
        if not employee.base_salary:
            continue  # Skip employees without a base salary

        joining_date = employee.date_of_joining
       
        if not joining_date:
            continue  # Skip if no joining date

        current_month = today.month
        current_year = today.year

        salary_month = joining_date.month
        salary_year = joining_date.year

        while (salary_year < current_year) or (salary_year == current_year and salary_month < current_month):
            generate_salary_for_month(employee, salary_month, salary_year)
            
            next_month = date(salary_year, salary_month, 1) + relativedelta(months=1)
            salary_month = next_month.month
            salary_year = next_month.year

def generate_salary_for_month(employee, month, year):
    pdb.set_trace()  # Debug: Inspect function call parameters

    timesheets = TimeSheet.objects.filter(employee=employee, date__month=month, date__year=year)
    leaves = Leave.objects.filter(employee=employee, start_date__month=month, start_date__year=year)
    
    present_days = timesheets.filter(status="Approved").count()
    absent_days = timesheets.filter(status="Rejected").count()

    leave_days = sum((leave.end_date - leave.start_date).days + 1 for leave in leaves if leave.status == "Approved")

    base_salary = employee.base_salary or Decimal("0.00")
    

    salary_per_day = base_salary / Decimal("30")
      

    deductions = absent_days * salary_per_day
    
    total_salary = max(base_salary - deductions, Decimal("0.00"))
    
    month_name = date(year, month, 1).strftime("%B")
   

    SalarySlip.objects.update_or_create(
        employee=employee,
        month=month_name,
        year=year,
        defaults={
            'basic_salary': base_salary,
            'hra': base_salary * Decimal("0.2"),
            'deductions': deductions,
            'net_salary': total_salary,
            'total_present_days': present_days,
            'total_absent_days': absent_days,
            'total_leave_days': leave_days,
            'total_salary': total_salary
        }
    )
    


# @shared_task
# def generate_salary_slips():
#     today = date.today()
#     previous_month = today - relativedelta(months=1)
#     month = previous_month.month
#     year = previous_month.year

#     employees = Employee.objects.all()

#     for employee in employees:
#         if employee.salary is None:
#             continue  # Skip employees with no salary set

#         # Fetch records for the previous month
#         timesheets = TimeSheet.objects.filter(employee=employee, date__month=month, date__year=year)
#         leaves = Leave.objects.filter(employee=employee, start_date__month=month, start_date__year=year)

#         # Count present and absent days based on status
#         present_days = timesheets.filter(status="Approved").count()
#         absent_days = timesheets.filter(status="Rejected").count()

#         # Calculate total leave days
#         leave_days = sum((leave.end_date - leave.start_date).days + 1 for leave in leaves if leave.status == "Approved")

#         # Calculate salary details
#         base_salary = employee.salary or Decimal("0.00")  # Use employee salary or zero
#         print(base_salary,"base salary ==")
#         salary_per_day = base_salary / 30 # Assuming 30 days in a month

#         print(salary_per_day,"=================== hello")  
#         deductions = absent_days * salary_per_day
#         print(deductions,"Dedection")
#         total_salary = base_salary - deductions

#         # Ensure values are not negative
#         total_salary = max(total_salary, Decimal("0.00"))

#         # Create or update the salary slip for the employee
#         SalarySlip.objects.update_or_create(
#             employee=employee,
#             month=str(month),  # Convert month number to name if needed
#             year=year,
#             defaults={
#                 'basic_salary': base_salary,
#                 'hra': base_salary * Decimal("0.2"),  # Assuming 20% HRA
#                 'deductions': deductions,
#                 'net_salary': total_salary,
#                 'total_present_days': present_days,
#                 'total_absent_days': absent_days,
#                 'total_leave_days': leave_days,
#                 'total_salary': total_salary
#             }
#         )
