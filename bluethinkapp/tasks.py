from celery import shared_task
from django.utils.timezone import now
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Employee

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


from celery import shared_task
from django.utils.timezone import now
from datetime import date
from dateutil.relativedelta import relativedelta
from bluethinkapp.models import Employee, SalarySlip, TimeSheet, Leave  

@shared_task
def generate_salary_slips():
    today = date.today()
    
    # Get the previous month and adjust the year if needed
    previous_month = today - relativedelta(months=1)
    month = previous_month.month
    year = previous_month.year

    employees = Employee.objects.all()

    for employee in employees:
        if employee.salary is None:
            continue  # Skip employees with no salary set

        # Fetch records for the previous month
        timesheets = TimeSheet.objects.filter(employee=employee, date__month=month, date__year=year)
        leaves = Leave.objects.filter(employee=employee, start_date__month=month, start_date__year=year)

        # Count present and absent days based on status
        present_days = timesheets.filter(status="Approved").count()  # Ensure correct capitalization
        absent_days = timesheets.filter(status="Rejected").count()

        # Calculate total leave days
        leave_days = sum((leave.end_date - leave.start_date).days + 1 for leave in leaves if leave.status == "Approved")

        # Salary calculations
        base_salary = float(employee.salary)  # Convert to float to avoid TypeErrors
        per_day_salary = base_salary / 30  # Assume 30 days per month
        deductions = absent_days * per_day_salary
        total_salary = base_salary - deductions  # Deduct absent days

        # Ensure values are not negative
        total_salary = max(total_salary, 0)

        # Create or update salary slip
        SalarySlip.objects.update_or_create(
            employee=employee,
            month=str(month),
            year=year,
            defaults={
                'basic_salary': employee.base_salary,  # ✅ Match Employee model field
                'hra': employee.base_salary * 0.2,  # ✅ Example HRA calculation
                'deductions': absent_days * employee.salary_per_day,  # ✅ Use correct field
                'net_salary': employee.base_salary - (absent_days * employee.salary_per_day),  
                'total_present_days': present_days,
                'total_absent_days': absent_days,
                'total_leave_days': leave_days,
                'total_salary': employee.base_salary - (absent_days * employee.salary_per_day)
            }
        )
    
    return "Salary slips generated successfully!"
