from rest_framework import serializers
from .models import Restaurant, Table, Reservation


class RestaurantSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number',
                  'opening_time', 'closing_time', 'owner_name']


class TableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Table
        fields = ['id',  'restaurant_name', 'capacity']


class ReservationSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='user.username')
    table_id = serializers.ReadOnlyField(source='table.id')

    class Meta:
        model = Reservation
        fields = ['id', 'created_by', 'restaurant',
                  'table_id', 'datetime', 'people']
