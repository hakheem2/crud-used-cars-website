from django.contrib import admin
from .models import Car, CarImage
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 2
    fields = ["image"]
    verbose_name = "Gallery Image"
    verbose_name_plural = "Gallery Images"


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name", "make", "model", "year", "stock_no", "sale_price", "available", "created_at", "duplicate_button")
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
        ("Details", {
            "fields": ("about", "key_features")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "available",),
            "classes": ("collapse",),  # collapsible
        }),
        ("Media", {
            "fields": ("main_image",)
        }),
    )
    readonly_fields = ("created_at", "updated_at")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:car_id>/duplicate/', self.admin_site.admin_view(self.duplicate_view), name='car-duplicate'),
        ]
        return custom_urls + urls

    def duplicate_view(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        car.duplicate()
        self.message_user(request, f'Car "{car.name}" duplicated successfully!')
        return redirect(request.META.get('HTTP_REFERER', '/admin/'))

    def duplicate_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Duplicate</a>',
            f"{obj.id}/duplicate/"
        )
    duplicate_button.short_description = 'Duplicate Car'


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ("car", "image")
