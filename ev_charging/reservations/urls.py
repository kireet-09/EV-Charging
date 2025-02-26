
from django.urls import path
from .views import  home, login_user, signup_user
from .views import reservation, reservation_success, cancel_reservation
from .views import my_reservations
from django.contrib.auth import views as auth_views
from .views import station_map
from .views import dummy_payment
from .views import announcements

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('signup/', signup_user, name='signup'),
    path('reservation/', reservation, name='reservation'),
    path('reservation/success/<int:reservation_id>/', reservation_success, name='reservation_success'),
    path('my-reservations/', my_reservations, name='my_reservations'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # ✅ Add logout route
    path('cancel-reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
    path('stations/', station_map, name='stations'),
    path("dummy-payment/<int:reservation_id>/", dummy_payment, name="dummy_payment"),
     path('announcements/', announcements, name='announcements'),
]