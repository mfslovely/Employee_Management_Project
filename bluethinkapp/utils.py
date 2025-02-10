from .models import SalarySlip, Employee
from datetime import datetime

def generate_salary_slip(employee, present_days, absent_days):
    month_name = datetime.today().strftime('%B %Y')  # e.g., "February 2025"
    base_salary = employee.salary
    per_day_salary = base_salary / 30  # Assuming 30 days in a month
    deductions = absent_days * per_day_salary
    net_salary = base_salary - deductions

    salary_slip, created = SalarySlip.objects.get_or_create(
        employee=employee,
        month=month_name,
        defaults={
            'base_salary': base_salary,
            'present_days': present_days,
            'absent_days': absent_days,
            'deductions': deductions,
            'net_salary': net_salary
        }
    )
    return salary_slip
