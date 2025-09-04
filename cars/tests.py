from django.test import TestCase

# Create your tests here.
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
