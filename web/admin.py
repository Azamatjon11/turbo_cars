from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.urls import reverse
from .models import Car, Review, ContactMessage, TeamMember

# Unregister Group model as it's not needed
admin.site.unregister(Group)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'price', 'condition', 'category', 'created_at', 'delete_button')
    list_filter = ('condition', 'category', 'fuel_type', 'year')
    search_fields = ('title', 'year', 'price')

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
