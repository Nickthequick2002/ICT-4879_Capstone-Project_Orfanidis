from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Blog


# Create your views here.

def home(request):
    footer_blogs = Blog.objects.order_by('-created_at')[:3]  # latest 3 blogs

    return render(request, 'index.html', {
        'footer_blogs': footer_blogs,
    })

def membership_upgrade(request):
    return render(request, "membership_upgrade.html")

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, "blog_detail.html", {'blog': blog})










