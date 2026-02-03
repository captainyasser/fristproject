from django.apps import AppConfig







class EmDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'em_data'

    def ready(self):
        import em_data.signals  # استيراد الإشارات