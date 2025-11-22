from rest_framework import permissions



class IsParticipant(permissions.BasePermission):
    '''
    Allow access only if the request user is part of the conversation
    Only authenticated users can access the API
    '''

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # Only participant can run data retrieval/modification request
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS + ['PUT', 'PATCH', 'DELETE']:
            return request.user in obj.conversation.participants.all()