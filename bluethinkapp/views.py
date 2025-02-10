from django.shortcuts import render,redirect
import json
from django.utils.timezone import now
from django.db.models import Sum
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.db.models import Q
from datetime import timedelta
from .models import Employee,WorkFromHome,Leave,BasicInformation,LoginLogoutHistory, Claim,TimeSheet,Role,Department,Project,Holiday,Asset,AssignedDevice,ProjectAssignment,TeamLead, TeamMember
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth import authenticate, login ,logout
from .forms import (
    AccountDetailsForm,
    CurrentAddressForm,
    PermanentAddressForm,
    FamilyDetailsForm,
    EducationDetailsForm,
    CommunicationDetailsForm,
    DocumentSectionForm,
    PreviousEmploymentDetailsForm,ClaimForm,ApplyLeaveForm,TimeSheetForm,ProjectForm,HolidayForm,ProjectAssignmentForm,EmployeeForm
)
from django.views import View
from .tasks import check_login_and_notify 
from django.http import JsonResponse,HttpResponseForbidden,HttpResponse
from django.shortcuts import get_object_or_404
from datetime import timedelta ,date , datetime
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from .forms import ApplyLeaveForm
from .models import Leave, Employee, Department
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ApplyLeaveForm
from .models import Leave, Employee
from django.core.mail import send_mail
from datetime import date
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import SalarySlip




def dashboard(request):
    today = timezone.now().date()
    next_month = today + timedelta(days=30)

    upcoming_birthdays = BasicInformation.objects.filter(
        date_of_birth__month=today.month, 
        date_of_birth__day__gte=today.day, 
        date_of_birth__day__lte=next_month.day
    )
    upcoming_anniversaries = BasicInformation.objects.filter(
        date_of_joining__month=today.month, 
        date_of_joining__day__gte=today.day, 
        date_of_joining__day__lte=next_month.day
    )
    employees_on_leave = Leave.objects.filter(
        start_date__lte=today, 
        end_date__gte=today
    )

    employees_working_from_home = WorkFromHome.objects.all()
    assigned_assets = Asset.objects.filter(owned_by__isnull=False)
    

    # Get the assigned devices for the manager's dashboard
    assigned_devices = AssignedDevice.objects.select_related('asset', 'employee').all()
    context = {
        'upcoming_birthdays': upcoming_birthdays,
        'upcoming_anniversaries': upcoming_anniversaries,
        'employee_on_leave': employees_on_leave,
        'employee_working_from_home': employees_working_from_home,
        'assigned_assets': assigned_assets,
        'assigned_devices': assigned_devices,
    }
    return render(request, 'bluethinkincapp/deshboard.html', context)

def manager_dashboard(request):
    today = timezone.now().date()
    next_month = today + timedelta(days=30)

    upcoming_birthdays = BasicInformation.objects.filter(
        date_of_birth__month=today.month, 
        date_of_birth__day__gte=today.day, 
        date_of_birth__day__lte=next_month.day
    )
    upcoming_anniversaries = BasicInformation.objects.filter(
        date_of_joining__month=today.month, 
        date_of_joining__day__gte=today.day, 
        date_of_joining__day__lte=next_month.day
    )
    employees_on_leave = Leave.objects.filter(
        start_date__lte=today, 
        end_date__gte=today
    )

    employees_working_from_home = WorkFromHome.objects.all()
    assigned_assets = Asset.objects.filter(owned_by__isnull=False)
    

    # Get the assigned devices for the manager's dashboard
    assigned_devices = AssignedDevice.objects.select_related('asset', 'employee').all()
    context = {
        'upcoming_birthdays': upcoming_birthdays,
        'upcoming_anniversaries': upcoming_anniversaries,
        'employee_on_leave': employees_on_leave,
        'employee_working_from_home': employees_working_from_home,
        'assigned_assets': assigned_assets,
        'assigned_devices': assigned_devices,
    }
    return render(request, 'manager/manager_dashboard.html', context)

def director_dashboard(request):
    return render(request, 'Director/director_dashboard.html')

def hr_dashboard(request):
    today = timezone.now().date()
    next_month = today + timedelta(days=30)

    upcoming_birthdays = BasicInformation.objects.filter(
        date_of_birth__month=today.month, 
        date_of_birth__day__gte=today.day, 
        date_of_birth__day__lte=next_month.day
    )
    upcoming_anniversaries = BasicInformation.objects.filter(
        date_of_joining__month=today.month, 
        date_of_joining__day__gte=today.day, 
        date_of_joining__day__lte=next_month.day
    )
    employees_on_leave = Leave.objects.filter(
        start_date__lte=today, 
        end_date__gte=today
    )

    employees_working_from_home = WorkFromHome.objects.all()
    assigned_assets = Asset.objects.filter(owned_by__isnull=False)
    

    # Get the assigned devices for the manager's dashboard
    assigned_devices = AssignedDevice.objects.select_related('asset', 'employee').all()
    context = {
        'upcoming_birthdays': upcoming_birthdays,
        'upcoming_anniversaries': upcoming_anniversaries,
        'employee_on_leave': employees_on_leave,
        'employee_working_from_home': employees_working_from_home,
        'assigned_assets': assigned_assets,
        'assigned_devices': assigned_devices,
    }
    return render(request, 'HR/hr_dashboard.html',context)

def admin_dashboard(request):
    today = timezone.now().date()
    next_month = today + timedelta(days=30)

    upcoming_birthdays = BasicInformation.objects.filter(
        date_of_birth__month=today.month, 
        date_of_birth__day__gte=today.day, 
        date_of_birth__day__lte=next_month.day
    )
    upcoming_anniversaries = BasicInformation.objects.filter(
        date_of_joining__month=today.month, 
        date_of_joining__day__gte=today.day, 
        date_of_joining__day__lte=next_month.day
    )
    employees_on_leave = Leave.objects.filter(
        start_date__lte=today, 
        end_date__gte=today
    )

    employees_working_from_home = WorkFromHome.objects.all()
    assigned_assets = Asset.objects.filter(owned_by__isnull=False)
    

    # Get the assigned devices for the manager's dashboard
    assigned_devices = AssignedDevice.objects.select_related('asset', 'employee').all()
    context = {
        'upcoming_birthdays': upcoming_birthdays,
        'upcoming_anniversaries': upcoming_anniversaries,
        'employee_on_leave': employees_on_leave,
        'employee_working_from_home': employees_working_from_home,
        'assigned_assets': assigned_assets,
        'assigned_devices': assigned_devices,
    }

    return render(request, 'admin/admin_dashboard.html', {'assigned_devices': assigned_devices, 'upcoming_birthdays': upcoming_birthdays, 'upcoming_anniversaries': upcoming_anniversaries, 'employees_on_leave': employees_on_leave, 'employees_working_from_home': employees_working_from_home, 'assigned_assets': assigned_assets
        
    })
    

def employee_register(request):
    roles = Role.objects.all()
    departments = Department.objects.all()

    if request.method == 'POST':
        department_name = request.POST.get('department')    
        role_name = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        date_of_birth = request.POST.get('date_of_birth')
        date_of_joining = request.POST.get('date_of_joining')
        job_title = request.POST.get('job_title')
        hashed_password = make_password(password)

        # Check if all fields are filled
        if not first_name or not last_name or not email or not password:
            messages.error(request, 'Please fill all the fields')
            return render(request, 'bluethinkincapp/employee_register.html', {'roles': roles, 'departments': departments})

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An employee with this email already exists.')
            return render(request, 'bluethinkincapp/employee_register.html', {'roles': roles, 'departments': departments})

        # Handle Role selection
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            messages.error(request, 'Invalid role selected')
            return render(request, 'bluethinkincapp/employee_register.html', {'roles': roles, 'departments': departments})

        # Handle Department selection
        try:
            department = Department.objects.get(name=department_name)
        except Department.DoesNotExist:
            messages.error(request, 'Invalid department selected')
            return render(request, 'bluethinkincapp/employee_register.html', {'roles': roles, 'departments': departments})

        # Check if the user already exists (based on email)
        user = User.objects.filter(email=email).first()
        if not user:
            # If user doesn't exist, create a new one
            user = User.objects.create(username=email, email=email, password=hashed_password)
        
        # Create employee
        employee = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            date_of_birth=date_of_birth,
            date_of_joining=date_of_joining,
            job_title=job_title,
            user=user,  # Associate the employee with the user
            role=role,
            department=department
        )
        employee.save()
        messages.success(request, 'Employee registered successfully')
        return redirect('employee_login')
    return render(request, 'bluethinkincapp/employee_register.html', {'roles': roles, 'departments': departments})


def employee_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Employee with this email does not exist')
            return render(request, 'bluethinkincapp/employee_login.html')
        

        if user is not None:
            login(request, user)
            employee = Employee.objects.get(user=user)  # Get the employee object

            messages.success(request, 'Employee logged in successfully')
            check_login_and_notify.delay(user_id=user.id)  # This sends the task asynchronously
            
            # Check both role and department for employee
            if employee.role.name == 'Employee':
                department_name = employee.department.name  # Get department name
                if department_name == 'Python':
                    return redirect('dashboard')  # Redirect to employee's Python dashboard
                elif department_name == 'Java':
                    return redirect('dashboard')  # Redirect to employee's Java dashboard
                elif department_name == 'Web Development':
                    return redirect('dashboard')  # Redirect to employee's Web Dev dashboard
                elif department_name == 'Dynamics':
                    return redirect('dashboard')  # Redirect to employee's Dynamics dashboard
                elif department_name == 'HR':
                    return redirect('dashboard')  # Redirect to employee's HR dashboard
                elif department_name == 'BDE':
                    return redirect('dashboard')  # Redirect to employee's BDE dashboard
                elif department_name == 'Management':
                    return redirect('dashboard')  # Redirect to employee's Management dashboard
                else:
                    return redirect('dashboard')  # Default employee dashboard
                
            elif employee.role.name == 'Manager':
                department_name = employee.department.name  # Get department name
                if department_name == 'Python':
                    return redirect('manager_dashboard')  # Redirect to manager's Python dashboard
                elif department_name == 'Java':
                    return redirect('manager_dashboard')  # Redirect to manager's Java dashboard
                elif department_name == 'Web Development':
                    return redirect('manager_dashboard')  # Redirect to manager's Web Dev dashboard
                elif department_name == 'Dynamics':
                    return redirect('manager_dashboard')  # Redirect to manager's Dynamics dashboard
                elif department_name == 'HR':
                    return redirect('manager_dashboard')  # Redirect to manager's HR dashboard
                elif department_name == 'BDE':
                    return redirect('manager_dashboard')  # Redirect to manager's BDE dashboard
                elif department_name == 'Management':
                    return redirect('manager_dashboard')  # Redirect to manager's Management dashboard
                else:
                    return redirect('manager_dashboard')  # Default manager dashboard

            elif employee.role.name == 'Director':
                return redirect('director_dashboard')
            
            elif employee.role.name == 'Admin':
                return redirect('admin_dashboard')  # Redirect to director's dashboard
                
            elif employee.role.name == 'HR':
                return redirect('hr_dashboard')  # Redirect to HR's dashboard

        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'bluethinkincapp/employee_login.html')





@login_required
def employee_profile(request):
    try:
        employee = request.user.employee  
    except Employee.DoesNotExist:
        messages.error(request, "Employee profile not found.")
        return redirect('dashboard')
    
    
    account_form = AccountDetailsForm(instance=employee)
    current_address_form = CurrentAddressForm(instance=employee)
    permanent_address_form = PermanentAddressForm(instance=employee)
    family_details_form = FamilyDetailsForm(instance=employee)
    education_details_form = EducationDetailsForm(instance=employee)
    communication_details_form = CommunicationDetailsForm(instance=employee)
    document_section_form = DocumentSectionForm(instance=employee)
    previous_employment_details_form = PreviousEmploymentDetailsForm(instance=employee)

    if request.method == 'POST':
        
        if 'profile_photo' in request.FILES:
            employee.profile_photo = request.FILES['profile_photo']
            employee.save()
            messages.success(request, 'Profile photo updated successfully.')

        if 'account_details' in request.POST:
            account_form = AccountDetailsForm(request.POST, instance=employee)
            if account_form.is_valid():
                account_form.save()
                employee = request.user.employee  # Refresh the employee data
                messages.success(request, 'Account details updated successfully.')
            else:
                messages.error(request, 'Error updating account details.')

        elif 'current_address' in request.POST:
            current_address_form = CurrentAddressForm(request.POST, instance=employee)
            if current_address_form.is_valid():
                current_address_form.save()
                employee = request.user.employee  # Refresh the employee data
                messages.success(request, 'Current address updated successfully.')
            else:
                messages.error(request, 'Error updating current address.')

        elif 'permanent_address' in request.POST:
            permanent_address_form = PermanentAddressForm(request.POST, instance=employee)
            if permanent_address_form.is_valid():
                permanent_address_form.save()
                employee = request.user.employee  # Refresh the employee data
                messages.success(request, 'Permanent address updated successfully.')
            else:
                messages.error(request, 'Error updating permanent address.')

        elif 'family_details' in request.POST:
            family_details_form = FamilyDetailsForm(request.POST, instance=employee)
            if family_details_form.is_valid():
                family_details_form.save()
                employee = request.user.employee  # Refresh the employee data
                messages.success(request, 'Family details updated successfully.')
            else:
                messages.error(request, 'Error updating family details.')

        elif 'education_details' in request.POST:
            education_details_form = EducationDetailsForm(request.POST, instance=employee)
            if education_details_form.is_valid():
                education_details_form.save()
                employee = request.user.employee 
                messages.success(request, 'Education details updated successfully.')
            else:
                messages.error(request, 'Error updating education details.')

        elif 'communication_details' in request.POST:
            communication_details_form = CommunicationDetailsForm(request.POST, instance=employee)
            if communication_details_form.is_valid():
                communication_details_form.save()
                employee = request.user.employee 
                messages.success(request, 'Communication details updated successfully.')
            else:
                messages.error(request, 'Error updating communication details.')

        elif 'document_section' in request.POST:
            document_section_form = DocumentSectionForm(request.POST, request.FILES, instance=employee)
            if document_section_form.is_valid():
                document_section_form.save()
                employee = request.user.employee 
                messages.success(request, 'Documents updated successfully.')
            else:
                messages.error(request, 'Error updating documents.')

        elif 'previous_employment_details' in request.POST:
            previous_employment_details_form = PreviousEmploymentDetailsForm(request.POST, instance=employee)
            if previous_employment_details_form.is_valid():
                previous_employment_details_form.save()
                employee = request.user.employee  
                messages.success(request, 'Previous employment details updated successfully.')
            else:
                messages.error(request, 'Error updating previous employment details.')
    
    context = {
        'employee': employee,
        'account_form': account_form,
        'current_address_form': current_address_form,
        'permanent_address_form': permanent_address_form,
        'family_details_form': family_details_form,
        'education_details_form': education_details_form,
        'communication_details_form': communication_details_form,
        'document_section_form': document_section_form,
        'previous_employment_details_form': previous_employment_details_form,
        
    }
    
    return render(request, 'bluethinkincapp/employee_profile.html', context)




def logout_for_the_day(request):
   
    activity = LoginLogoutHistory.objects.filter(user=request.user).last()
    
    if activity and not activity.logout_time:
        activity.logout_time = timezone.now()
        activity.save()

   
    activities = LoginLogoutHistory.objects.filter(user=request.user).order_by('-login_time')
    
   
    logout(request)

    
    return render(request, 'bluethinkincapp/logout_history.html', {'activities': activities})

def is_holiday(day):
    holidays = [
        date(2024, 1, 1),  # New Year's Day
        date(2024, 11, 14),
          # Diwali
        # Add more holidays as required
    ]
    return day in holidays

@login_required
def leave_list(request):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    employee = Employee.objects.get(user=request.user)
    timesheets = TimeSheet.objects.filter(employee=employee)
    leaves = Leave.objects.filter(employee=employee)

    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    first_day = date(year, month, 1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    all_dates = [first_day + timedelta(days=i) for i in range((last_day - first_day).days + 1)]

    # Build the calendar data
    calendar_data = {}
    for day in all_dates:
        day_status = 'absent'  # Default to absent
        if timesheets.filter(date=day, status='approved').exists():
            day_status = 'present'
        elif timesheets.filter(date=day, status='rejected').exists():
            day_status = 'rejected'
        elif leaves.filter(start_date__lte=day, end_date__gte=day, status='approved').exists():
            day_status = 'leave'
        elif day.weekday() in [5, 6]:  
            day_status = 'weekend'
        elif is_holiday(day): 
            day_status = 'holiday'
        

        calendar_data[day.day] = day_status

    # Check if the request is an AJAX request (via the header)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'calendar_data': calendar_data})
    

    # For non-AJAX requests, render the page with the calendar data
    return render(request, 'bluethinkincapp/leave_management.html', {'calendar_data': calendar_data})



@method_decorator(login_required, name='dispatch')
class ApplyLeaveView(View):
    def get(self, request):
        employee = request.user.employee
        current_date = now().date()
        current_year = current_date.year
        current_month = current_date.month

        # Handle new employees
        joining_date = employee.date_of_joining
        if (current_date - joining_date).days < 90:
            total_casual_leave = 0 
        else:
            eligible_months = (current_year - joining_date.year) * 12 + current_month - joining_date.month + 1
            total_casual_leave = min(12, eligible_months - 3)

        # Filter applied casual leaves
        applied_leaves = Leave.objects.filter(
            employee=employee,
            start_date__year=current_year,
            category='casual',
            
        )

        
        try:
            applied_casual_leave = sum(
                (leave.end_date - leave.start_date).days + 1
                for leave in applied_leaves
            )
        except Exception as e:            
            applied_casual_leave = 0

        # Remaining casual leave
        remaining_casual_leave = max(0, total_casual_leave - applied_casual_leave)        
        form = ApplyLeaveForm()

        manager = Employee.objects.filter(department=employee.department, role__name="Manager").first()

        context = {
            "total_casual_leave": total_casual_leave,
            "applied_casual_leave": applied_casual_leave,
            "remaining_casual_leave": remaining_casual_leave,
            "form": form,
            "manager": manager,
            "applied_leaves": applied_leaves,
        }
        return render(request, "bluethinkincapp/apply_leave.html", context)

 

    def post(self, request):
        employee = request.user.employee
        form = ApplyLeaveForm(request.POST)

        if form.is_valid():
            leave_application = form.save(commit=False)
            leave_application.employee = employee

            # Recalculate leave availability
            current_date = now()
            current_year = current_date.year
            current_month = current_date.month
            

            # Handle new employees
            joining_date = employee.date_of_joining
            if (current_date.date() - joining_date).days < 90:
                total_casual_leave = 0
            else:
                eligible_months = (current_year - joining_date.year) * 12 + current_month - joining_date.month + 1
                total_casual_leave = min(12, eligible_months - 3)

            applied_leaves = Leave.objects.filter(
                employee=employee,
                start_date__year=current_year,
                category='casual'
            )            

            applied_casual_leave = (
                applied_leaves.annotate(
                    duration=ExpressionWrapper(
                        F('end_date') - F('start_date') + 1,
                        output_field=IntegerField()
                    )
                ).aggregate(total_days=Sum('duration'))['total_days'] or 0
            )

              # Debugging

            remaining_casual_leave = max(0, total_casual_leave - applied_casual_leave)
              # Debugging

            # Determine leave status
            leave_duration = (leave_application.end_date - leave_application.start_date).days + 1
            if leave_application.category == 'casual' and leave_duration <= remaining_casual_leave:
                leave_application.status = 'pending'
            else:
                leave_application.status = 'without_pay'

            manager = Employee.objects.filter(department=employee.department, role__name="Manager").first()
            
            if manager:
                leave_application.approved_by = manager

            leave_application.save()            
            return redirect('apply_leave')

        return render(request, "bluethinkincapp/apply_leave.html", {"form": form})

@method_decorator(login_required, name='dispatch')
class MangerLeaveView(View):
    def get(self, request):
        # Get the manager's details
        employee = request.user.employee
        search_query = request.GET.get('first_name', '').strip()
        leave_requests_pending = Leave.objects.filter(approved_by=employee, status='pending')
        leave_requests_approved = Leave.objects.filter(approved_by=employee, status='approved')
        leave_requests_rejected = Leave.objects.filter(approved_by=employee, status='rejected')

        if search_query:
            filter_query = Q(employee__first_name__icontains=search_query) | Q(employee__last_name__icontains=search_query)
            leave_requests_pending = leave_requests_pending.filter(filter_query)
            leave_requests_approved = leave_requests_approved.filter(filter_query)
            leave_requests_rejected = leave_requests_rejected.filter(filter_query)

        # Pass these requests to the template context
        context = {
            'leave_requests_pending': leave_requests_pending,
            'leave_requests_approved': leave_requests_approved,
            'leave_requests_rejected': leave_requests_rejected,
            'search_query': search_query
        }

        # Render the page with leave requests
        return render(request, 'manager/approve_leave.html', context)

    def post(self, request):
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')

        try:
           
            leave = Leave.objects.get(id=leave_id, approved_by=request.user.employee)

            # Check the action and update the leave status accordingly
            if action == 'approve':
                leave.status = 'approved'
            elif action == 'reject':
                leave.status = 'rejected'

            # Save the updated leave request
            leave.save()

            # Redirect to the same page to refresh the leave requests
            return redirect('approve_leave')

        except Leave.DoesNotExist:
            # If no leave request found with the given ID, return a 404 error
            return HttpResponse("Leave request does not exist.", status=404)

@method_decorator(login_required, name='dispatch')
class MangerLeaveView(View):
    def get(self, request):
        # Get the manager's details
        employee = request.user.employee
        search_query = request.GET.get('first_name', '').strip()
        leave_requests_pending = Leave.objects.filter(approved_by=employee, status='pending')
        leave_requests_approved = Leave.objects.filter(approved_by=employee, status='approved')
        leave_requests_rejected = Leave.objects.filter(approved_by=employee, status='rejected')

        if search_query:
            filter_query = Q(employee__first_name__icontains=search_query) | Q(employee__last_name__icontains=search_query)
            leave_requests_pending = leave_requests_pending.filter(filter_query)
            leave_requests_approved = leave_requests_approved.filter(filter_query)
            leave_requests_rejected = leave_requests_rejected.filter(filter_query)

        # Pass these requests to the template context
        context = {
            'leave_requests_pending': leave_requests_pending,
            'leave_requests_approved': leave_requests_approved,
            'leave_requests_rejected': leave_requests_rejected,
            'search_query': search_query
        }

        # Render the page with leave requests
        return render(request, 'manager/approve_leave.html', context)

    def post(self, request):
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')

        try:
           
            leave = Leave.objects.get(id=leave_id, approved_by=request.user.employee)

            # Check the action and update the leave status accordingly
            if action == 'approve':
                leave.status = 'approved'
            elif action == 'reject':
                leave.status = 'rejected'

            # Save the updated leave request
            leave.save()

            # Redirect to the same page to refresh the leave requests
            return redirect('approve_leave')

        except Leave.DoesNotExist:
            # If no leave request found with the given ID, return a 404 error
            return HttpResponse("Leave request does not exist.", status=404)


class MangerTimesheetView(View):
    def get(self, request):
        employee_name = request.GET.get('first_name')
        month = request.GET.get('month')
        timesheets = TimeSheet.objects.all()

        if employee_name:
            timesheets = TimeSheet.objects.filter(employee__first_name__icontains=employee_name)

        if month == "current":
            today = date.today()
            start_of_month = today.replace(day=1)
            timesheets = timesheets.filter(date__gte=start_of_month)

        elif month == "previous":
            today = date.today()
            first_of_current_month = today.replace(day=1)
            last_month_end = first_of_current_month - timedelta(days=1)
            start_of_last_month = last_month_end.replace(day=1)
            timesheets = timesheets.filter(date__range=(start_of_last_month, last_month_end))

        return render(request, 'manager/approve_timesheet.html', {'timesheets': timesheets})
    
    def post(self, request):
        action = request.POST.get("action")
        timesheet_ids = request.POST.getlist("timesheet_ids")
        acknowledgment = request.POST.get("acknowledgment") == "on"
        for timesheet_id in timesheet_ids:
            timesheet = TimeSheet.objects.get(id=timesheet_id)

            # Get the individual comment for this timesheet
            comment_key = f"comments_{timesheet_id}"
            comment = request.POST.get(comment_key, "").strip()

            acknowledgment_key = f"acknowledgment_{timesheet_id}"
            acknowledgment = request.POST.get(acknowledgment_key) == "on"

            # Update the timesheet with the status and comment
            if action == "approve":
                timesheet.status = "approved"
            elif action == "reject":
                timesheet.status = "rejected"
            timesheet.comment = comment
            timesheet.acknowledgment = acknowledgment
            timesheet.save()

        messages.success(request, f"Timesheets {action}d successfully.")
        return redirect("manager_approve_timesheet")

@login_required
def some_view(request,user_id):
    """
    View to trigger the Celery task to check login status.
    """
    # Pass the current user's ID to the Celery task
    user_id = request.user.id  # Get the current user's ID
    check_login_and_notify.delay(user_id) 
    

    # Redirect to a success page or a relevant view after triggering the task
    return redirect('dashboard') 

@login_required
def claims(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            # Retrieve the Employee instance for the logged-in user
            employee = Employee.objects.get(user=request.user)                      # Assign the Employee instance to the claim
            claim.employee = employee                        # Save the claim
            claim.save()
            return redirect('claims')  # Redirect to the same page after saving the claim
    else:
        form = ClaimForm()    # Fetch the claims related to the logged-in employee
    user_claims = Claim.objects.filter(employee__user=request.user)

    return render(request, 'bluethinkincapp/claims.html', {
        'form': form,
        'user_claims': user_claims,
    }) 

@login_required
def add_time_sheet(request):
    # Ensure employee is retrieved correctly
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        # Handle case if the employee does not exist for some reason
        return HttpResponse("Employee not found", status=404)
    
    if request.method == 'POST':
        form = TimeSheetForm(request.POST)
        
        if form.is_valid():
            # Create timesheet object but don't save it yet
            timesheet = form.save(commit=False)
            timesheet.employee = employee  # Associate the timesheet with the logged-in employee

            # Get the assigned project through ProjectAssignment
            assigned_project_id = request.POST.get('assigned_project')
            if assigned_project_id:
                try:
                    # Find the ProjectAssignment for the given employee
                    assigned_project = ProjectAssignment.objects.get(
                        project_id=assigned_project_id,
                        employee=employee
                    )
                    # Link the timesheet to the ProjectAssignment instead of directly to Project
                    timesheet.project_assignment = assigned_project
                except ProjectAssignment.DoesNotExist:
                    form.add_error('assigned_project', 'Selected project is not assigned to you.')
                    return render(request, 'bluethinkincapp/add_time_sheet.html', {
                        'form': form,
                        'projects': Project.objects.filter(assigned_to=employee),
                        'timesheet': TimeSheet.objects.filter(employee=employee),
                    })
            # Save the timesheet to the database
            timesheet.save()
            return redirect('add_time_sheet')  # Redirect after successful form submission
        else:
            print(form.errors)  # This will print out any form validation errors to the console
    else:
        form = TimeSheetForm()

    # Filter projects for the logged-in user
    if request.user.is_staff:  # If the user is a manager
        projects = Project.objects.all()  # Managers can see all projects
    else:  # If the user is an employee
        # Only projects assigned to the employee through ProjectAssignment
        projects = Project.objects.filter(assignments__employee=employee)

    # Debugging: Print the employee and projects
    print(f"Employee: {employee.first_name} ============")
    print(f"Assigned Projects: {projects}=============")

    return render(request, 'bluethinkincapp/add_time_sheet.html', {
        'form': form,
        'timesheet': TimeSheet.objects.filter(employee__user=request.user),
        'projects': projects,  # Pass the filtered list of projects
        'employee_projects': projects,  # Ensure employee's projects are passed to the template
    })



@login_required
def edit_time_sheet(request):
    if request.method == 'POST':
        time_sheet_id = request.POST.get('time_sheet_id')
        acknowledgment = request.POST.get('acknowledgment') == 'on'  # Get acknowledgment checkbox value

        try:
            timesheet = TimeSheet.objects.get(pk=time_sheet_id)
        except TimeSheet.DoesNotExist:
            return HttpResponseForbidden("Timesheet not found.")
                                                                                                                                                                                                                        
        # Validate the logged-in user's access to this timeshee
        if timesheet.employee.user != request.user and not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to edit this timesheet.")
        
        form = TimeSheetForm(request.POST, instance=timesheet)
        
        if form.is_valid():
            timesheet = form.save(commit=False)
            if acknowledgment:  # Update acknowledgment if checked
                timesheet.acknowledgment = True
            if not request.user.is_staff:  # Ensure employee remains unchanged
                timesheet.employee = Employee.objects.get(user=request.user)
            timesheet.save()
            return redirect('add_time_sheet')

    return redirect('add_time_sheet')



@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user       
            return redirect('add_project')  # Redirect after successful save
        else:
            print(form.errors)  # Log the form errors
    else:
        form = ProjectForm()
    # Fetch all projects for dropdown
    projects = Project.objects.values("project_name", "vendor_name") 
    return render(request, 'manager/add_project.html', {'form': form, 'projects': projects})                 


@login_required
def manage_holidays(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            holiday = form.save()
            # Return success response
            return JsonResponse({'success': True, 'holiday': holiday.name})
        else:
            # If the form is not valid, return errors
            return JsonResponse({'success': False, 'errors': form.errors})

    else:
        form = HolidayForm()
        holidays = Holiday.objects.all()
        holiday_events = [
            {"title": holiday.name, "start": holiday.date.isoformat(), "description": holiday.description}
            for holiday in holidays
        ]
        holiday_events_json = json.dumps(holiday_events)
        return render(request, 'Director/manage_holidays.html', {
            'form': form,
            'holidays': holidays,
            'holiday_events_json': holiday_events_json,
        })
    


def assign_device(request):
    if request.method == "POST":
        asset_name = request.POST.get('asset_name')
        model_number = request.POST.get('model_number')
        serial_number = request.POST.get('serial_number')
        processor = request.POST.get('processor')
        storage = request.POST.get('storage')
        ram = request.POST.get('ram')
        employee_id = request.POST.get('employee_id')
        assigned_date = request.POST.get('assigned_date')
        category = request.POST.get('category')

        # Get employee object
        employee = Employee.objects.get(id=employee_id)

        # Create new asset
        asset = Asset.objects.create(
            asset_name=asset_name,
            model_number=model_number,
            serial_number=serial_number,
            processor=processor,
            storage=storage,
            ram=ram,
            category=category,
        )

        # Assign asset to employee
        assigned_device = AssignedDevice.objects.create(
            asset=asset,
            employee=employee,
            assigned_date=assigned_date,
            category=category,
        )

        messages.success(request, "Device assigned successfully!")
        return redirect('assign_device')  # redirect to the same page to clear the form

    
    assets = Asset.objects.all()
    employees = Employee.objects.all()
    assigned_devices = AssignedDevice.objects.all()

    return render(request, 'admin/assigned_device.html', {
        'assets': assets,
        'employees': employees,
        'assigned_devices': assigned_devices,
    })

@login_required
def manage_assign_projects(request):
    if request.method == 'POST':
        form = ProjectAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_assign_projects')
    else:
        form = ProjectAssignmentForm()
    
    assignments = ProjectAssignment.objects.all()

    return render(request, 'manager/manage_assign_projects.html', {'form': form, 'assignments': assignments})




@login_required
def assign_manager_view(request):
    # if request.user.employee.role.name != 'Director':
    #     messages.error(request, 'Access denied: Only directors can assign managers.')
    #     return redirect('assign_manager')  # Redirect non-directors to their dashboard
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        department_id = request.POST.get('department_id')
        
        try:
            employee = Employee.objects.get(id=employee_id)
            department = Department.objects.get(id=department_id)
        except (Employee.DoesNotExist, Department.DoesNotExist):
            messages.error(request, 'Invalid employee or department selected.')
            return redirect('assign_manager')
        
        # Check if the employee already has the role 'Manager' and is assigned to the department
        if employee.role and employee.department and employee.role.name == 'Manager' and employee.department == department:
            messages.error(request, f"{employee.first_name} {employee.last_name} is already a manager in the {department.name} team.")
            return redirect('assign_manager')
        
        # Check if the department already has a manager
        if Employee.objects.filter(role__name='Manager', department=department).exists():
            messages.error(request, f"A manager is already assigned to the {department.name} team.")
            return redirect('assign_manager')
        
        # Update the employee's role to manager and assign the department
        employee.role = Role.objects.get(name='Manager')
        employee.department = department
        employee.save()

        messages.success(request, f"{employee.first_name} {employee.last_name} has been assigned as a manager of the {department.name} team.")
        return redirect('director_dashboard')  # Redirect to director's dashboard after assignment

    # Fetch all employees (including those who are managers)
    employees = Employee.objects.all()  # Fetch all employees
    departments = Department.objects.all()  # Fetch all departments
    managers = Employee.objects.filter(role__name='Manager').exclude(role__isnull=True)  # Ensure valid role is assigned
    
    return render(request, 'Director/assign_manager.html', {'employees': employees, 'departments': departments, 'managers': managers})

def manage_team(request):
    manager = request.user.employee  # Assuming the logged-in user is linked to an Employee instance
    if not manager.role.name == "Manager":
        return redirect('unauthorized')  # Redirect if the user is not a manager

    department = manager.department  # Get the manager's department

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "assign_team_lead":
            # Assign a Team Lead
            employee_id = request.POST.get('employee_id')
            employee = Employee.objects.get(id=employee_id, department=department)
            TeamLead.objects.create(employee=employee, department=department)

        elif action == "assign_team_members":
            # Assign employees to a Team Lead
            lead_id = request.POST.get('lead_id')
            employee_ids = request.POST.getlist('employee_ids')
            lead = TeamLead.objects.get(id=lead_id, department=department)

            for emp_id in employee_ids:
                employee = Employee.objects.get(id=emp_id, department=department)
                TeamMember.objects.create(lead=lead, employee=employee)

        elif action == 'assign_under_team_member':
            # Assign employees under a specific Team Member
            team_member_id = request.POST.get('team_member_id')
            employee_ids = request.POST.getlist('employee_ids')

            # Fetch the team member
            team_member = TeamMember.objects.filter(employee_id=team_member_id).first()

            if not team_member:
                return redirect('manage_team')  # Handle case where no team member is found

            # Fetch the selected employees to assign
            selected_employees = Employee.objects.filter(id__in=employee_ids)

            for employee in selected_employees:
                # Create a new TeamMember instance for the subordinate under the team member
                TeamMember.objects.create(
                    parent_team_member=team_member,  # Assign the parent team member
                    employee=employee,               # The employee being assigned
                    lead=team_member.lead            # Use the same lead from the parent team member
                )

            return redirect('manage_team')  # Redirect to the manage team page

    # Fetch all employees in the department
    employees = Employee.objects.filter(department=department, role__name="Employee")
    team_leads = TeamLead.objects.filter(department=department)

    # Identify employees who are already assigned as team leads or team members
    assigned_employee_ids = TeamMember.objects.filter(
        lead__department=department
    ).values_list('employee_id', flat=True)

    team_lead_employee_ids = team_leads.values_list('employee_id', flat=True)

    # Mark employees as assigned, team leads, or unassigned
    employees_with_status = [

        {
            "id": employee.id,
            "name": f"{employee.first_name} {employee.last_name}",
            "is_assigned": employee.id in assigned_employee_ids,
            "is_team_lead": employee.id in team_lead_employee_ids,
        }
        for employee in employees
    ]

    # Fetch team members and their subordinates for hierarchy view
    team_members = TeamMember.objects.filter(lead__department=department)

    context = {
        'department': department,
        'team_leads': team_leads,
        'employees': employees,
        'employees_with_status': employees_with_status,
        'team_members': team_members,  # Include team members in the context
    }
    return render(request, 'manager/manage_team.html', context)


@method_decorator(login_required, name='dispatch')
class HRLeaveView(View):
    def get(self, request):
        # Search query to filter leaves by employee name
        search_query = request.GET.get('first_name', '').strip()

        # Fetch all leave requests for all employees
        leave_requests = Leave.objects.all()

        if search_query:
            # Filter by employee's first name or last name
            filter_query = Q(employee__first_name__icontains=search_query) | Q(employee__last_name__icontains=search_query)
            leave_requests = leave_requests.filter(filter_query)

        # Separate leave requests by status
        leave_requests_pending = leave_requests.filter(status='pending')
        leave_requests_approved = leave_requests.filter(status='approved')
        leave_requests_rejected = leave_requests.filter(status='rejected')

        # Pass the filtered data to the template context
        context = {
            'leave_requests_pending': leave_requests_pending,
            'leave_requests_approved': leave_requests_approved,
            'leave_requests_rejected': leave_requests_rejected,
            'search_query': search_query
        }

        # Render the HR leave list template
        return render(request, 'HR/Hr_leave_list.html', context)








def manage_employees(request):
    # Fetch all employees for listing
    employees = Employee.objects.all()

    # Determine if editing or adding based on `pk` parameter
    pk = request.GET.get('pk')  # `pk` parameter from query string
    if pk:
        # Editing an existing employee
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeForm(request.POST or None, instance=employee)
        action = "Edit Employee"
    else:
        # Adding a new employee
        employee = None
        form = EmployeeForm(request.POST or None)
        action = "Add Employee"

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_employees')

    return render(request, 'HR/manage_employees.html', {
        'employees': employees,
        'form': form,
        'action': action,
        'employee': employee
    })


class HrTimesheetView(View):
    def get(self, request):
        employee_name = request.GET.get('first_name')
        month = request.GET.get('month')
        timesheets = TimeSheet.objects.all()

        if employee_name:
            timesheets = timesheets.filter(employee__first_name__icontains=employee_name)

        today = date.today()

        if month == "current":
            start_of_month = today.replace(day=1)
            timesheets = timesheets.filter(date__gte=start_of_month)

        elif month == "previous":
            first_of_current_month = today.replace(day=1)
            last_month_end = first_of_current_month - timedelta(days=1)
            start_of_last_month = last_month_end.replace(day=1)
            timesheets = timesheets.filter(date__range=(start_of_last_month, last_month_end))

        return render(request, 'HR/manage_timesheet.html', {'timesheets': timesheets})


def generate_salary_pdf(request, slip_id):
    slip = SalarySlip.objects.get(id=slip_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="SalarySlip_{slip.employee.first_name}_{slip.month}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Salary Slip")

    p.setFont("Helvetica", 12)
    p.drawString(50, 770, f"Employee Name: {slip.employee.first_name} {slip.employee.last_name}")
    p.drawString(50, 750, f"Month: {slip.month}")
    p.drawString(50, 730, f"Base Salary: {slip.base_salary}")
    p.drawString(50, 710, f"Present Days: {slip.present_days}")
    p.drawString(50, 690, f"Absent Days: {slip.absent_days}")
    p.drawString(50, 670, f"Deductions: {slip.deductions}")
    p.drawString(50, 650, f"Net Salary: {slip.net_salary}")

    p.showPage()
    p.save()
    return response


def employee_salary_slips(request):
    employee = request.user.employee  # Get the logged-in employee
    current_month = date.today().strftime('%B %Y')
    
    slips = SalarySlip.objects.filter(employee=employee)  # Get the current month and year (e.g., January 2025)
    
    # Check if salary slip for the current month already exists
    try:
        salary_slip = SalarySlip.objects.get(employee=employee, month=current_month)
    except SalarySlip.DoesNotExist:
        salary_slip = None  # No salary slip generated yet

    if salary_slip:
        context = {'slips': [salary_slip]}  # If salary slip exists, show it
    else:
        context = {'no_slip_message': f"Salary slip for {current_month} will be available soon after the month ends."}
  
    return render(request, 'bluethinkincapp/salary_slips.html', {'slips': slips})

