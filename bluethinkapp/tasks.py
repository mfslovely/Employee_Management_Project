from celery import shared_task
from django.utils.timezone import now
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Employee

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
