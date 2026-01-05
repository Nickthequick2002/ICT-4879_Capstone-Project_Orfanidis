from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def contact_page(request):

    # Handles the form submission
    if request.method == 'POST':
        name = request.POST.get('cf-name')
        email = request.POST.get('cf-email')
        message = request.POST.get('cf-message')

        # This is a basic validation 
        if not name or not email or not message:
            return JsonResponse({'success': False, 'error': 'Missing fields'}, status=400)

        # Send email to the admin mailbox
        send_mail(
            subject=f"New message from {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email='fittrack.services@gmail.com',
            recipient_list=['fittrack.services@gmail.com'],
            fail_silently=False,
        )

        # A simple auto-reply to the user
        user_message = f"""
Hi {name},

Thanks for contacting FitTrack!

We’ve received your message and our support team is already on it.
You can expect a detailed response within the next 24 hours.

Best regards,
The FitTrack Support Team 
"""

        send_mail(
            subject="Thanks for reaching out to FitTrack!",
            message=user_message,  
            from_email='fittrack.services@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({'success': True})

    # Render the page for the GET response
    return render(request, 'contact/contact.html')
