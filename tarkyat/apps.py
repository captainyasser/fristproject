from django.apps import AppConfig

class TarkyatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tarkyat'

    def ready(self):
        import tarkyat.signals  # استيراد الإشارات عند تحميل التطبيق