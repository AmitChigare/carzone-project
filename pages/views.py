from django.shortcuts import render, redirect
from .models import Team
from cars.models import Car
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.
def home(request):
    teams = Team.objects.all()
    featured_cars = Car.objects.filter(is_featured=True).order_by("-created_date")
    all_cars = Car.objects.all().order_by("-created_date")
    # search_fields = Car.objects.values("model", "year", "city", "body_style")
    model_search = Car.objects.values_list("model", flat=True).distinct()
    year_search = Car.objects.values_list("year", flat=True).distinct()
    city_search = Car.objects.values_list("city", flat=True).distinct()
    body_style_search = Car.objects.values_list("body_style", flat=True).distinct()
    context = {
        "teams": teams,
        "featured_cars": featured_cars,
        "all_cars": all_cars,
        # "search_fields": search_fields,
        "model_search": model_search,
        "year_search": year_search,
        "city_search": city_search,
        "body_style_search": body_style_search,
    }
    return render(request, "pages/home.html", context)


def about(request):
    teams = Team.objects.all()
    context = {
        "teams": teams,
    }
    return render(request, "pages/about.html", context)


def services(request):
    return render(request, "pages/services.html")


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        phone = request.POST["phone"]
        message = request.POST["message"]

        email_subject = (
            f"You have a new message from Carzone website regarding: {subject}"
        )
        message_body = (
            f"Name: {name}. Email: {email}. Phone: {phone}. Message: {message}"
        )

        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        send_mail(
            email_subject,
            message_body,
            "smtpamit@gmail.com",
            [admin_email],
            fail_silently=False,
        )
        messages.success(
            request, "Thank you for contacting us. We will get back to you shortly"
        )
        return redirect("contact")
    return render(request, "pages/contact.html")
