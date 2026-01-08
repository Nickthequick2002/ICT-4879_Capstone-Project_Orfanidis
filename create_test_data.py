import os
import django
import sys

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FitTrack.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile
from fitshop.models import Order, Product
from mycals.models import Consume, Food
from django.utils import timezone

username = 'testprofile'
try:
    user = User.objects.get(username=username)
    print(f"User {username} already exists")
except User.DoesNotExist:
    user = User.objects.create_user(username, 'testprofile@example.com', 'password123')
    print(f"User {username} created")

# Ensure profile exists
profile, created = Profile.objects.get_or_create(user=user)
profile.is_member = True
profile.goal = 'strength'
profile.save()
print("Profile updated: Member=True, Goal=Strength")

# Create Order
product, _ = Product.objects.get_or_create(name='Test Dumbbell', defaults={'price': 50.00})
# Clear old orders for test
Order.objects.filter(user=user).delete()
Order.objects.create(user=user, total_price=50.00, order_id='ORDER_TEST_001')
Order.objects.create(user=user, total_price=25.50, order_id='ORDER_TEST_002')
print("Orders created")

# Create Consumption
food, _ = Food.objects.get_or_create(name='Test Apple', defaults={'calories': 95, 'protein': 0.5, 'carbs': 25, 'fats': 0.3})
# Clear old consumption for today
Consume.objects.filter(user=user, date=timezone.now().date()).delete()
Consume.objects.create(user=user, food_consumed=food)
Consume.objects.create(user=user, food_consumed=food) # 2 apples
print("Consumption data created")
