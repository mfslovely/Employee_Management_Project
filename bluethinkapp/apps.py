from django.apps import AppConfig



class BluethinkappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bluethinkapp'

    def ready(self):
        import bluethinkapp.signals


     
