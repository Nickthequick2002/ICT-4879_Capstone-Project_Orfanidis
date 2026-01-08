from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from fitshop.models import Product, Order 
from payments.models import SubscriptionTransaction 
from workouts.models import Exercise, Program, ProgramExercise, UserProgramActivity
from django import forms
from home.models import Blog
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

# ... (keep existing imports)
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
    
    # --- 1. USER ANALYTICS ---
    users = User.objects.all()
    total_users = users.count()
    
    # Time ranges
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    day_ago = now - timedelta(days=1)
    
    new_users_week = users.filter(date_joined__gte=week_ago).count()
    new_users_month = users.filter(date_joined__gte=month_ago).count()
    
    # Active users (last login)
    active_users_24h = users.filter(last_login__gte=day_ago).count()
    active_users_7d = users.filter(last_login__gte=week_ago).count()
    
    # Premium Ratio
    # We need to access the Profile model. "is_member" indicates premium.
    premium_users = 0
    for u in users:
        if hasattr(u, 'profile') and u.profile.is_member:
            premium_users += 1
            
    premium_ratio = round((premium_users / total_users * 100), 1) if total_users > 0 else 0

    # --- 2. BUSINESS ANALYTICS ---
    # Total Revenue = Orders + Subscriptions
    order_revenue = Order.objects.aggregate(sum=Sum('total_price'))['sum'] or 0
    sub_revenue = SubscriptionTransaction.objects.aggregate(sum=Sum('amount'))['sum'] or 0
    total_revenue = float(order_revenue) + float(sub_revenue)
    
    # Monthly Income (Orders + Subs in last 30 days)
    # Ideally "Monthly" means "This Month", but "Last 30 Days" is often more useful for rolling stats.
    # Let's do "Current Month" to be precise with "Income" terminology usually.
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    monthly_orders = Order.objects.filter(created_at__gte=current_month_start).aggregate(sum=Sum('total_price'))['sum'] or 0
    monthly_subs = SubscriptionTransaction.objects.filter(created_at__gte=current_month_start).aggregate(sum=Sum('amount'))['sum'] or 0
    monthly_income = float(monthly_orders) + float(monthly_subs)
    
    # ARPU (Average Revenue Per User)
    arpu = round(total_revenue / total_users, 2) if total_users > 0 else 0


    # --- 3. CONTENT ANALYTICS ---
    # Most accessed programs
    most_accessed = UserProgramActivity.objects.values('program__name').annotate(views=Count('id')).order_by('-views')[:5]
    
    # Program Enrollments (Total count of activity records)
    total_enrollments = UserProgramActivity.objects.count()

    # Basic stats shown on the dashboard cards (kept for compatibility)
    products_count = Product.objects.count()


    # --- 4. ACTIVITY FEED ---
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_orders = Order.objects.order_by('-created_at')[:5]

    context = {
        # Core Stats
        'products_count': products_count,
        'users_count': total_users,
        
        # User Stats
        'new_users_week': new_users_week,
        'new_users_month': new_users_month,
        'active_users_24h': active_users_24h,
        'active_users_7d': active_users_7d,
        'premium_ratio': premium_ratio,
        'premium_users': premium_users,
        'free_users': total_users - premium_users,
        
        # Business Stats
        'total_revenue': total_revenue,
        'monthly_income': monthly_income,
        'arpu': arpu,
        
        # Content Stats
        'most_accessed_programs': most_accessed,
        'total_enrollments': total_enrollments,
        
        # Activity Feed
        'recent_users': recent_users,
        'recent_orders': recent_orders,
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

     # List all blogs for newest to olders 
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


def dashboard_exercises_list(request):
    # Prefetch related programs for each exercise for performance
    exercises = Exercise.objects.all().prefetch_related('programexercise_set__program')

    # Handles the search bar logic
    query = request.GET.get("q")
    if query:
        exercises = exercises.filter(name__icontains=query)

    # Calculates the total amount of exercises in the list
    total_exercises = exercises.count() 

    return render(request, 'dashboard/exercise_list.html', {
        'exercises': exercises,
        'total_exercises': total_exercises, 
        'query': query,
    })

def dashboard_add_exercise(request):
    programs = Program.objects.all()  # Used in the multi-select dropdown

    if request.method == 'POST':
        # Basic exercise fields
        name = request.POST.get('name')
        short_description = request.POST.get('short_description')
        detailed_instructions = request.POST.get('detailed_instructions')

        image = request.FILES.get("image")

        
        video_url = request.POST.get('video_url')

        body_part = request.POST.get('body_part')
        goal = request.POST.get('goal')
        exercise_type = request.POST.get('exercise_type')
        difficulty = request.POST.get('difficulty')
        equipment = request.POST.get('equipment')

        # Create exercise object
        exercise = Exercise.objects.create(
            name=name,
            short_description=short_description,
            detailed_instructions=detailed_instructions,
            image=image,
            video_url=video_url,
            body_part=body_part,
            goal=goal,
            exercise_type=exercise_type,
            difficulty=difficulty,
            equipment=equipment,
        )

        # Program assignment (multi-select)
        selected_program_ids = request.POST.getlist('programs')

        for program_id in selected_program_ids:
            ProgramExercise.objects.create(
                program_id=program_id,
                exercise=exercise,
                day_number=1,  # simple for now
                order=1,
            )

        messages.success(request, "Exercise added successfully.")
        return redirect('dashboard-exercises')

    return render(request, 'dashboard/exercise_form.html', {
        'title': 'Add New Exercise',
        'exercise': None,
        'programs': programs,
        'selected_program_ids': [],
    })

def dashboard_edit_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    programs = Program.objects.all()

    # Current program assignments for this exercise
    selected_program_ids = list(
        ProgramExercise.objects.filter(exercise=exercise).values_list('program_id', flat=True)
    )

    if request.method == 'POST':
        # Update basic fields
        exercise.name = request.POST.get('name')
        exercise.short_description = request.POST.get('short_description')
        exercise.detailed_instructions = request.POST.get('detailed_instructions')

        # If a new image is uploaded, replace it
        image = request.FILES.get('image')
        if image:
            exercise.image = image

        exercise.video_url = request.POST.get('video_url')
        exercise.body_part = request.POST.get('body_part')
        exercise.goal = request.POST.get('goal')
        exercise.exercise_type = request.POST.get('exercise_type')
        exercise.difficulty = request.POST.get('difficulty')
        exercise.equipment = request.POST.get('equipment')

        exercise.save()

        # Update program assignments
        new_program_ids = request.POST.getlist('programs')

        # Remove old links
        ProgramExercise.objects.filter(exercise=exercise).delete()

        # Create new links
        for program_id in new_program_ids:
            ProgramExercise.objects.create(
                program_id=program_id,
                exercise=exercise,
                day_number=1,
                order=1,
            )

        messages.success(request, "Exercise updated successfully.")
        return redirect('dashboard-exercises')

    return render(request, 'dashboard/exercise_form.html', {
        'title': 'Edit Exercise',
        'exercise': exercise,
        'programs': programs,
        'selected_program_ids': selected_program_ids,
    })

def dashboard_delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    exercise.delete()  # ProgramExercise rows are deleted via CASCADE
    messages.success(request, "Exercise deleted successfully.")
    return redirect('dashboard-exercises')

# Calculates how many exercises exist up  to now.
def manage_exercises(request):
    exercises = Exercise.objects.all()
    total_exercises = exercises.count()
    return render(request, "exercise_list.html", {
        "exercises": exercises,
        "total_exercises": total_exercises
    })



