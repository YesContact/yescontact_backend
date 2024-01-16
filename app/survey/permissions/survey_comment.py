from rest_framework import permissions

from survey.models import Comment

class IsOwnerOrReadOnlyComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.survey.user == request.user
    
class IsWriterOfComment(permissions.BasePermission):
    def has_permission(self, request, view):
        comment_id = request.data.get('comment')
        if not comment_id:
            return False

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return False

        return request.user == comment.user