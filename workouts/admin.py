from django.contrib import admin
from .models import Exercise, Program, ProgramExercise, ExerciseImage

# Register your models here.

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name",)

class ExerciseImageInline(admin.TabularInline):
    model = ExerciseImage
    extra = 1

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "body_part", "goal", "exercise_type", "difficulty")
    list_filter = ("body_part", "goal", "exercise_type", "difficulty")
    search_fields = ("name", "short_description")
    inlines = [ExerciseImageInline]


@admin.register(ProgramExercise)
class ProgramExerciseAdmin(admin.ModelAdmin):
    list_display = ("program", "exercise", "day_number", "order")
    list_filter = ("program", "day_number")





