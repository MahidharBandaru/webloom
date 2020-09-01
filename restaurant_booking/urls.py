from django.contrib import admin
from django.urls import path, include
from reservations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/restaurants', views.RestaurantList.as_view()),
    path('api/restaurants/<int:pk>',
         views.RestaurantUpdateRetrieveDelete.as_view()),

    path('api/restaurants/<int:restaurant_id>/tables',
         views.TablesListCreate.as_view()),
    path('api/restaurants/<int:restaurant_id>/tables/<int:pk>',
         views.TableUpdateRetrieveDelete.as_view()),

    path('api/reservations',
         views.ReservationListCreate.as_view()),
    path('api/reservations/<int:pk>',
         views.ReservationRetrieveDelete.as_view()),

    path('api/restaurants/<int:restaurant_id>/reservation_slots',
         views.restaurant_reservation),
]
