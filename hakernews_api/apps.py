from django.apps import AppConfig


class HakernewsApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hakernews_api"

    def ready(self):
        print("starting scheduler............")
        from . import scheduler

        scheduler.start()
