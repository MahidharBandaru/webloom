from rest_framework import permissions
from .models import Restaurant


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsRestaurantOwner(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        restaurant = Restaurant.objects.get(pk=view.kwargs['restaurant_id'])
        return restaurant.owner == request.user


class IsReservationByUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
