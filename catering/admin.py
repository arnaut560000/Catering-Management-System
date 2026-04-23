from django.contrib import admin
from .models import Venue, MenuItem, Booking, Feedback


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'meal_type', 'price', 'is_recommended')
    list_filter = ('category', 'meal_type', 'is_recommended')
    search_fields = ('name', 'description', 'image_url')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'booking_date', 'event_time', 'number_of_persons', 'venue')
    list_filter = ('booking_date', 'venue')
    search_fields = ('customer_name', 'email', 'contact_number')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'sentiment', 'created_at')
    list_filter = ('sentiment', 'rating')
    search_fields = ('customer_name', 'comment')
