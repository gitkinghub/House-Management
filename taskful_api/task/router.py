from rest_framework import routers

from .views import AttachmentViewset, TaskListViewset, TaskViewset

app_name = 'task'

router =routers.DefaultRouter()
router.register("tasklists", TaskListViewset)
router.register("tasks", TaskViewset)
router.register("attachments", AttachmentViewset)
