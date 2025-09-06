from cars import views
from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('success/', views.success, name='success'),
    path("book-test-drive/", views.book_test_drive, name="book_test_drive"),

]