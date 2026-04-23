from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
    ]

    MEAL_TYPE_CHOICES = [
        ("rice_meal", "Rice Meal"),
        ("pasta", "Pasta"),
        ("snack", "Snack"),
        ("dessert", "Dessert"),
        ("drink", "Drink"),
        ("viand", "Viand"),
    ]

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_recommended = models.BooleanField(default=False)

    class Meta:
        ordering = ["category", "-is_recommended", "name"]

    def __str__(self):
        return self.name


class Booking(models.Model):
    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    contact_number = models.CharField(max_length=30)
    booking_date = models.DateField()
    event_time = models.TimeField()
    number_of_persons = models.PositiveIntegerField()
    selected_drinks = models.CharField(max_length=255, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="bookings")
    special_request = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["booking_date", "event_time", "-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.booking_date}"


class Feedback(models.Model):
    SENTIMENT_CHOICES = [
        ("positive", "Positive"),
        ("neutral", "Neutral"),
        ("negative", "Negative"),
    ]

    customer_name = models.CharField(max_length=120)
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="feedback_entries",
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    sentiment = models.CharField(
        max_length=20,
        choices=SENTIMENT_CHOICES,
        default="neutral",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.sentiment}"
