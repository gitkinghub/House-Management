from django.shortcuts import render
from rest_framework import viewsets, mixins

from .permission import IsAllowedToEditAttachmentElseNone, IsAllowedToEditTaskElseNone, IsAllowedToEditTaskListElseNone

from .serializers import AttachmentSerializers, TaskListSerializers, TaskSerializers

from .models import Attachment, Task, TaskList


class TaskListViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializers
    permission_classes = [IsAllowedToEditTaskListElseNone, ]

class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    permission_classes = [
        IsAllowedToEditTaskElseNone,
    ]

    def get_queryset(self):
        queryset = super(TaskViewset, self).get_queryset()
        user_profile = self.request.user.profile
        updated_queryset = queryset.filter(created_by=user_profile)
        return updated_queryset

class AttachmentViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializers
    permission_classes = [
        IsAllowedToEditAttachmentElseNone,
    ]
