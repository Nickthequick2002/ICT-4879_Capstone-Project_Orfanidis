from django.shortcuts import render
from accounts.models import Testimonial

# Create your views here.
def aboutus_view(request):
    testimonials = (
        Testimonial.objects
        .filter(is_approved=True)
        .select_related("profile", "profile__user")
        .order_by("-created_at")[:10]
    )

    no_testimonials_exist = (testimonials.count() == 0)

    return render(request, "aboutus/aboutus.html", {
        "testimonials": testimonials,
        "no_testimonials_exist": no_testimonials_exist,
    })


