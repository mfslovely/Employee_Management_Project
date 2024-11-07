from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
 
    path('deshboard/', views.dashboard,name = 'dashboard'),
    path('employee_register/', views.employee_register,name='employee_register'),
    path('', views.employee_login,name='employee_login'),
    path('my-profile/', views.employee_profile, name='employee_profile'),
    path('logout-for-the-day/', views.logout_for_the_day, name='logout_for_the_day'),
    path('claims/', views.claims, name='claims'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


