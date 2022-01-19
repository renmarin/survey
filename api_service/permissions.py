from rest_framework import permissions
from .models import Question


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner.
        return obj.author == request.user


class IsOwnerParent(permissions.BasePermission):
    """
    Custom permission to only allow owners of an question to create new options.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        question = Question.objects.get(pk=view.kwargs["pk"])
        return question.author == request.user
