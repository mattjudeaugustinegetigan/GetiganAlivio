from celery import shared_task
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.core.mail import send_mail
from django.conf import settings
from .models import Pet, FeedingSchedule

@shared_task
def check_feeding_time():
    pets = Pet.objects.all()
    current_time = make_aware(datetime.now())  # Ensure the current time is timezone-aware

    for pet in pets:
        feeding_schedule = FeedingSchedule.objects.filter(pet=pet)
        for schedule in feeding_schedule:
            feeding_time = schedule.time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
            if feeding_time <= current_time < feeding_time + timedelta(minutes=10):  # 10-minute window
                send_mail(
                    'Time to Feed Your Pet!',
                    f'It\'s time to feed {pet.name}! Please give them {schedule.meal_type}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [pet.user.email],  # Send email to the pet's owner
                )
