from django.apps import AppConfig


class KuccConfig(AppConfig):
    name = 'org'


    def ready(self):
        import users.signals
