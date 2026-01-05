from django.contrib import admin
from .models import Exercise, Program, ProgramExercise

# Register your models here.

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "body_part", "goal", "exercise_type", "difficulty")
    list_filter = ("body_part", "goal", "exercise_type", "difficulty")
    search_fields = ("name", "short_description")


@admin.register(ProgramExercise)
class ProgramExerciseAdmin(admin.ModelAdmin):
    list_display = ("program", "exercise", "day_number", "order")
    list_filter = ("program", "day_number")





