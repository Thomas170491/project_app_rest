from django.urls import path

from . import views
from .views import (
    AcceptOrderView,
    BookRideView,
    LoginView,
    LogOutView,
    MarkNotiView,
    NotificationView,
    OrderRideView,
    PaymentView,
    UserDashboardView,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", views.register, name="register"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("user-dashboard/", UserDashboardView.as_view(), name="user-dashboard"),
    path("order-ride/", OrderRideView.as_view(), name="order-ride"),
    path("book-ride/", BookRideView.as_view(), name="book-ride"),
    path("notification/", NotificationView.as_view(), name="notification"),
    path("accept-order/", AcceptOrderView.as_view(), name="accept-order"),
    path("mark-notification/", MarkNotiView.as_view(), name="mark-notification"),
    path("payment/", PaymentView.as_view(), name="payment"),
]
