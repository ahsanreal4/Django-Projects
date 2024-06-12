from rest_framework.permissions import BasePermission
from .constants import Constants

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name=Constants.MANAGER).exists()

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name=Constants.DELIVERY_CREW).exists()

class IsManagerOrDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.groups.filter(name=Constants.MANAGER).exists() or request.user.groups.filter(name=Constants.DELIVERY_CREW).exists())
