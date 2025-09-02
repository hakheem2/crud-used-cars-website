from django.shortcuts import get_object_or_404, render
from cars.models import Car

# Create your views here.
def home(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars': cars})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def terms(request):
    return render(request, 'terms.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')