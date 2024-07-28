from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, AuthenticationFailed):
        response = Response(
            {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "error",
                "message": "unauthorized",
            },
        )
    return response
