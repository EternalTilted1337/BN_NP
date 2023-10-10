from django.apps import AppConfig
class BdNpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BD_NP'
    def ready(self):
        import BD_NP.signals

# class AppointmentConfig(AppConfig):
#     name = 'appointment'
#
#     # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
#     def ready(self):
#         import appointment.signals


class AppointmentConfig(AppConfig):
    name = 'BD_NP'

    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import BD_NP.signals