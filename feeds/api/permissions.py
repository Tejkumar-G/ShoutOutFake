import json

from rest_framework import permissions


class IsAdminOrReadonly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method == 'GET' or admin_permission


class IsIndividualUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            if request.user.is_anonymous:
                return False
            try:
                if request.user.uid == request.data['creatorId']:
                    return True
            except KeyError:
                request.data['creatorId'] = request.user.uid

            return request.user.uid == request.data['creatorId']

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            if request.user.is_anonymous:
                return False
            return request.user.uid == request.data['fromId']
        elif request.method == 'PUT':
            if request.user.is_anonymous:
                return False
            return request.user.uid == request.data['fromId'] == obj.fromId.uid
        return request.user.uid == obj.fromId.uid


class AcceptOrDeclineChallengeIfSameUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT':
            if request.user.is_anonymous:
                return False
            if request.user.uid == obj.userId.uid:
                if request.query_params.get('status').lower() == 'accept':
                    request.data['status'] = 'Accept'
                else:
                    request.data['status'] = 'Decline'
                request.data['creatorId'] = request.user.uid
                request.data['challengeId'] = obj.challengeId.id
                request.data['attachments'] = obj.attachments
                request.data['note'] = obj.note
            return request.user.uid == obj.userId.uid


