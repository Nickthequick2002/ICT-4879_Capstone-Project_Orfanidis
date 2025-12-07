from home.models import Blog

#This view is created to make sure that the blog name is shown in all the pages
# and in the blog page

def recent_blogs(request):
    return {
        'recent_blogs': Blog.objects.order_by('-created_at')[:3]
    }