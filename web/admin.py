from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.urls import reverse
from .models import Car, Review, ContactMessage, TeamMember, CarImage
from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data if d]
        else:
            result = [single_file_clean(data, initial)] if data else []
        return result

class CarAdminForm(forms.ModelForm):
    images_upload = MultipleFileField(
        required=False,
        label="Upload All Pictures",
        help_text="Select all pictures for this car. The first picture automatically becomes the main picture."
    )

    class Meta:
        model = Car
        exclude = ('image',)

# Unregister Group model as it's not needed
admin.site.unregister(Group)

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'created_at')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    form = CarAdminForm
    list_display = ('title', 'year', 'price', 'condition', 'category', 'created_at', 'delete_button')
    list_filter = ('condition', 'category', 'fuel_type', 'year')
    search_fields = ('title', 'year', 'price')

    def save_model(self, request, obj, form, change):
        images = request.FILES.getlist('images_upload')
        if images:
            # First one becomes the main picture
            obj.image = images[0]
            
        super().save_model(request, obj, form, change)
        
        if images:
            # Clear old additional images if re-uploading
            if change:
                CarImage.objects.filter(car=obj).delete()
            # Save the rest of the images as additional pictures
            for img in images[1:]:
                CarImage.objects.create(car=obj, image=img)

    def delete_button(self, obj):
        url = reverse('admin:web_car_delete', args=[obj.id])
        return format_html('<a class="button" style="color: #ba2121; font-weight: bold;" href="{}">Delete</a>', url)
    delete_button.short_description = 'Actions'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'vehicle_purchased', 'rating', 'created_at', 'delete_button')
    list_filter = ('rating', 'created_at')
    search_fields = ('author_name', 'vehicle_purchased', 'content')

    def delete_button(self, obj):
        url = reverse('admin:web_review_delete', args=[obj.id])
        return format_html('<a class="button" style="color: #ba2121; font-weight: bold;" href="{}">Delete</a>', url)
    delete_button.short_description = 'Actions'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'delete_button')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

    def delete_button(self, obj):
        url = reverse('admin:web_contactmessage_delete', args=[obj.id])
        return format_html('<a class="button" style="color: #ba2121; font-weight: bold;" href="{}">Delete</a>', url)
    delete_button.short_description = 'Actions'
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_at', 'delete_button')
    search_fields = ('name', 'role')

    def delete_button(self, obj):
        url = reverse('admin:web_teammember_delete', args=[obj.id])
        return format_html('<a class="button" style="color: #ba2121; font-weight: bold;" href="{}">Delete</a>', url)
    delete_button.short_description = 'Actions'
