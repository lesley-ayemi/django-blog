from django.apps import AppConfig


class MarketingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketing'
    def ready(self):
        # print(">DEBUG::loading_signals")
        import marketing.signals
