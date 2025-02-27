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
import calendar


HOLIDAYS = {
    "2025-01-01",  # New Year
    "2025-12-25",  # Christmas
    "2025-07-04",  # Independence Day
    # Add more holidays here
}

def is_holiday(date_obj):
    return date_obj.strftime("%Y-%m-%d") in HOLIDAYS

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
    month_name = calendar.month_name[month]  # Convert number to name ("January", "December")

    # Fetch all timesheets for the employee in the given month (any status)
    timesheets = TimeSheet.objects.filter(employee=employee, date__month=month, date__year=year)

    last_day = calendar.monthrange(year, month)[1]  # Get the last day of the month
    start_date__lte = date(year, month, last_day)

    # Fetch all approved leaves that overlap with the month
    leaves = Leave.objects.filter(
        employee=employee,
        start_date__lte=start_date__lte, 
        end_date__gte=start_date__lte,
        status="Approved"
    )

    # Calculate number of leave days
    leave_days = sum((leave.end_date - leave.start_date).days + 1 for leave in leaves)

    # Get all days in the month
    total_present = timesheets.count()  # Count all filled timesheets
    print(total_present,"total presnt")
    total_leave = leave_days
    print(total_leave,"total leave")
    total_absent = 0
    print(total_absent,"gdjkfdfjknhi")

    first_day = date(year, month, 1)
    last_day = date(year, month, last_day)

    for day in range(1, last_day.day + 1):
        current_date = date(year, month, day)
        
        if not timesheets.filter(date=current_date).exists() and not leaves.filter(start_date__lte=current_date, end_date__gte=current_date).exists():
            if current_date.weekday() not in [5, 6]:  # Only count weekdays as absent
                total_absent += 1

    # Salary calculations
    base_salary = employee.base_salary or Decimal("0.00")
    salary_per_day = base_salary / Decimal("30")
    deductions = total_absent * salary_per_day
    total_salary = max(base_salary - deductions, Decimal("0.00"))

    # ✅ **Fix: Ensure `month` is always stored as a month name**
    SalarySlip.objects.update_or_create(
        employee=employee,
        month=month_name,  # Always store as "January", "December", etc.
        year=year,
        defaults={
            'basic_salary': base_salary,
            'hra': base_salary * Decimal("0.2"),
            'deductions': deductions,
            'net_salary': total_salary,
            'total_present_days': total_present,
            'total_absent_days': total_absent,
            'total_leave_days': total_leave,
            'total_salary': total_salary
        }
    )