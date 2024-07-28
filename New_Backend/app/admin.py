# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import InvitationEmails, Payments, RideOrder, User, Vehicle

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "is_active",
        "is_superuser",
        "created_at",
        "modified_at",
    )
    ordering = (
        "-is_superuser",
        "-created_at",
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)


@admin.register(InvitationEmails)
class InvitationEmailsAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")


@admin.register(RideOrder)
class RideOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
