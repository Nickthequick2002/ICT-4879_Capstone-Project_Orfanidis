from django.db import models
from django.contrib.auth.models import User

# Extra user info is stored seperately form the built-in user model
class Profile(models.Model):

    # Dropdown choices for the user preferences
    BODY_PART_CHOICES = [
        ('arms', 'Arms'),
        ('legs', 'Legs'),
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('abs', 'Abs'),
        ('full', 'Full Body'),
    ]

    GOAL_CHOICES = [
        ('strength', 'Build Strength'),
        ('weight_loss', 'Lose Weight'),
        ('endurance', 'Improve Endurance'),
        ('flexibility', 'Increase Flexibility'),
    ]
    EXERCISE_CHOICES = [
        ('cardio', 'Cardio'),
        ('weights', 'Weights'),
        ('yoga', 'Yoga'),
        ('hiit', 'HIIT'),
        ('calisthenics', 'Calisthenics'),
    ]

    # On-to-one link with the Django user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Profile picture functionality
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')

    # User preferences and all the choices are optional
    focus_body_part = models.CharField(max_length=100, blank=True, null=True, choices=BODY_PART_CHOICES)
    goal = models.CharField(max_length=100, blank=True, null=True, choices=GOAL_CHOICES)
    exercise_type = models.CharField(max_length=100, blank=True, null=True, choices=EXERCISE_CHOICES)

    # This is the membership status, keeps the admin page updated to see who is member
    is_member = models.BooleanField(default=False)

class Testimonial(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="testimonials")
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} Profile"

