from cars import views
from django.urls import path

app_name = 'cars'
urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('ajax/cars/', views.car_list_ajax, name='car_list_ajax'),
    path('my-favourites/', views.wishlist_view, name="wishlist"),
    path('ajax/toggle-wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('<slug:slug>/', views.car_detail, name='car_detail'),
]