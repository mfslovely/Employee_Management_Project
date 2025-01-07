from django.contrib import admin
from django.contrib import admin
from .models import Employee, Claim,TimeSheet,Project,Leave
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'user')
    search_fields = ('first_name', 'last_name', 'user__username')
    list_filter = ('user',)

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'category', 'amount', 'status', 'last_action')
    search_fields = ('employee__first_name', 'employee__last_name', 'category')
    list_filter = ( 'date_from', 'date_to')
    date_hierarchy = 'last_action'

@admin.register(TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'date', 'hours', 'status', )
    search_fields = ('employee__first_name', 'employee__last_name', 'date')
    list_filter = ( 'date', 'status')
    
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'project_type', 'start_date', 'end_date', 'status','vendor_name')
    search_fields = ('project_name', 'description')
    list_filter = ( 'start_date', 'end_date', 'status')
    date_hierarchy = 'start_date'


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'leave_type', 'start_date', 'end_date', 'status', 'reason')
    search_fields = ('employee__first_name', 'employee__last_name', 'leave_type')
    list_filter = ( 'start_date', 'end_date', 'status')
    


    