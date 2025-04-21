from rest_framework import permissions

class IsAllowedToEditTaskListElseNone(permissions.BasePermission):
    """ Permission to allow only creator of tasklist to edit it"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_anonymous:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # For editing operations, only the creator can edit
        if request.method not in permissions.SAFE_METHODS:
            return request.user.profile == obj.created_by

        # For read operations, allow if user is a member of the house
        # Check if the user's profile is in the house's members list
        return request.user.profile in obj.house.members.all()

class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    """Permission to allow members of a house to access it"""
    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
        #     return request.user.is_authenticated  # allow all reads if logged in

        if not request.user.is_anonymous:
            return request.user.profile.house is not None

        return False

    def has_object_permission(self, request, view, obj):
        return request.user.profile.house == obj.task_list.house

class IsAllowedToEditAttachmentElseNone(permissions.BasePermission):
    """Permission to allow members of a house to access it"""
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.profile.house is not None

        return False

    def has_object_permission(self, request, view, obj):
        return request.user.profile.house == obj.task.task_list.house
