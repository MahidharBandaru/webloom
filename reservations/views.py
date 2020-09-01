from rest_framework import generics, permissions, mixins, status
from .models import Restaurant, Table, Reservation
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import RestaurantSerializer, TableSerializer, ReservationSerializer
from .permissions import IsOwnerOrReadOnly, IsRestaurantOwner, IsReservationByUser
from rest_framework.decorators import api_view, renderer_classes
from datetime import datetime, timedelta
from .utils import get_table_for_reservation

# Create your views here.


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantUpdateRetrieveDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class TablesListCreate(generics.ListCreateAPIView):
    serializer_class = TableSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsRestaurantOwner]

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        serializer.save(restaurant=restaurant)

    def get_queryset(self):
        restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        return Table.objects.filter(restaurant=restaurant)


class TableUpdateRetrieveDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        return Table.objects.filter(restaurant=restaurant)


class ReservationListCreate(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsReservationByUser]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(pk=self.request.data['restaurant'])
        query_datetime = datetime.strptime(
            self.request.data['datetime'], '%Y-%m-%dT%H:%M:%S')

        people = int(self.request.data['people'])
        free_table = get_table_for_reservation(
            restaurant, query_datetime, people)
        if free_table == -1:
            raise ValidationError(
                'Error: Sorry! We\'re completely booked for this time slot')
        serializer.save(user=self.request.user,
                        restaurant=restaurant, table=free_table)


class ReservationRetrieveDelete(generics.RetrieveDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsReservationByUser]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


@api_view(['GET'])
def restaurant_reservation(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        raise ValidationError('Error: Restaurant does not exist')

    people = request.query_params.get('people', '')
    year = request.query_params.get('year', '')
    month = request.query_params.get('month', '')
    day = request.query_params.get('day', '')

    if people == '' or year == '' or month == '' or day == '':
        raise ValidationError(
            'People, year, month, day required as url query parameters')

    try:
        year = int(year)
        month = int(month)
        day = int(day)
        query_date = datetime(year, month, day)
    except ValueError as e:
        raise ValidationError('Error: Invalid date')
    today = datetime.today()
    today = datetime(year=today.year, month=today.month, day=today.day)
    if query_date < today:
        raise ValidationError('Error: Date cannot be from past')

    free_slots = []

    restaurant_opening_time = restaurant.opening_time
    restaurant_closing_time = restaurant.closing_time
    start_datetime = datetime(
        year, month, day, hour=restaurant_opening_time.hour, minute=restaurant_opening_time.minute)
    end_datetime = datetime(
        year, month, day, hour=restaurant_closing_time.hour, minute=restaurant_closing_time.minute)
    if(start_datetime >= end_datetime):
        end_datetime = end_datetime + timedelta(days=1)

    curr_datetime = start_datetime
    try:
        people = int(people)
    except ValueError as e:
        raise ValidationError('Error: Invalid number of people')
    while(curr_datetime < end_datetime):
        free_table = get_table_for_reservation(restaurant,
                                               curr_datetime, people)
        if curr_datetime >= datetime.now() and free_table != -1:
            free_slots.append(curr_datetime)
        curr_datetime += timedelta(minutes=15)

    return Response({"reservation_slots": free_slots})
