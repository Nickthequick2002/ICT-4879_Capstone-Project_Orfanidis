from django.db import models

# Create your models here.

class Exercise(models.Model):

    # They have the same names as in the profile file, for better filtering. 
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

    EXERCISE_TYPE_CHOICES = [
        ('cardio', 'Cardio'),
        ('weights', 'Weights'),
        ('yoga', 'Yoga'),
        ('hiit', 'HIIT'),
        ('calisthenics', 'Calisthenics'),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    # Basic exercise info
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255, blank=True)
    detailed_instructions = models.TextField(
        blank=True,
        help_text="Step-by-step guide on how to perform the exercise safely."
    )

    # Media files for exercise previews/tutorials
    image = models.ImageField(
        upload_to='exercises/images/',
        blank=True,
        null=True,
        help_text="Upload an illustrative image of the exercise."
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="Link to a video demo (YouTube or mp4 URL)."
    )

    # Classification fields (used for filtering and recommendations)
    body_part = models.CharField(max_length=20, choices=BODY_PART_CHOICES)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, blank=True)

    # Optional equipment info (dumbbells, mat, etc.)
    equipment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


# Pograms class that represents a training programs
class Program(models.Model):
    name = models.CharField(max_length=200)
    short_description = models.CharField(
        max_length=255,
        blank=True,
        help_text="Shown on the program card in the UI."
    )
    long_description = models.TextField(
        blank=True,
        help_text="Detailed explanation of what this program includes."
    )

    image = models.ImageField(
        upload_to='programs/images/',
        blank=True,
        null=True,
        help_text="Thumbnail image used in the program card."
    )

    def __str__(self):
        return self.name


# The main class of the exercise model. Gives the tags that the exercises have and also the different exercises depending on the day. 
class ProgramExercise(models.Model):
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        help_text="The program this exercise belongs to."
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        help_text="The exercise being added to this program."
    )

    # Full programs structure that gives also the different exercises and days
    day_number = models.PositiveIntegerField(
        default=1,
        help_text="Day of the program (e.g., 1 for Day 1)."
    )

    # Controls display order within the day
    order = models.PositiveIntegerField(
        default=1,
        help_text="Position of this exercise inside the day's sequence."
    )

    # Optional training structure
    sets = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Number of sets (optional)."
    )
    reps = models.CharField(
        max_length=50,
        blank=True,
        help_text="Reps or duration (e.g., '12', '30 sec')."
    )

    class Meta:
        ordering = ['day_number', 'order']

    def __str__(self):
        return f"{self.program.name} - {self.exercise.name}"

# This class is created in order for the admin to be able to add multiple images.
class ExerciseImage(models.Model):
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="exercise_images/")

    def __str__(self):
        return f"Image for {self.exercise.name}"