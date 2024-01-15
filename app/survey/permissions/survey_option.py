from rest_framework import permissions

from survey.models import Survey


class IsOwnerOrReadOnlyOption(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            print(321312312)
            return True
        print(321312312)
        return obj.survey.user == request.user


class IsCreatorOfSurvey(permissions.BasePermission):
    message = "You are not the creator of this survey."

    def has_permission(self, request, view):
        survey_id = request.data.get('survey')
        print(survey_id)
        if not survey_id:
            return False

        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return False

        return request.user == survey.user
