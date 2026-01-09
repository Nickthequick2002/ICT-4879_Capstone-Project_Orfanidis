from django.db import models
from django.contrib.auth.models import User


# Food item with basic nutrition values
class Food(models.Model):
    name = models.CharField(max_length=255)  # Food name
    calories = models.FloatField() # Total calories per serving
    protein = models.FloatField()  # Protein in grams
    carbs = models.FloatField() # Carbohydrates in grams
    fats = models.FloatField() # Fats in grams
    serving_qty = models.FloatField(default=1.0) # Amount (e.g., 100 or 1)
    serving_unit = models.CharField(max_length=50, default="serving") # Unit (e.g., "g", "oz", "cup")

    def __str__(self):
        return f"{self.name} ({self.serving_qty} {self.serving_unit})"

# Stores what food a user ate on a specific day
class Consume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1.0) # Number of servings/units consumed
    date = models.DateField(auto_now_add=True) # Saves today's date

    @property
    def total_calories(self):
        return round(self.food_consumed.calories * self.quantity, 1)

    @property
    def total_protein(self):
        return round(self.food_consumed.protein * self.quantity, 1)

    @property
    def total_carbs(self):
        return round(self.food_consumed.carbs * self.quantity, 1)

    @property
    def total_fats(self):
        return round(self.food_consumed.fats * self.quantity, 1)

    def __str__(self):
        return f"{self.user.username} - {self.food_consumed.name} (x{self.quantity})"
