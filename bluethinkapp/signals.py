from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import LoginLogoutHistory

@receiver(user_logged_in)
def track_login(sender, user, request, **kwargs):
    
    history = LoginLogoutHistory.objects.create(user=user, login_time=timezone.now())
    history.save()

@receiver(user_logged_out)
def track_logout(sender, user, request, **kwargs):
    try:
        history = LoginLogoutHistory.objects.filter(user=user).latest('login_time')
        history.logout_time = timezone.now()
        history.save()
    except LoginLogoutHistory.DoesNotExist:
        pass


    




