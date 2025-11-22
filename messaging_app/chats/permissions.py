from rest_framework.permissions import BasePermission


class IsParticipant(BasePermission):
    '''
    Allow access only if the request user is part of the conversation
    '''

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participant.all()