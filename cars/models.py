from django.db import models
from django.utils.timezone import now
import random
import string
from django.utils.text import slugify
from django.core.files.base import ContentFile
import os

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

    def duplicate(self):
        """
        Creates a full duplicate of this car instance, including all fields,
        main_image, and all related CarImage objects.
        """
        # Generate a new unique stock number
        new_stock_no = 'REF' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        # Generate a new slug based on name and stock_no
        new_slug = slugify(f"{self.name}-{new_stock_no}")

        # Duplicate main_image content if it exists
        main_image_file = None
        if self.main_image:
            self.main_image.open()
            main_image_content = self.main_image.read()
            main_image_name = os.path.basename(self.main_image.name)
            main_image_file = ContentFile(main_image_content, name=main_image_name)

        # Create duplicate car with all fields
        duplicate_car = Car.objects.create(
            name=self.name,
            slug=new_slug,
            stock_no=new_stock_no,
            make=self.make,
            model=self.model,
            year=self.year,
            sale_price=self.sale_price,
            full_price=getattr(self, 'full_price', None),
            down_pay=self.down_pay,
            mileage=self.mileage,
            transmission=self.transmission,
            fuel=self.fuel,
            warranty=self.warranty,
            spec=self.spec,
            cylinders=self.cylinders,
            body_type=self.body_type,
            about=self.about,
            key_features=self.key_features,
            main_image=main_image_file,
            available=self.available
        )

        # Duplicate all related CarImage objects
        for img in self.gallery_images.all():  # adjust related_name if needed
            if img.image:
                img.image.open()
                img_content = img.image.read()
                img_name = os.path.basename(img.image.name)
                duplicate_car.gallery_images.create(
                    image=ContentFile(img_content, name=img_name)
                )

        return duplicate_car

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="cars/gallery/")

    def __str__(self):
        return f"Image for {self.car.make} {self.car.model}"
