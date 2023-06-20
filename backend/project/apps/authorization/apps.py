from django.apps import AppConfig


class AuthorizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project.apps.authorization'

    verbose_name = "Регистрация и авторизация"

    def ready(self):
        from .signals import change_type_user, delete_coach
        _ = [change_type_user, delete_coach]
