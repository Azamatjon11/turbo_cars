from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Car, Review, ContactMessage, TeamMember
from .translations import TRANSLATIONS, get_language

def translated(request, key):
    return TRANSLATIONS[get_language(request)][key]

def set_language(request, language):
    if language in TRANSLATIONS:
        request.session['language'] = language

    next_url = request.GET.get('next') or ''
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = 'index'

    response = redirect(next_url)
    if language in TRANSLATIONS:
        response.set_cookie('language', language, max_age=60 * 60 * 24 * 365)
    return response

def index(request):
    featured_cars = Car.objects.filter(category='Stock').order_by('-created_at')[:6]
    reviews = Review.objects.prefetch_related('media').all().order_by('-created_at')[:3]
    
    context = {
        'cars': featured_cars,
        'reviews': reviews,
    }
    return render(request, 'web/index.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )
        messages.success(request, translated(request, 'message_sent'))
        return redirect('contact')
        
    return render(request, 'web/contact.html')

def cars_in_stock(request):
    cars = Car.objects.filter(category='Stock').order_by('-created_at')
    return render(request, 'web/cars_in_stock.html', {'cars': cars, 'title': translated(request, 'all_inventory')})

def new_cars(request):
    cars = Car.objects.filter(category='Stock', condition='New').order_by('-created_at')
    return render(request, 'web/cars_in_stock.html', {'cars': cars, 'title': translated(request, 'new_cars')})

def used_cars(request):
    cars = Car.objects.filter(category='Stock', condition='Used').order_by('-created_at')
    return render(request, 'web/cars_in_stock.html', {'cars': cars, 'title': translated(request, 'used_cars')})

def damaged_cars(request):
    cars = Car.objects.filter(category='Stock', condition='Damaged').order_by('-created_at')
    return render(request, 'web/cars_in_stock.html', {'cars': cars, 'title': translated(request, 'damaged_cars')})

def how_it_works(request):
    return render(request, 'web/how_it_works.html')

def logistics(request):
    return render(request, 'web/logistics.html')

def reviews(request):
    reviews = Review.objects.prefetch_related('media').all().order_by('-created_at')
    return render(request, 'web/reviews.html', {'reviews': reviews})

def about(request):
    team = TeamMember.objects.all().order_by('created_at')

    return render(request, 'web/about.html', {'team': team})

def car_detail(request, pk):
    from django.shortcuts import get_object_or_404
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'web/car_detail.html', {'car': car})
