from django.db import models
from django.contrib.auth.models import User


# Food item with basic nutrition values
class Food(models.Model):
    name = models.CharField(max_length=255)  # Food name
    calories = models.FloatField() # Total calories per serving
    protein = models.FloatField()  # Protein in grams
    carbs = models.FloatField() # Carbohydrates in grams
    fats = models.FloatField() # Fats in grams
 
    def __str__(self):
        return self.name

# Stores what food a user ate on a specific day
class Consume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True) # Saves today's date

    def __str__(self):
        return f"{self.user.username} - {self.food_consumed.name}"
