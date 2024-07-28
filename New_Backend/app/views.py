import base64
import json
import logging
import random
import re
from datetime import timedelta

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from flask_jwt_extended import create_access_token
from geopy.distance import geodesic
from jose import jwt
from rest_framework import status
from rest_framework.decorators import throttle_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rideshare import settings

# from .api.permissions import CustomIsAuthenticated
from .models import *
from .models import InvitationEmails
from .serializer import *
from .serializer import LoginSerializer
from .token import generate_token
from .utils import send_email_verification

User = get_user_model()
# Create your views here.

# Create your views here.


def index(request):
    if request.user.is_superuser:
        if request.method == "POST":
            email = request.POST.get("email")
            if InvitationEmails.objects.filter(email=email).exists():
                pass
            else:
                send_email_verification(request, email)
                InvitationEmails.objects.create(
                    email=request.POST.get("email"),
                    name=request.POST.get("name"),
                    role=request.POST.get("role"),
                )

        pending_users = InvitationEmails.objects.filter(is_registered=False)
        context = {
            "pending_users": pending_users,
        }
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")


def register(request):
    try:

        inv_id = request.POST.get("inv_id", None)
        inv_obj = InvitationEmails.objects.get(id=inv_id)
        email = inv_obj.email
        phone_number = request.POST.get("phone_number", None)
        name = request.POST.get("name", None)
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        role = inv_obj.role
        if email and username:
            if User.objects.filter(username=username).exists():
                return render(request, "404.html", {"error": "Username already taken"})

            if User.objects.filter(email=email).exists():
                return render(request, "404.html", {"error": "email already taken"})
        if email and phone_number and name and username and password and role:
            user = User.objects.create_user(
                email=email,
                name=name,
                password=password,
                username=username,
                role=role,
                phone_number=phone_number,
            )

            refresh = RefreshToken.for_user(user)
            user.refresh_token = str(refresh)
            user.access_token = str(refresh.access_token)
            user.is_active = True
            user.save()

            inv_obj = InvitationEmails.objects.get(email=user.email)
            inv_obj.is_registered = True
            inv_obj.save()

            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "token": str(user.refresh_token),
                "refresh_token": str(user.access_token),
            }
            return render(
                request, "404.html", {"error": "Account Created Successfully"}
            )
        else:
            return render(
                request,
                "404.html",
                {
                    "error": "Please fill all the information to create account, ask for invite"
                },
            )
    except Exception as e:
        print(e)
        return render(
            request,
            "404.html",
            {"error": "Internal Server error"},
        )


class LoginView(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get("username", None)
            password = data.get("password", None)
            if username in ["", None] or password in ["", None]:
                return Response(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "status": "error",
                        "message": "Username and password is required",
                    }
                )

            serializer = LoginSerializer(
                data=request.data, context={"request": request}
            )

            if serializer.is_valid():

                user = serializer.validated_data.get("user")

                refresh = RefreshToken.for_user(user)
                user.refresh_token = str(refresh)
                user.access_token = str(refresh.access_token)
                user.save()
                data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "is_superuser": user.is_superuser,
                    "token": str(user.access_token),
                    "refresh_token": str(user.refresh_token),
                }

                return Response(
                    {
                        "code": status.HTTP_201_CREATED,
                        "status": "success",
                        "message": "Login successful! Enjoy your experience",
                        "data": data,
                    }
                )

            else:
                message = "Your account is inactive, Please check your email, Contact us for help."
                if serializer.errors.get("non_field_errors")[0] != message:
                    message = "Invalid credentials"
                return Response(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "status": "error",
                        "message": message,
                    }
                )
        except Exception as e:
            print(f"There is something wrong in LoginView: {e}")
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "message": "Internal server error",
                }
            )


def activate_account(request, uidb64, token):
    try:
        email = force_str(urlsafe_base64_decode(uidb64))
        is_valid_user = InvitationEmails.objects.filter(email=email).exists()
    except Exception as e:
        is_valid_user = False
    if is_valid_user is not None and generate_token.check_token(email, token):
        inv = InvitationEmails.objects.get(email=email)
        context = {"inv": inv}
        messages.success(
            request, "Your Account has been activated. Please try to login!"
        )
        return render(request, "register.html", context)
    else:
        messages.error(request, "Could not verify the email, Try again")
        return render(request, "404.html")


class UserDashboardView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cars = Vehicle.objects.filter(is_booked=False)
        serializer = VehicleSerializer(cars, many=True)
        try:
            return Response(
                {
                    "code": status.HTTP_201_CREATED,
                    "status": "success",
                    "message": "User Dashboard Api is working fine",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "message": "Internal server error",
                }
            )


class OrderRideView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data.get("username", None)
        driver = User.objects.get(username=username)
        vehicle = Vehicle.objects.get(user=driver)
        serializer = VehicleSerializer(vehicle)
        try:
            return Response(
                {
                    "code": status.HTTP_201_CREATED,
                    "status": "success",
                    "message": "Please add address information to book this ride",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "message": "Internal server error",
                }
            )


class BookRideView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            driver = User.objects.get(username=data["order_data"]["user"]["username"])

            coordinates = data.get("coordinates")

            if coordinates:
                departure = coordinates.get("departure", {})
                destination = coordinates.get("destination", {})
                if not departure or not destination:
                    return Response(
                        {
                            "code": status.HTTP_400_BAD_REQUEST,
                            "status": "error",
                            "message": "Please select from and to coordinate points",
                        }
                    )
                departure_point = (departure["lat"], departure["lng"])
                destination_point = (destination["lat"], destination["lng"])
                distance = geodesic(departure_point, destination_point).kilometers
                total_price = 20 + (float(distance) * 1.5)
                total_price = round(total_price, 2)

                order = RideOrder.objects.create(
                    user=request.user,
                    driver=driver,
                    departure=departure_point,
                    destination=destination_point,
                    status="pending",
                    distance=distance,
                )
            else:
                totalDistance = data.get("totalDistance")
                order = RideOrder.objects.create(
                    user=request.user,
                    driver=driver,
                    departure=data["departure"],
                    destination=data["destination"],
                    status="pending",
                    distance=totalDistance,
                )
                total_price = 20 + (float(totalDistance) * 1.5)
                total_price = round(total_price, 2)
            payment = Payments.objects.create(
                user=request.user,
                driver=driver,
                order=order,
                total_price=total_price,
            )
            Notification.objects.create(
                sender=request.user,
                receiver=driver,
                order=order,
                message_sender=f"Your request for ride is sent",
                message_receiver=f"{request.user.username} send request for ride from {order.departure} to {order.destination} for {payment.total_price}, Are you ready?",
            )
            return Response(
                {
                    "code": status.HTTP_201_CREATED,
                    "status": "success",
                    "message": "Order for ride is placed, wait for driver to accept",
                }
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "message": "Internal server error",
                }
            )


class NotificationView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            as_sender = Notification.objects.filter(sender=request.user, is_read=False)
            as_receiver = Notification.objects.filter(
                receiver=request.user, is_read=False
            )
            serializer1 = NotificationSerializer(as_sender, many=True)
            serializer2 = NotificationSerializer(as_receiver, many=True)
            return Response(
                {
                    "code": status.HTTP_201_CREATED,
                    "status": "success",
                    "message": "Order for ride is placed, wait for driver to accept",
                    "data": {
                        "noti_as_sender": serializer1.data,
                        "noti_as_receiver": serializer2.data,
                    },
                }
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "message": "Internal server error",
                }
            )


class AcceptOrderView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            order_id = data.get("order_id")
            is_accepted = data.get("is_accepted")
            order = RideOrder.objects.get(id=order_id)

            if is_accepted:
                order.status = "accepted"
                order.save()
                Notification.objects.create(
                    sender=request.user,
                    receiver=order.user,
                    order=order,
                    message_sender=f"Order is accepted",
                    message_receiver=f"Your order is accept, Your ride is coming soon",
                )
            else:
                order.status = "rejected"
                order.save()
                Notification.objects.create(
                    sender=request.user,
                    receiver=order.user,
                    order=order,
                    message_sender=f"Order is rejected",
                    message_receiver=f"Your order is rejected.",
                )
            return Response(
                {
                    "code": status.HTTP_201_CREATED,
                    "status": "success",
                    "message": "Order for ride is placed, wait for driver to accept",
                }
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "message": "Internal server error",
                }
            )


class MarkNotiView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            noti_id = data.get("noti_id")
            noti = Notification.objects.get(id=noti_id)
            noti.is_read = True
            noti.save()
            return Response(
                {
                    "code": status.HTTP_201_CREATED,
                    "status": "success",
                    "message": "Notification mark as read",
                }
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "message": "Internal server error",
                }
            )


class LogOutView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:

            print("jereere")
            token = RefreshToken(request.user.refresh_token)
            token.blacklist()
            request.user.refresh_token = ""
            request.user.access_token = ""
            request.user.save()
            return Response(
                {
                    "code": status.HTTP_200_OK,
                    "status": "success",
                    "message": "Logout successfully",
                }
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "message": "Internal server error",
                }
            )


class PaymentView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            order_id = data.get("order_id")
            pay_id = data.get("pay_id")

            order = RideOrder.objects.get(id=order_id)
            order.status = "completed"
            order.save()
            pay = Payments.objects.get(id=pay_id)
            pay.is_paid = True
            pay.save()
            return Response(
                {
                    "code": status.HTTP_200_OK,
                    "status": "success",
                    "message": "Payment Successful",
                }
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "message": "Internal server error",
                }
            )

    def get(self, request, *args, **kwargs):
        try:
            pays = Payments.objects.filter(user=request.user, is_paid=False)
            serializer = PaySerializer(pays, many=True)
            return Response(
                {
                    "code": status.HTTP_200_OK,
                    "status": "success",
                    "message": "Payment Retrieved",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "message": "Internal server error",
                }
            )
