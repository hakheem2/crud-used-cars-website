from django.shortcuts import get_object_or_404, render
from .models import Car
from django.http import JsonResponse

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
        cars = cars.filter(make__in=makes)
    if body_types:
        cars = cars.filter(body_type__in=body_types)
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
    print('true')
    return render(request, 'car_list.html', context)

def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    return render(request, "car_detail.html", {"car": car})

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


