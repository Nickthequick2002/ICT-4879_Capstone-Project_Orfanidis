from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

@login_required
def membership_success(request):
    order_id = request.GET.get("orderID")

    # Activate membership for the user
    profile = request.user.profile
    profile.is_member = True
    profile.save()

    # Send a welcome email after a successful payment
    subject = "🎉 Welcome to FitTrack Premium!"
    message = (
        f"Hello {request.user.first_name or request.user.username},\n\n"
        "Thank you for upgrading to FitTrack Premium! \n"
        "Your membership is now active and ready to use.\n\n"
        f"Order ID: {order_id}\n\n"
        "If you have any questions, feel free to reply to this email.\n"
        "Enjoy your premium features!\n\n"
        "The FitTrack Team"
    )

    send_mail(
        subject,
        message,
        "fittrack.services@gmail.com",     
        [request.user.email],           
        fail_silently=False,
    )

    # Show and redirect the user to the confirmation page
    return render(request, "membership_success.html", {"order_id": order_id})

def membership_upgrade(request):
    # Simple membership upgrade page
    return render(request, "membership_upgrade.html")

