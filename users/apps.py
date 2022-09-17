from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # CONNECTS SIGNALS.PY TO APP
    def ready(self):
        import users.signals  