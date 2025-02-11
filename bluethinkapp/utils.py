from .models import SalarySlip, Employee
from datetime import datetime

def is_holiday(day):
    # Define a function to check if a day is a holiday
    # Example: return True if day is a public holiday
    return False

def calculate_salary(employee, month, year):
    first_day = date(year, month, 1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    total_present = 0
    total_absent = 0
    total_leave = 0

    for day in range(1, last_day.day + 1):
        current_date = date(year, month, day)
        
        # Determine status based on timesheets and leaves
        timesheets = TimeSheet.objects.filter(employee=employee, date=current_date, status='approved')
        leaves = Leave.objects.filter(employee=employee, start_date__lte=current_date, end_date__gte=current_date, status='approved')
        
        if timesheets.exists():
            total_present += 1
        elif leaves.exists():
            total_leave += 1
        elif current_date.weekday() in [5, 6] or is_holiday(current_date):  # Weekend or Holiday
            continue
        else:
            total_absent += 1
    
    # Calculate salary
    salary_per_day = employee.salary_per_day
    total_salary = (total_present + total_leave) * salary_per_day  # Paid leaves included

    # Store in database
    salary_slip, created = SalarySlip.objects.get_or_create(
        employee=employee, month=month, year=year,
        defaults={
            'total_present_days': total_present,
            'total_absent_days': total_absent,
            'total_leave_days': total_leave,
            'total_salary': total_salary
        }
    )

    if not created:
        salary_slip.total_present_days = total_present
        salary_slip.total_absent_days = total_absent
        salary_slip.total_leave_days = total_leave
        salary_slip.total_salary = total_salary
        salary_slip.save()
    
    return salary_slip