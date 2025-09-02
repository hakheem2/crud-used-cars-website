from django.db import models
from cars.models import Car
from django.utils import timezone

class Order(models.Model):
    # --- USER INFO ---
    name = models.CharField(max_length=255)   # changed from full_name
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # --- CAR INFO ---
    order_id = models.CharField(max_length=50, unique=True, editable=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="orders")
    car_name = models.CharField(max_length=255)
    car_price = models.DecimalField(max_digits=10, decimal_places=2)
    car_year = models.PositiveIntegerField()
    car_model = models.CharField(max_length=255)
    stock_number = models.CharField(max_length=100)

    # --- META ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            now = timezone.now()
            # Example format: ORD-20250902-174530
            self.order_id = now.strftime("ORD-%Y%m%d-%H%M%S")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} - {self.car_name}"