from django.contrib import admin
from .models import Pet


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'breed', 'food_preference', 'feeding_schedule', 'user')

admin.site.register(Pet)