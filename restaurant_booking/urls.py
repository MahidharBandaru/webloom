"""zappit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reservations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('api/posts', views.PostList.as_view()),
    # path('api/posts/<int:pk>', views.PostRetrieveDelete.as_view()),
    # path('api/posts/<int:pk>/vote', views.VoteCreate.as_view()),
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
