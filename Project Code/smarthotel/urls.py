"""smarthotel URL Configuration

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
from django.urls import path
from smarthotel import settings
from django.conf.urls.static import static
from hotel.views import *
from registration.views import *
from user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('user_registration/', userRegistration, name='userRegistration'),
    path('hotel_registration/', hotelRegistration, name='hotelRegistration'),
    path('hotel_home/', hotelHome, name='hotel_home'),
    path('hotel_add_room/', hotelAddRoom, name='hotel_add_room'),
    path('hotel_add_image/', hotelAddImage, name='hotel_add_image'),
    path('user_home/', userHome, name='user_home'),
    path('user_room_list/<str:hotelid>/<str:checkin>/<str:checkout>/', userRoomList, name='user_room_list'),
    path('user_view_room/<str:roomid>/<str:checkin>/<str:checkout>/', userViewRoom, name='user_view_room'),
    path('user_cancel_room/<str:roomid>/<str:checkin>/<str:checkout>/', userCancelRoom, name='user_cancel_room'),
    path('user_book_room/<str:roomid>/<str:checkin>/<str:checkout>/', userBookRoom, name='user_book_room'),
    path('user_history/', userHistory, name='user_history'),
    path('user_rating/<str:roomid>/', userRating, name='user_rating'),
    path('hotel_logout/', hotelLogout, name='hotel_logout'),
    path('user_logout/', userLogout, name='user_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
