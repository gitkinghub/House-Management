from rest_framework import serializers


from .models import House


class HouseSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(read_only=True)
    members  = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="profile-detail")
    manager = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name="profile-detail")
    taskLists = serializers.HyperlinkedRelatedField(
        read_only=True, many=True, view_name="tasklist-detail", source="lists"
    )

    class Meta:
        model = House
        fields = [
            "url",
            "id",
            "name",
            "image",
            "created_on",
            "description",
            "manager",
            "points",
            "completed_tasks_count",
            "not_completed_tasks_count",
            "members_count",
            "members",
            "taskLists",
        ]

        read_only_fields = ["points", "completed_tasks_count", "not_completed_tasks_count"]
