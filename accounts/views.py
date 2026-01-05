from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from .models import Profile, Testimonial
from django.views.decorators.http import require_POST


# LOGIN FUNCTIONALITY 
def login_view(request):
    if request.method == 'POST':

        # Read credentials
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check user in the database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) # Start the session
            return JsonResponse({
            'success': True,
            'username': user.username,
            'message': f'Welcome back, {user.username}!'
        })
        else:

            # Invalid login message
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})

    # Render the logi  modal template
    return render(request, 'accounts/login.html')


# LOGOUT FUNCTIONALITY
def logout_view(request):
    logout(request)
    request.session.flush()   # Clear the session info
    return redirect('home')


# SIGNUP FUNCTIONALITY 
def signup_view(request):
    if request.method == 'POST':
        data = request.POST

        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        # Optional preferences for the users
        focus = data.get('focus_body_part')
        goal = data.get('goal')
        exercise = data.get('exercise_type')

        # Validate passwords to see if they match
        if password1 != password2:
            return JsonResponse({'success': False, 'error': 'Passwords do not match.'})

        # Username must be unique
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists.'})

        # Email must be unique
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already registered.'})

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )

        # Create the Profile 
        Profile.objects.create(
            user=user,
            focus_body_part=focus,
            goal=goal,
            exercise_type=exercise,
        )

        # Auto-login the user after the signup
        login(request, user)

        return JsonResponse({
            'success': True,
            'username': user.username,
            'message': f'Welcome {username}! Your FitTrack profile was created successfully'
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# PROFILE PAGE VIEW AND UPDATE FUNCTIONALITY
@login_required
def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == "POST":

        # Update username 
        new_username = request.POST.get("username")
        if new_username:

            # Prevent duplicate usernames
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                messages.error(request, "This username is already taken.")
            else:
                user.username = new_username
                user.save()
                messages.success(request, "Username updated successfully.")

        # Update profile picture 
        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]
            profile.save()
            messages.success(request, "Profile picture updated successfully.")

        return redirect("profile")  # Prevent resubmission on refresh

    return render(request, "accounts/profile.html", {
        "user": user,
        "profile": profile,
    })

# CHANGE PROFILE PICTURE FUNCTIONALITY
@login_required
def change_pfp(request):
    if request.method == "POST":
        picture = request.FILES.get("profile_picture")  # Matches input name

        if picture:
            profile = request.user.profile
            profile.profile_picture = picture
            profile.save()
            messages.success(request, "Profile picture updated successfully!")
        else:
            messages.error(request, "Please select an image file.")
    return redirect("profile")

# CHANGE USERNAME FUNCTIONALITY (USING AJAX)
@login_required
def change_username(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."})

    # Read the JSON body 
    try:
        body = json.loads(request.body)
    except:
        return JsonResponse({"success": False, "error": "Invalid JSON received."})

    new_username = body.get("username")

    if not new_username:
        return JsonResponse({"success": False, "error": "Username cannot be empty."})

    # Check if the user is already a user
    if User.objects.filter(username=new_username).exists():
        return JsonResponse({"success": False, "error": "Username already taken."})

    # Update username and save it
    request.user.username = new_username
    request.user.save()

    return JsonResponse({"success": True, "username": new_username})


# CHANGE PASSWORD FUNCTIONALITY (USING AJAX)
@login_required
def change_password(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."})

    # Read the JSON body 
    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"success": False, "error": "Invalid JSON."})

    current_password = data.get("current_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    # Validate current password
    if not check_password(current_password, request.user.password):
        return JsonResponse({"success": False, "error": "Current password is incorrect."})

    # Validate new passwords match
    if new_password != confirm_password:
        return JsonResponse({"success": False, "error": "New passwords do not match."})

    # Prevent using the same password
    if check_password(new_password, request.user.password):
        return JsonResponse({"success": False, "error": "New password cannot be the same as the old password."})

    # Update password and save it 
    request.user.set_password(new_password)
    request.user.save()

    # Keep user logged in
    update_session_auth_hash(request, request.user)

    return JsonResponse({"success": True, "message": "Password updated successfully!"})

# DELETE ACCOUNT FUNCTIONALITY
@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("home")
    return redirect("profile")


# SUBMIT TESTIMONIALS FUNCTIONALITY
@login_required
@require_POST
def submit_testimonial(request):
    profile = request.user.profile

    message = request.POST.get("message", "").strip()

    # If the user has already submitted a testimonial, it is shown and gives them the ability to change it
    existing = Testimonial.objects.filter(profile=profile).first()
    if existing:
        existing.message = message
        existing.save()
    
    # If it is their first time writing a testimonial, they proceed normally. 
    else:
        Testimonial.objects.create(profile=profile, message=message)

    return redirect("profile")

# ALLOWS USERS TO EDIT THEIR TESTIMONIAL
def edit_testimonial(request):
    profile = request.user.profile

    # Get the user's testimonial (each user has at most one)
    testimonial = Testimonial.objects.filter(profile=profile).first()

    # If somehow they try to edit when they have none
    if not testimonial:
        messages.error(request, "You do not have a testimonial to edit.")
        return redirect("profile")

    # New updated text from the form
    new_message = request.POST.get("message", "").strip()

    # Do not save empty testimonials
    if not new_message:
        messages.error(request, "Your testimonial cannot be empty.")
        return redirect("profile")

    # Save the updated text
    testimonial.message = new_message
    testimonial.save()

    messages.success(request, "Your testimonial has been updated.")
    return redirect("profile")

# ALLOWS USERS TO PERMANTLY DELETE THEIR TESTIMONIAL
@login_required
@require_POST
def delete_testimonial(request):
    profile = request.user.profile

    # Try to find the testimonial that belongs to this user
    testimonial = Testimonial.objects.filter(profile=profile).first()

    # If they don't have a testimonial, nothing to delete
    if not testimonial:
        messages.error(request, "You do not have a testimonial to delete.")
        return redirect("profile")

    # Delete the testimonial from the database
    testimonial.delete()

    messages.success(request, "Your testimonial has been deleted.")
    return redirect("profile")

from django.contrib import messages

# ALLOWS THE USERS TO CHANGE THEIR PREFERENCES
@login_required
def update_preferences(request):

    # Only POST requests are allowed
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."})

    # Try to safely read the incoming JSON payload
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON data."})

    profile = request.user.profile

    # Update each preference or set it to None if empty
    profile.focus_body_part = data.get("focus_body_part") or None
    profile.goal = data.get("goal") or None
    profile.exercise_type = data.get("exercise_type") or None

    # Save all changes to the database
    profile.save()

    # Send success status back to the frontend
    return JsonResponse({"success": True})



