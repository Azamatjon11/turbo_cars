from django.db import models

class Car(models.Model):
    CONDITION_CHOICES = [
        ('Used', 'Used'),
        ('Damaged', 'Damaged'),
        ('New', 'New'),
    ]
    CATEGORY_CHOICES = [
        ('Stock', 'Stock'),
        ('Auction', 'Auction'),
    ]
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]
    MILEAGE_UNIT_CHOICES = [
        ('km', 'km'),
        ('mil', 'mil'),
    ]

    title = models.CharField(max_length=200)
    year = models.IntegerField()
    mileage = models.PositiveIntegerField()
    mileage_unit = models.CharField(max_length=3, choices=MILEAGE_UNIT_CHOICES, default='mil')
    fuel_type = models.CharField(max_length=50, choices=FUEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cars/', null=True, blank=True)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Stock')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def display_mileage(self):
        return f"{self.mileage:,} {self.mileage_unit}"

class Review(models.Model):
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=5)
    location = models.CharField(max_length=100)
    vehicle_purchased = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} - {self.vehicle_purchased}"

    @property
    def author_initial(self):
        return self.author_name[0] if self.author_name else "?"

    @property
    def has_media(self):
        return self.media.exists()

class ReviewMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    review = models.ForeignKey(Review, related_name='media', on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    image = models.ImageField(upload_to='reviews/photos/', null=True, blank=True)
    video = models.FileField(upload_to='reviews/videos/', null=True, blank=True)
    caption = models.CharField(max_length=160, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f"{self.get_media_type_display()} for {self.review}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/', null=True, blank=True)
    whatsapp_number = models.CharField(max_length=20, null=True, blank=True, help_text="Enter number with country code, e.g., +1234567890")
    telegram_number = models.CharField(max_length=50, null=True, blank=True, help_text="Enter Telegram username or number (e.g. username or +1234567890)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car.title}"
