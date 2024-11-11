from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Employee,WorkFromHome,Leave,BasicInformation,LoginLogoutHistory, Claim
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
    PreviousEmploymentDetailsForm,ClaimForm,ApplyLeaveForm
)






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


def employee_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        date_of_birth = request.POST.get('date_of_birth')
        date_of_joining = request.POST.get('date_of_joining')
        job_title = request.POST.get('job_title')
        hashed_password = make_password(password)
        user = User.objects.create(username=email, email=email, password=hashed_password)

        if not first_name or not last_name or not email or not password:
            messages.error(request, 'Please fill all the fields')
            return render(request, 'bluethinkincapp/employee_register.html')
        if Employee.objects.filter(email=email).exists():
            messages.error(request, 'An employee with this email already exists.')
            return render(request, 'bluethinkincapp/employee_register.html')

        employee = Employee.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password,date_of_birth = date_of_birth, date_of_joining=date_of_joining,job_title=job_title, user = user  )
        employee.save()
        messages.success(request,'Employee registered successfully')
        return redirect('employee_login')
    return render(request, 'bluethinkincapp/employee_register.html')



def employee_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Employee with this email does not exist')
            return render(request, 'bluethinkincapp/employee_login.html')
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Employee logged in successfully')
            return redirect('dashboard')  

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




@login_required
def claims(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.employee = request.user 
            claim.save()
            return redirect('claims')

    else:
        form = ClaimForm()  

   
    user_claims = Claim.objects.filter(employee__user=request.user)

    return render(request, 'bluethinkincapp/claims.html', {
        'form': form,           
        'user_claims': user_claims,  
    })


@login_required
def leave_list(request):
    leaves = Leave.objects.filter(employee__user=request.user)
    return render(request, 'bluethinkincapp/leave_management.html', {'leaves': leaves})


@login_required
class ApplyLeaveView(View):
    def get(self, request):
       
        available_leaves = {
            "casual": 10, 
            "leave_without_pay": 0,
            "manager_approval": 5
        }
        applied_leaves = Leave.objects.filter(employee__user=request.user)
        form = ApplyLeaveForm()

        context = {
            "available_leaves": available_leaves,
            "applied_leaves": applied_leaves,
            "form": form,
        }
        return render(request, "apply_leave.html", context)

    def post(self, request):
        form = ApplyLeaveForm(request.POST)
        if form.is_valid():
            leave_application = form.save(commit=False)
            leave_application.employee = request.user
            leave_application.status = 'pending'
            leave_application.save()
            return redirect('apply_leave')
        return render(request, "apply_leave.html", {"form": form})