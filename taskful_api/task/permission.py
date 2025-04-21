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
        return request.user.profile == obj.created_by

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
