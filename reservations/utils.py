from datetime import datetime, timedelta
from .models import Reservation, Table


def get_table_for_reservation(restaurant, date_time, people):

    time_lower = date_time - timedelta(hours=2)
    time_upper = date_time + timedelta(hours=2)

    print(time_lower, time_upper, 'here', people)

    clashing_reservations = Reservation.objects.filter(
        datetime__gt=time_lower, datetime__lt=time_upper, restaurant=restaurant, people__gte=people-2, people__lte=people+2)

    suitable_tables = Table.objects.filter(
        capacity__gte=people, capacity__lte=people+2)

    free_tables = set()
    for table in suitable_tables:
        free_tables.add(table)
    for reservation in clashing_reservations:
        free_tables.discard(reservation.table)

    if len(free_tables) == 0:
        return -1

    free_table = free_tables.pop()
    return free_table
