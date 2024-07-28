from django.contrib.auth.models import (
    AbstractBaseUser,
    Group,
    Permission,
    PermissionsMixin,
)
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.utils import timezone

from .managers import UserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    ROLE = (
        ("driver", "driver"),
        ("customer", "customer"),
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    role = models.CharField(max_length=100, choices=ROLE, default="customer")
    refresh_token = models.TextField(blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone_number"]

    def __str__(self):
        return f"{self.username} - {self.email}"

    def has_perm(self, perm, obj=None):
        if self.is_admin:
            return True
        # For users with is_staff, check specific permissions
        if self.is_staff:
            # Specify the permissions that users with is_staff should have
            if perm.startswith("view_"):
                return True

        # Default behavior for other users
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_admin:
            return True
        # For users with is_staff, check if they have any permissions in the specified module (app_label)
        if self.is_staff:
            # Retrieve the 'staff' group and check its permissions for the specified module
            staff_group = Group.objects.get(name="staff")
            allowed_permissions = staff_group.permissions.filter(
                content_type__app_label=app_label
            ).exists()
            return allowed_permissions

        # Default behavior for other users
        return False


class Vehicle(models.Model):
    CATEGORY = (
        ("mini", "mini"),
        ("suv", "suv"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=225, blank=True, null=True)
    year = models.CharField(max_length=225, blank=True, null=True)
    category = models.CharField(max_length=225, choices=CATEGORY, default="mini")
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"


class RideOrder(models.Model):
    STATUS = (
        ("pending", "pending"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
        ("in_progress", "in_progress"),
        ("completed", "completed"),
    )
    user = models.ForeignKey(User, related_name="order_user", on_delete=models.CASCADE)
    driver = models.ForeignKey(
        User, related_name="order_driver", on_delete=models.CASCADE
    )
    departure = models.CharField(max_length=225, blank=True, null=True)
    destination = models.CharField(max_length=225, blank=True, null=True)
    distance = models.CharField(max_length=225, blank=True, null=True)
    status = models.CharField(max_length=225, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"


class Payments(models.Model):
    user = models.ForeignKey(
        User, related_name="user_payment", on_delete=models.SET_NULL, null=True
    )
    driver = models.ForeignKey(
        User, related_name="driver_payment", on_delete=models.SET_NULL, null=True
    )
    order = models.ForeignKey(RideOrder, on_delete=models.SET_NULL, null=True)
    total_price = models.FloatField(default=0.0)
    extra = models.FloatField(default=0.0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"


class InvitationEmails(models.Model):
    ROLE = (
        ("driver", "driver"),
        ("customer", "customer"),
    )
    name = models.CharField(max_length=225, blank=True, null=True)
    email = models.CharField(max_length=225, blank=True, null=True, unique=True)
    role = models.CharField(max_length=100, choices=ROLE, default="customer")
    is_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    sender = models.ForeignKey(
        User, related_name="noti_sender", on_delete=models.SET_NULL, null=True
    )
    receiver = models.ForeignKey(
        User, related_name="noti_receiver", on_delete=models.SET_NULL, null=True
    )
    order = models.ForeignKey(RideOrder, on_delete=models.SET_NULL, null=True)
    message_sender = models.TextField(blank=True, null=True)
    message_receiver = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender}   -------    {self.receiver}"
