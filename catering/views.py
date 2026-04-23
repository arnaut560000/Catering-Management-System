from django.db.models import Avg, Count
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import BookingForm, FeedbackForm
from .models import Booking, Feedback, MenuItem, Venue


def analyze_sentiment(comment: str) -> str:
    comment_lower = comment.lower()

    positive_words = [
        "good",
        "great",
        "excellent",
        "delicious",
        "nice",
        "love",
        "amazing",
        "best",
    ]
    negative_words = [
        "bad",
        "poor",
        "terrible",
        "awful",
        "slow",
        "worst",
        "disappointing",
    ]

    pos_score = sum(word in comment_lower for word in positive_words)
    neg_score = sum(word in comment_lower for word in negative_words)

    if pos_score > neg_score:
        return "positive"
    if neg_score > pos_score:
        return "negative"
    return "neutral"


def home(request):
    venues = Venue.objects.all()[:3]
    featured_items = MenuItem.objects.filter(is_recommended=True)[:4]
    stats = {
        "venues": Venue.objects.count(),
        "menu_items": MenuItem.objects.count(),
        "bookings": Booking.objects.count(),
        "feedback_entries": Feedback.objects.count(),
    }
    context = {
        "venues": venues,
        "featured_items": featured_items,
        "stats": stats,
    }
    return render(request, "catering/home.html", context)


def book_event(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            request.session["latest_booking_id"] = booking.id
            return redirect("booking_success")
    else:
        form = BookingForm()

    return render(request, "catering/book.html", {"form": form})


def booking_success(request):
    booking = None
    latest_booking_id = request.session.get("latest_booking_id")
    if latest_booking_id:
        booking = Booking.objects.filter(id=latest_booking_id).select_related("venue").first()
    return render(request, "catering/booking_success.html", {"booking": booking})


def recommendations(request):
    preferred_meal = request.GET.get("meal", "lunch")
    persons = int(request.GET.get("persons", "50") or 50)

    recommended_items = MenuItem.objects.filter(category=preferred_meal).order_by(
        "-is_recommended",
        "name",
    )
    estimated_total = sum(item.price for item in recommended_items[:3]) * max(persons, 1)
    featured_count = recommended_items.filter(is_recommended=True).count()

    context = {
        "preferred_meal": preferred_meal,
        "persons": persons,
        "recommended_items": recommended_items,
        "estimated_total": estimated_total,
        "featured_count": featured_count,
    }
    return render(request, "catering/recommendations.html", context)


def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.sentiment = analyze_sentiment(feedback.comment)
            feedback.save()
            return redirect("dashboard")
    else:
        form = FeedbackForm()

    return render(request, "catering/feedback.html", {"form": form})


def dashboard(request):
    total_feedback = Feedback.objects.count()
    total_bookings = Booking.objects.count()
    upcoming_bookings = Booking.objects.filter(booking_date__gte=timezone.localdate()).count()
    average_rating = Feedback.objects.aggregate(avg=Avg("rating"))["avg"] or 0
    sentiment_data = Feedback.objects.values("sentiment").annotate(total=Count("id"))
    rating_breakdown = Feedback.objects.values("rating").annotate(total=Count("id")).order_by("-rating")
    popular_venues = Venue.objects.annotate(total_bookings=Count("bookings")).order_by("-total_bookings", "name")[:5]
    recent_bookings = Booking.objects.select_related("venue").order_by("-created_at")[:5]
    recent_feedback = Feedback.objects.select_related("booking").order_by("-created_at")[:5]

    context = {
        "total_feedback": total_feedback,
        "total_bookings": total_bookings,
        "upcoming_bookings": upcoming_bookings,
        "average_rating": round(average_rating, 1) if average_rating else 0,
        "sentiment_data": sentiment_data,
        "rating_breakdown": rating_breakdown,
        "popular_venues": popular_venues,
        "recent_bookings": recent_bookings,
        "recent_feedback": recent_feedback,
    }
    return render(request, "catering/dashboard.html", context)
