from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_event, name='book_event'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('dashboard/', views.dashboard, name='dashboard'),
]