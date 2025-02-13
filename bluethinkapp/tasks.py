from celery import shared_task
from django.utils.timezone import now
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Employee
from decimal import Decimal

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

from decimal import Decimal
from django.utils.timezone import now
from .models import Employee, SalarySlip, TimeSheet, Leave
from django.utils import timezone
from datetime import timedelta,date
import datetime 
from dateutil.relativedelta import relativedelta



@shared_task
def generate_salary_slips():
    today = date.today()
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
        present_days = timesheets.filter(status="Approved").count()
        absent_days = timesheets.filter(status="Rejected").count()

        # Calculate total leave days
        leave_days = sum((leave.end_date - leave.start_date).days + 1 for leave in leaves if leave.status == "Approved")

        # Calculate salary details
        base_salary = employee.salary or Decimal("0.00")  # Use employee salary or zero
        salary_per_day = base_salary / 30  # Assuming 30 days in a month
        deductions = absent_days * salary_per_day
        total_salary = base_salary - deductions

        # Ensure values are not negative
        total_salary = max(total_salary, Decimal("0.00"))

        # Create or update the salary slip for the employee
        SalarySlip.objects.update_or_create(
            employee=employee,
            month=str(month),  # Convert month number to name if needed
            year=year,
            defaults={
                'basic_salary': base_salary,
                'hra': base_salary * Decimal("0.2"),  # Assuming 20% HRA
                'deductions': deductions,
                'net_salary': total_salary,
                'total_present_days': present_days,
                'total_absent_days': absent_days,
                'total_leave_days': leave_days,
                'total_salary': total_salary
            }
        )
