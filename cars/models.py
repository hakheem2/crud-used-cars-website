from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
        ('semi-automatic', 'Semi-Automatic'),
    ]

    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]

    BODY_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('pickup', 'Pickup'),
        ('van', 'Van'),
        ('other', 'Other'),
    ]
    name = models.CharField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    stock_no = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)  # auto filled from save()
    available = models.BooleanField(default=True)

    sale_price = models.DecimalField(max_digits=12, decimal_places=0)
    full_price = models.DecimalField(max_digits=12, decimal_places=0)
    down_pay = models.DecimalField(max_digits=12, decimal_places=0)

    mileage = models.PositiveIntegerField()  # in kilometers or miles

    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES
    )

    fuel = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES
    )

    warranty = models.CharField(
        max_length=100,
        default="Under Warranty"
    )

    spec = models.CharField(
        max_length=100,
        default="GCC Specs"
    )

    cylinders = models.PositiveIntegerField()

    body_type = models.CharField(
        max_length=50,
        choices=BODY_TYPE_CHOICES
    )

    about = models.TextField(blank=True, null=True)

    key_features = models.TextField(
        help_text="Enter one feature per line."
    )

    main_image = models.ImageField(upload_to="cars/main/")

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.stock_no}-{self.name}")
        super().save(*args, **kwargs)

    def features_list(self):
        """
        Returns key features as a list (split by new lines)
        """
        return [f.strip() for f in self.key_features.splitlines() if f.strip()]

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="cars/gallery/")

    def __str__(self):
        return f"Image for {self.car.make} {self.car.model}"
