from django import forms
from .models import Employee,Claim,Leave

class AccountDetailsForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['bank_name', 'account_number', 'ifsc_code']

class CurrentAddressForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['current_street', 'current_city', 'current_state', 'current_country', 'current_pincode']

class PermanentAddressForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['permanent_street', 'permanent_city', 'permanent_state', 'permanent_country', 'permanent_pincode']

class FamilyDetailsForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['father_name', 'mother_name', 'spouse_name', 'contact_number']

class EducationDetailsForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['high_school', 'intermediate', 'graduation', 'post_graduation']

class CommunicationDetailsForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['mobile_number', 'company_email', 'internal_email', 'personal_email']

class DocumentSectionForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['profile_photo', 'aadhar_number', 'aadhar_doc', 'pan_number', 'pan_doc', 'offer_letter', 'relieving_letter', 'resignation_letter', 'appointment_letter', 'bank_statement', 'salary_slip1', 'salary_slip2', 'salary_slip3']

class PreviousEmploymentDetailsForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['previous_company_name', 'start_date', 'end_date', 'previous_role', 'reference_name', 'reference_email', 'reference_mobile', 'reference_role']


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['category', 'date_from', 'date_to', 'amount', 'description', 'claim_file','comment','approved_by','status']
        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date'}),
            'date_to': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg description-field'}),
         
        }



class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }