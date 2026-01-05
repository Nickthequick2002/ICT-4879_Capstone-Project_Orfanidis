# This script was made to reduce the food database amd then upload it for the calorie tracking system

import csv
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FitTrack.settings')
django.setup()

from mycals.models import Food  

# Path to CSV file 
csv_path = 'reduced_foods.csv'

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        Food.objects.create(
            name=row['name'],
            calories=float(row['calories']),
            protein=float(row['protein']),
            carbs=float(row['carbs']),
            fats=float(row['fats'])
        )

print("Food data imported successfully!")
