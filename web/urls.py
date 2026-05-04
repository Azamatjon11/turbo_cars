from django.urls import path
from . import views

urlpatterns = [
    path('language/<str:language>/', views.set_language, name='set_language'),
    path('', views.index, name='index'),
    path('ContactUs/', views.contact, name='contact'),
    path('CarsInStock/', views.cars_in_stock, name='cars_in_stock'),
    path('CarAuctions/', views.auctions, name='auctions'),
    path('Logistics/', views.logistics, name='logistics'),
    path('Reviews/', views.reviews, name='reviews'),
    path('AboutUs/', views.about, name='about'),
    path('UsedCars/', views.used_cars, name='used_cars'),
    path('DamagedCars/', views.damaged_cars, name='damaged_cars'),
    path('NewCars/', views.new_cars, name='new_cars'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
]
