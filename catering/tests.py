from datetime import date, time

from django.test import TestCase
from django.urls import reverse

from .models import Booking, Feedback, MenuItem, Venue


class CateringViewsTests(TestCase):
    def setUp(self):
        self.venue = Venue.objects.create(
            name="Main Hall",
            location="Downtown",
            capacity=120,
        )
        self.booking = Booking.objects.create(
            customer_name="Ana Cruz",
            email="ana@example.com",
            contact_number="09123456789",
            booking_date=date.today(),
            event_time=time(12, 0),
            number_of_persons=40,
            selected_drinks="Iced Tea",
            venue=self.venue,
            special_request="Vegetarian options",
        )
        MenuItem.objects.create(
            name="Chicken Pasta",
            category="lunch",
            meal_type="pasta",
            description="Creamy pasta dish",
            price="180.00",
            is_recommended=True,
        )
        Feedback.objects.create(
            customer_name="Ana Cruz",
            booking=self.booking,
            rating=5,
            comment="Great food and excellent service",
            sentiment="positive",
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_recommendations_page_loads(self):
        response = self.client.get(reverse("recommendations"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page_loads(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_booking_submission_redirects_to_success(self):
        response = self.client.post(
            reverse("book_event"),
            {
                "customer_name": "Marco Santos",
                "email": "marco@example.com",
                "contact_number": "09999999999",
                "booking_date": "2099-12-31",
                "event_time": "18:30",
                "number_of_persons": 80,
                "selected_drinks": "Juice",
                "venue": self.venue.id,
                "special_request": "Birthday setup",
            },
        )
        self.assertRedirects(response, reverse("booking_success"))

    def test_feedback_submission_sets_sentiment(self):
        response = self.client.post(
            reverse("submit_feedback"),
            {
                "customer_name": "Marco Santos",
                "booking": self.booking.id,
                "rating": 5,
                "comment": "Amazing food and great service",
            },
        )
        self.assertRedirects(response, reverse("dashboard"))
        feedback = Feedback.objects.latest("id")
        self.assertEqual(feedback.sentiment, "positive")
