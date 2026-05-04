from pathlib import Path

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.urls import reverse
from .models import Car, Review, ContactMessage, TeamMember, CarImage, ReviewMedia
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
    mileage_unit = forms.ChoiceField(
        choices=Car.MILEAGE_UNIT_CHOICES,
        widget=forms.RadioSelect,
        label="Mileage Unit",
    )
    images_upload = MultipleFileField(
        required=False,
        label="Upload All Pictures",
        help_text="Select all pictures for this car. The first picture automatically becomes the main picture."
    )

    class Meta:
        model = Car
        exclude = ('image',)

class ReviewAdminForm(forms.ModelForm):
    media_upload = MultipleFileField(
        required=False,
        label="Add Review Photos/Videos",
        help_text="Select delivery photos and video clips for this customer review."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media_upload'].widget.attrs['accept'] = 'image/*,video/*'

    class Meta:
        model = Review
        fields = '__all__'

# Unregister Group model as it's not needed
admin.site.unregister(Group)



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

class ReviewMediaInline(admin.TabularInline):
    model = ReviewMedia
    extra = 1
    fields = ('media_type', 'image', 'video', 'caption', 'sort_order')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    inlines = [ReviewMediaInline]
    list_display = ('author_name', 'vehicle_purchased', 'rating', 'media_count', 'created_at', 'delete_button')
    list_filter = ('rating', 'created_at')
    search_fields = ('author_name', 'vehicle_purchased', 'content')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        uploaded_media = request.FILES.getlist('media_upload')
        next_sort_order = obj.media.count()
        for index, uploaded_file in enumerate(uploaded_media):
            content_type = uploaded_file.content_type or ''
            extension = Path(uploaded_file.name).suffix.lower()
            is_video = content_type.startswith('video/') or extension in {'.mp4', '.mov', '.m4v', '.webm', '.avi'}
            ReviewMedia.objects.create(
                review=obj,
                media_type='video' if is_video else 'image',
                video=uploaded_file if is_video else None,
                image=None if is_video else uploaded_file,
                sort_order=next_sort_order + index,
            )

    def media_count(self, obj):
        return obj.media.count()
    media_count.short_description = 'Media'

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
