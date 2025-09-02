from cars import views
from django.urls import path
from .views import success

app_name = 'orders'
urlpatterns = [
    path('success/', success, name='success'),
]