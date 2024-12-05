from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link pet to the user
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    food_preference = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=10, choices=[('dog', 'Dog'), ('cat', 'Cat')], default='dog')  
    photo = models.ImageField(upload_to='images/', default='images/dog.png')
    FEEDING_SCHEDULE_CHOICES = [
        ('once', 'Once a day'),
        ('twice', 'Twice a day'),
        ('thrice', 'Three times a day'),
    ]
    feeding_schedule = models.CharField(max_length=10, choices=FEEDING_SCHEDULE_CHOICES)

    def __str__(self):
        return self.name

class FeedingSchedule(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='feeding_schedules')
    time = models.TimeField()
    meal_type = models.CharField(max_length=50)  # e.g., Breakfast, Dinner
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
