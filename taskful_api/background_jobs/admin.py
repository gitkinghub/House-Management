from django.apps import AppConfig
from django.contrib import admin

# Register your models here.

class BackgroundJobsConfig(AppConfig):
    name = "background_jobs"

    def ready(self):
        import background_jobs.tasks