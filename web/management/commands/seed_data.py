from django.core.management.base import BaseCommand
from web.models import Car, Review

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Clear existing data
        Car.objects.all().delete()
        Review.objects.all().delete()

        # Cars
        cars = [
            {
                "title": "2022 BMW 3 Series 330i",
                "year": 2022,
                "mileage": "15,000 mi",
                "fuel_type": "Petrol",
                "price": 42500,
                "condition": "Used",
                "category": "Stock",
                "image_url": "https://images.unsplash.com/photo_1555215695_3004980ad54e",
            },
            {
                "title": "2021 Mercedes-Benz C-Class",
                "year": 2021,
                "mileage": "22,000 mi",
                "fuel_type": "Petrol",
                "price": 38900,
                "condition": "Used",
                "category": "Stock",
                "image_url": "https://images.unsplash.com/photo_1618843479313_40f8afb4b4d8",
            },
            {
                "title": "2020 Audi A4 Premium Plus",
                "year": 2020,
                "mileage": "28,000 mi",
                "fuel_type": "Petrol",
                "price": 34500,
                "condition": "Used",
                "category": "Stock",
                "image_url": "https://images.unsplash.com/photo_1606664515524_ed2f786a0bd6",
            },
            {
                "title": "2019 Tesla Model 3 Long Range",
                "year": 2019,
                "mileage": "35,000 mi",
                "fuel_type": "Electric",
                "price": 32000,
                "condition": "Used",
                "category": "Stock",
                "image_url": "https://images.unsplash.com/photo_1560958089_b8a1929cea89",
            },
            {
                "title": "2018 Range Rover Sport",
                "year": 2018,
                "mileage": "65,000 mi",
                "fuel_type": "Diesel",
                "price": 8500,
                "condition": "Damaged",
                "category": "Auction",
                "image_url": "https://images.unsplash.com/photo_1606016159991_dfe4f2746ad5",
            },
            {
                "title": "2022 Toyota Camry Hybrid",
                "year": 2022,
                "mileage": "12,000 mi",
                "fuel_type": "Hybrid",
                "price": 29500,
                "condition": "Used",
                "category": "Stock",
                "image_url": "https://images.unsplash.com/photo_1621007947382_bb3c3994e3fb",
            },
        ]

        for car_data in cars:
            Car.objects.create(**car_data)
            self.stdout.write(f"Created car: {car_data['title']}")

        # Reviews
        reviews = [
            {
                "author_name": "James Wilson",
                "vehicle_purchased": "2022 BMW 3 Series",
                "location": "Toronto, Canada",
                "content": "Excellent service from start to finish! The team helped me find the perfect BMW and the shipping to Canada was smooth and hassle-free. Highly recommend!",
                "rating": 5
            },
            {
                "author_name": "Sarah Martinez",
                "vehicle_purchased": "2021 Mercedes C-Class",
                "location": "Miami, FL",
                "content": "I was hesitant to buy a car online, but AutoExcellence made it so easy. The vehicle was exactly as described and arrived on time. Will definitely buy again!",
                "rating": 5
            },
            {
                "author_name": "Michael Chen",
                "vehicle_purchased": "2019 Tesla Model 3",
                "location": "Los Angeles, CA",
                "content": "Found a great deal on a Tesla through their auction. The whole process was transparent and the logistics team kept me updated throughout. Fantastic experience!",
                "rating": 5
            }
        ]

        for review_data in reviews:
            Review.objects.create(**review_data)
            self.stdout.write(f"Created review: {review_data['author_name']}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
