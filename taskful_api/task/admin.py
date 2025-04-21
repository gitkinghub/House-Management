from django.contrib import admin

from .models import Attachment, Task, TaskList

admin.site.register(Task)
admin.site.register(Attachment)
admin.site.register(TaskList)
