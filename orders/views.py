from django.shortcuts import render
# Create your views here.
def success(request):
    name = request.GET.get("name", "Customer")
    return render(request, "orders/success.html", {"order_name": name})


import resend
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Car

resend.api_key = settings.RESEND_API_KEY


@require_POST
def book_test_drive(request):
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    date = request.POST.get("date")
    time = request.POST.get("time")
    car_id = request.POST.get("car_id")

    if not all([name, phone, date, time, car_id]):
        return JsonResponse({"status": "error", "message": "Missing required fields"}, status=400)

    car = get_object_or_404(Car, id=car_id)

    # Render email template
    html_content = render_to_string("orders/test-drive-email.html", {
        "car": car,
        "name": name,
        "phone": phone,
        "email": email,
        "date": date,
        "time": time,
    })

    # Send email via Resend
    try:
        resend.Emails.send({
            "from": "info@carsmaxautos.com",
            "to": ['info@carsmaxautos.com'],
            "subject": f"New Test Drive Booking - {car.name}",
            "html": html_content,
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "success"})
