from django.shortcuts import render,redirect
from django.utils.timezone import now
from django.db.models import Sum
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import Employee,WorkFromHome,Leave,BasicInformation,LoginLogoutHistory, Claim,TimeSheet,Role,Department,Project
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
    PreviousEmploymentDetailsForm,ClaimForm,ApplyLeaveForm,TimeSheetForm,ProjectForm
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
    

    context = {
        'upcoming_birthdays': upcoming_birthdays,
        'upcoming_anniversaries': upcoming_anniversaries,
        'employee_on_leave': employees_on_leave,
        'employee_working_from_home': employees_working_from_home,
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
    

    context = {
        'upcoming_birthdays': upcoming_birthdays,
        'upcoming_anniversaries': upcoming_anniversaries,
        'employee_on_leave': employees_on_leave,
        'employee_working_from_home': employees_working_from_home,
    }
    return render(request, 'manager/manager_dashboard.html', context)

def director_dashboard(request):
    return render(request, 'director_dashboard.html')

def hr_dashboard(request):
    return render(request, 'hr_dashboard.html')


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
                return redirect('director_dashboard')  # Redirect to director's dashboard
                
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
        date(2024, 11, 14),  # Diwali
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
            eligible_months = max(0, current_month - joining_date.month + 1)
            total_casual_leave = min(12, eligible_months)

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
                eligible_months = max(0, current_month - joining_date.month + 1)
                total_casual_leave = min(12, eligible_months)

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

        if not timesheet_ids:
            messages.error(request, "Please select at least one timesheet.")
            return redirect("manager_approve_timesheet")

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
    if request.method == 'POST':
        form = TimeSheetForm(request.POST)
        if form.is_valid():
            timesheet = form.save(commit=False)
            employee = Employee.objects.get(user=request.user)  # Associate with logged-in user
            timesheet.employee = employee
            timesheet.save()
            return redirect('add_time_sheet')
        else:
            print(form.errors)  # Debugging form errors
    else:
        form = TimeSheetForm()
    
    # Filter timesheets by logged-in user
    timesheet = TimeSheet.objects.filter(employee__user=request.user)
    return render(request, 'bluethinkincapp/add_time_sheet.html', {'form': form, 'timesheet': timesheet})


@login_required
def edit_time_sheet(request):
    if request.method == 'POST':
        time_sheet_id = request.POST.get('time_sheet_id')
        acknowledgment = request.POST.get('acknowledgment') == 'on'  # Get acknowledgment checkbox value

        try:
            timesheet = TimeSheet.objects.get(pk=time_sheet_id)
        except TimeSheet.DoesNotExist:
            return HttpResponseForbidden("Timesheet not found.")
        
        # Validate the logged-in user's access to this timesheet
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



