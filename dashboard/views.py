from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from fitshop.models import Product  
from django import forms
from home.models import Blog

# Create your views here.

# Use of Django's user model 
User = get_user_model()

# This function checks if the logged-in user is a staff member.
def staff_check(user):
    return user.is_staff

# The user must be loged in and the user must pass the staff check
# If the does not have these two, the access in dashboard is blocked
def staff_required(view_func):
    decorated_view = login_required(user_passes_test(staff_check)(view_func))
    return decorated_view


# Custom Admin Dashboard Home
@staff_required
def dashboard_home(request):

    # Basic stats shown on the dashboard cards
    products_count = Product.objects.count()
    users_count = User.objects.count()

    context = {
        'products_count': products_count,
        'users_count': users_count,
    }

    # Render the dashboard homepage HTML template with these stats.
    return render(request, 'dashboard/home.html', context)


# Product list page
@staff_required
def manage_products(request):

    # List all products (newest first)
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/product_list.html', {
        'products': products
    })


# This is the product form that add and edit functions are using
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'short_description', 'long_description', 'price', 'image']

        # Add Bootstrap styling to inputs
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'long_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# Add product function
@staff_required
def add_product(request):

    # If form is submitted then the product is created
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard-products')
    
    # Show empty form
    else:
        form = ProductForm()

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'title': "Add New Product",
    })


# Edit product function
@staff_required
def edit_product(request, id):

    # Find the product or show 404
    product: Product = get_object_or_404(Product, id=id)

    # Save updated product info
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard-products')
    
    # Load form with current product data
    else:
        form = ProductForm(instance=product)

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'title': f"Edit Product: {product.name}"
    })


# Delete product function
@staff_required
def delete_product(request, id):

    # Delete product and send back to list
    product: Product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('dashboard-products')


# This functions show to the admin the users that have created an account
def user_list(request):

    # Simple list of all registered users
    users = User.objects.all().order_by('date_joined')
    return render(request, 'dashboard/user_list.html', {'users': users})


@staff_required
def blog_list(request):

     # List all blogs (newest first)
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'dashboard/blog_list.html', {'blogs': blogs})


@staff_required
def create_blog(request):

    # Handle blog creation
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # Save the new blog post
        Blog.objects.create(
            title=title,
            subtitle=subtitle,
            content=content,
            image=image,
            author=request.user
        )

        return redirect('blog_list')
    
    # Show empty form
    return render(request, 'dashboard/create_blog.html')


@staff_required
def edit_blog(request, blog_id):

    # Load blog or show 404
    blog = get_object_or_404(Blog, id=blog_id)

    # Update blog fields manually
    if request.method == "POST":
        blog.title = request.POST.get('title')
        blog.subtitle = request.POST.get('subtitle')
        blog.content = request.POST.get('content')

        # Only update image if a new one was uploaded
        if request.FILES.get('image'):
            blog.image = request.FILES.get('image')

        blog.save()
        return redirect('blog_list')

    # Load existing data into the form
    return render(request, 'dashboard/create_blog.html', {'blog': blog})


@staff_required
def delete_blog(request, blog_id):

    # Delete the selected blog
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    return redirect('blog_list')


