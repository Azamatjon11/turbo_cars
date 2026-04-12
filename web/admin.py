from django.contrib import admin
from .models import Car, Review, ContactMessage

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'price', 'condition', 'category', 'created_at')
    list_filter = ('condition', 'category', 'fuel_type', 'year')
    search_fields = ('title', 'year', 'price')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'vehicle_purchased', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('author_name', 'vehicle_purchased', 'content')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
from django.utils.html import format_html
from django.urls import reverse
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_at', 'delete_button')
    search_fields = ('name', 'role')

    def delete_button(self, obj):
        url = reverse('admin:web_teammember_delete', args=[obj.id])
        return format_html('<a class="button" style="color: #ba2121; font-weight: bold;" href="{}">Delete</a>', url)
    delete_button.short_description = 'Actions'
