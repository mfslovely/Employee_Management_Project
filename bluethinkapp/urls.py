from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ApplyLeaveView,MangerLeaveView,MangerTimesheetView


urlpatterns = [ 
    path('deshboard/', views.dashboard,name = 'dashboard'),
    path('employee_register/', views.employee_register,name='employee_register'),
    path('', views.employee_login,name='employee_login'),
    path('my-profile/', views.employee_profile, name='employee_profile'),
    path('logout-for-the-day/', views.logout_for_the_day, name='logout_for_the_day'),
    path('claims/', views.claims, name='claims'),
    path('leave-list',views.leave_list, name='leave_list'),
    path('apply_leave/', ApplyLeaveView.as_view(), name='apply_leave'),
    path('manage_leave/', MangerLeaveView.as_view(), name='approve_leave'),
    path('check-login/', views.some_view, name='check-login'),
    path('timesheet/',views.add_time_sheet, name='add_time_sheet'),
    path('edit-timesheet/', views.edit_time_sheet, name='edit_time_sheet'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('director/dashboard/', views.director_dashboard, name='director_dashboard'),
    path('hr/dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('add-project/', views.add_project, name='add_project'),
    path('approve-timesheet/',MangerTimesheetView.as_view(), name='manager_approve_timesheet'),
    path('manage_holidays/', views.manage_holidays, name='manage_holidays'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('assign-device/', views.assign_device, name='assign_device'),
    path('assign-project/',views.manage_assign_projects, name='manage_assign_projects'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


