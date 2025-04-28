from django.shortcuts import render
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import viewsets, mixins, response
from rest_framework import status as s

from .permission import IsAllowedToEditAttachmentElseNone, IsAllowedToEditTaskElseNone, IsAllowedToEditTaskListElseNone

from .serializers import AttachmentSerializers, TaskListSerializers, TaskSerializers

from .models import Attachment, Task, TaskList, COMPLETE, NOT_COMPLETE


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        queryset = super(TaskViewset, self).get_queryset()
        user_profile = self.request.user.profile
        updated_queryset = queryset.filter(created_by=user_profile)
        return updated_queryset

    @action(detail=True, methods=["patch"])
    def update_task_status(self, request, pk=None):
        task = self.get_object()
        profile = request.user.profile
        status = request.data.get("status")

        try:
            if(status == NOT_COMPLETE):
                if(task.status == COMPLETE):
                    task.status = NOT_COMPLETE
                    task.completed_by = None
                    task.completed_on = None
                else:
                    raise Exception("Task is already not complete")
            elif (status == COMPLETE):
                if(task.status == NOT_COMPLETE):
                    task.status = COMPLETE
                    task.completed_by = profile
                    task.completed_on = timezone.now()
                else:
                    raise Exception("Task is already complete")
            else:
                raise Exception("Invalid Status")

            task.save()
            serializer = TaskSerializers(instance=task, context={"request": request})
            return response.Response(serializer.data, status=s.HTTP_200_OK)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=s.HTTP_400_BAD_REQUEST)


class AttachmentViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializers
    permission_classes = [
        IsAllowedToEditAttachmentElseNone,
    ]
