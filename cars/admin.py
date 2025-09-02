from django.contrib import admin
from .models import Car, CarImage


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 2
    fields = ["image"]
    verbose_name = "Gallery Image"
    verbose_name_plural = "Gallery Images"


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name", "make", "model", "year", "stock_no", "sale_price", "available", "created_at")
    list_filter = ("make", "year", "transmission", "fuel", "body_type", "available")
    search_fields = ("name", "make", "model", "stock_no", "year")
    prepopulated_fields = {"slug": ("stock_no","name")}  # optional, save typing
    inlines = [CarImageInline]

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "make", "model", "year", "stock_no", "slug",)
        }),
        ("Pricing", {
            "fields": ("sale_price", "full_price", "down_pay")
        }),
        ("Specifications", {
            "fields": ("mileage", "transmission", "fuel", "warranty", "spec", "cylinders", "body_type")
        }),
        ("Media", {
            "fields": ("main_image",)
        }),
        ("Details", {
            "fields": ("about", "key_features")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "available",),
            "classes": ("collapse",),  # collapsible
        }),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ("car", "image")
