from django.contrib import admin
from .models import Order
# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "name", "email", "car_name", "car_price", "created_at")
    list_filter = ("created_at", "car_year")
    search_fields = ("name", "email", "car_name", "stock_number")

    fieldsets = (
        ("User Info", {
            "fields": ("name", "email", "phone", "address")
        }),
        ("Car Info", {
            "fields": ("car", "car_name", "car_price", "car_year", "car_model", "stock_number")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("created_at", "updated_at")
