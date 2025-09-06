from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail

from django.db import models
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import Car
from orders.models import Order
from orders.utils import send_order_confirmation


# Create your views here.
def car_list(request):
    # Get unique values for filters
    makes = Car.objects.values_list('make', flat=True).distinct().order_by('make')
    body_types = Car.objects.values_list('body_type', flat=True).distinct().order_by('body_type')
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')
    down_pay = Car.objects.values_list('down_pay', flat=True).distinct().order_by('-down_pay')
    prices = Car.objects.values_list('sale_price', flat=True).distinct().order_by('-sale_price')
    mileage = Car.objects.values_list('mileage', flat=True).distinct().order_by('-mileage')
    context = {
        'makes': makes,
        'body_types': body_types,
        'years': years,
        'down_pay': down_pay,
        'prices': prices,
        'mileage': mileage,
    }
    return render(request, 'cars.html', context)


def car_list_ajax(request):
    # Get filter parameters from GET request
    makes = request.GET.getlist('make[]')
    body_types = request.GET.getlist('body_type[]')
    max_price = request.GET.get('max_price')
    max_mileage = request.GET.get('max_mileage')
    year = request.GET.getlist('year[]')
    monthly_installment = request.GET.get('monthly_installment')
    sort = request.GET.get('sort', 'recent')

    cars = Car.objects.all()

    # Apply filters
    if makes:
        # case-insensitive matching for makes
        cars = cars.filter(make__in=[m.lower() for m in makes])
        cars = cars.annotate(make_lower=models.functions.Lower('make')).filter(make_lower__in=[m.lower() for m in makes])

    if body_types:
        # case-insensitive matching for body types
        cars = cars.annotate(body_type_lower=models.functions.Lower('body_type')).filter(body_type_lower__in=[b.lower() for b in body_types])

    if max_price:
        cars = cars.filter(sale_price__lte=max_price)
    if max_mileage:
        cars = cars.filter(mileage__lte=max_mileage)
    if year:
        cars = cars.filter(year__in=year)
    if monthly_installment:
        cars = cars.filter(down_pay__lte=monthly_installment)

    # Apply sorting
    if sort == 'recent':
        cars = cars.order_by('-created_at')
    elif sort == 'model':
        cars = cars.order_by('-year')
    elif sort == 'lowest_price':
        cars = cars.order_by('sale_price')
    elif sort == 'highest_price':
        cars = cars.order_by('-sale_price')
    elif sort == 'mileage':
        cars = cars.order_by('mileage')

    context = {'cars': cars}
    return render(request, 'car_list.html', context)



def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    reopen_form = False

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        address = (request.POST.get("address") or "").strip()

        errors = []
        if not name: errors.append("A name is required.")
        if not email: errors.append("An email is required.")
        if not phone: errors.append("A phone number is required.")
        if not address: errors.append("An address is required.")

        if errors:
            for e in errors:
                messages.error(request, e)
            reopen_form = True
        else:
            order = Order.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                car=car,
                car_name=car.name,
                car_price=car.sale_price,
                car_model=car.model,
                car_year=car.year,
                stock_number=car.stock_no,
            )

            # Send email to customer AND yourself
            send_order_confirmation(order)

            messages.success(request, "Your order has been placed. We’ll contact you shortly.")
            return redirect(reverse('orders:success') + f"?name={name}")

    context = {'car': car, 'reopen_form': reopen_form}
    return render(request, "car_detail.html", context)


def toggle_wishlist(request):
    car_id = request.GET.get('car_id')
    wishlist = request.session.get('wishlist', [])

    if car_id:
        # Toggle the car in wishlist
        if car_id in wishlist:
            wishlist.remove(car_id)
            in_wishlist = False
        else:
            wishlist.append(car_id)
            in_wishlist = True

        request.session['wishlist'] = wishlist
        request.session.modified = True

        return JsonResponse({'success': True, 'in_wishlist': in_wishlist})
    else:
        # No car_id provided => return current wishlist
        return JsonResponse({'success': True, 'wishlist': wishlist})


def wishlist_view(request):
    wishlist_ids = request.session.get('wishlist', [])
    cars = Car.objects.filter(id__in=wishlist_ids)
    return render(request, 'wishlist.html', {'cars': cars})
