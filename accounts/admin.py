from django.contrib import admin
from .models import Profile

# Register your models here.

# Register profile model in django admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Columns shown in the admin list view
    list_display = ("user", "goal", "focus_body_part", "exercise_type", "is_member")
    
    # Allow quick membership toggle directly from the list
    list_editable = ("is_member",) 

    # Simple search by username or profile preferences
    search_fields = ("user__username", "goal", "focus_body_part")
