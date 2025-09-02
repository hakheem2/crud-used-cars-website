from django.shortcuts import render
# Create your views here.
def success(request):
    name = request.GET.get("name", "Customer")
    return render(request, "orders/success.html", {"order_name": name})