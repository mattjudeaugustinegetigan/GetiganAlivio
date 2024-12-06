from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.timezone import now, localtime

# Pet Model: Represents a pet owned by a user
class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link pet to the user
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100, blank=True, null=True)
    food_preference = models.CharField(max_length=100, blank=True, null=True)
    pet_type = models.CharField(max_length=10, choices=[('dog', 'Dog'), ('cat', 'Cat')], default='dog')  
    photo = models.ImageField(upload_to='images/', default='images/dog.png')  # Optional photo upload
    FEEDING_SCHEDULE_CHOICES = [
        ('once', 'Once a day'),
        ('twice', 'Twice a day'),
        ('thrice', 'Three times a day'),
    ]
    feeding_schedule = models.CharField(max_length=10, choices=FEEDING_SCHEDULE_CHOICES)

    def __str__(self):
        return self.name


# FeedingSchedule Model: Represents feeding times for a pet
class FeedingSchedule(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='feeding_schedules')
    time = models.TimeField()  # Feeding time
    meal_type = models.CharField(max_length=50)  # e.g., Breakfast, Dinner
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.meal_type} for {self.pet.name} at {self.time}"

    def send_feeding_notification(self):
        """Send an email notification to the pet owner."""
        current_time = localtime(now()).time()  # Get the local time
        if current_time >= self.time:  # If the current time matches or passes the feeding time
            subject = f"Time to feed your pet: {self.pet.name}"
            message = (
                f"Hello {self.pet.user.username},\n\n"
                f"It's time to feed your pet {self.pet.name} ({self.meal_type}).\n\n"
                "Best regards,\nYour Pet Care App"
            )
            email_from = 'mattjudeaugustine.getigan@cit.edu'  # Replace with your Outlook email address
            recipient_list = [self.pet.user.email]

            try:
                send_mail(subject, message, email_from, recipient_list)
                print(f"Notification sent to {self.pet.user.email} for feeding {self.pet.name}.")
            except Exception as e:
                print(f"Failed to send email notification: {e}")
