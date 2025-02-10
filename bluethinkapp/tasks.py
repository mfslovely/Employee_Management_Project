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


# your_app/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Employee, SalarySlip
from datetime import timedelta

@shared_task
def generate_monthly_salary_slips():
    today = timezone.now()
    # Get the first day of the current month
    first_day_of_month = today.replace(day=1)
    
    # Generate salary slips for each employee
    employees = Employee.objects.all()
    
    for employee in employees:
        # Retrieve timesheet data for this month for each employee
        timesheet = employee.timesheet_set.filter(date__gte=first_day_of_month)
        
        # Calculate the salary based on attendance (e.g. present days, absent days)
        present_days = timesheet.filter(status="Present").count()
        absent_days = timesheet.filter(status="Absent").count()

        # Your salary calculation logic (you can modify this based on your actual business rules)
        total_salary = employee.salary  # Base salary
        salary_deduction = (absent_days * (employee.salary / 30))  # Assuming 30 days in a month
        total_salary -= salary_deduction
        
        # Create salary slip
        SalarySlip.objects.create(
            employee=employee,
            month=today.strftime('%B %Y'),
            total_salary=total_salary,
            generated_on=timezone.now()
        )
    return 'Salary slips generated successfully.'




