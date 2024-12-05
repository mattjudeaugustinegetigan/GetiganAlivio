from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Pet
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import PetForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .forms import UserProfileForm
from django.contrib.auth import update_session_auth_hash 
from .forms import ProfileUpdateForm
from .forms import ProfileUpdateForm, CustomPasswordChangeForm
from .models import Pet, FeedingSchedule  


def home(request):
    return render(request, 'feedapp/home.html')
 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pet_list')  # Redirect to homepage after login
            else:
                messages.error(request, "Invalid username or password.")  # Error message
        else:
            messages.error(request, "Invalid username or password.")  # Error message
    else:
        form = AuthenticationForm()
   
    return render(request, 'feedapp/login.html', {'form': form})
 
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sign up successful! You can now log in.")  # Success message
            return redirect('login')
        else:
            messages.error(request, "Sign up failed. Please correct the errors below.")  # Error message
    else:
        form = UserCreationForm()
   
    return render(request, 'feedapp/signup.html', {'form': form})

def add_dogorcat(request):
    return render(request, 'feedapp/add_dogorcat.html')

@login_required
def add_pet_dog(request):
    if request.method == 'POST':
        pet_name = request.POST.get('name')
        pet_age = request.POST.get('age')
        pet_breed = request.POST.get('breed')
        food_preference = request.POST.get('food_preference')
        feeding_schedule = request.POST.get('feeding_schedule')

        if not all([pet_name, pet_age, pet_breed, food_preference, feeding_schedule]):
            error_message = "All fields are required."
            return render(request, 'feedapp/add_pet_dog.html', {'error_message': error_message})

        Pet.objects.create(
            user=request.user,
            name=pet_name,
            age=pet_age,
            breed=pet_breed,
            food_preference=food_preference,
            feeding_schedule=feeding_schedule,
            pet_type='dog'  # Classify as dog
        )
        return redirect('pet_list')

    return render(request, 'feedapp/add_pet_dog.html', {'pet_type': 'Dog'})

@login_required
def add_pet_cat(request):
    if request.method == 'POST':
        pet_name = request.POST.get('name')
        pet_age = request.POST.get('age')
        pet_breed = request.POST.get('breed')
        food_preference = request.POST.get('food_preference')
        feeding_schedule = request.POST.get('feeding_schedule')

        if not all([pet_name, pet_age, pet_breed, food_preference, feeding_schedule]):
            error_message = "All fields are required."
            return render(request, 'feedapp/add_pet_cat.html', {'error_message': error_message})

        Pet.objects.create(
            user=request.user,
            name=pet_name,
            age=pet_age,
            breed=pet_breed,
            food_preference=food_preference,
            feeding_schedule=feeding_schedule,
            pet_type='cat'  # Classify as cat
        )
        return redirect('pet_list')

    return render(request, 'feedapp/add_pet_cat.html', {'pet_type': 'Cat'})

@login_required
def pet_list(request):
    pets = Pet.objects.filter(user=request.user)  # Only show pets of the logged-in user
    return render(request, 'feedapp/pet_list.html', {'pets': pets})


def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet_list')  # Redirect to the pet list page
    else:
        form = PetForm(instance=pet)

    return render(request, 'feedapp/edit_pet.html', {'form': form, 'pet': pet})

@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, user=request.user)
    if request.method == "POST":
        pet.delete()
        return redirect('pet_list')  # Redirect to the pet list page or another page after deletion
    return render(request, 'feedapp/delete_pet_confirm.html', {'pet': pet})
    
def custom_logout(request):
    return redirect('login') 

@login_required
def profile_view(request):
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')  # Replace 'profile' with the appropriate URL name
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Prevent logout after password change
                return redirect('profile')

    else:
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'feedapp/profile.html', {
        'form': profile_form,
        'password_form': password_form,
    })

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if 'update_profile' in request.POST:  # Check which form was submitted
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')  # Replace 'profile' with your profile page URL name

        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after the password change
                messages.success(request, "Password changed successfully!")
                return redirect('profile')

    else:
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'feedapp/edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required
def manage_feeding_schedule(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, user=request.user)
    feeding_schedule = FeedingSchedule.objects.filter(pet=pet)
    
    context = {
        'pet': pet,
        'feeding_schedule': feeding_schedule,  # List of feeding schedules associated with the pet
    }
    return render(request, 'feedapp/manage_feeding_schedule.html', context)

@login_required
def add_feeding_schedule(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, user=request.user)
    
    if request.method == 'POST':
        time = request.POST.get('time')
        meal_type = request.POST.get('meal_type')
        if time and meal_type:
            FeedingSchedule.objects.create(pet=pet, time=time, meal_type=meal_type)
            return redirect('manage_feeding_schedule', pet_id=pet.id)
        else:
            error_message = "Both time and meal type are required."
            return render(request, 'feedapp/add_feeding_schedule.html', {'pet': pet, 'error_message': error_message})
    
    return render(request, 'feedapp/add_feeding_schedule.html', {'pet': pet})

@login_required
def edit_feeding_schedule(request, schedule_id):
    schedule = get_object_or_404(FeedingSchedule, id=schedule_id, pet__user=request.user)
    
    if request.method == 'POST':
        schedule.time = request.POST.get('time', schedule.time)
        schedule.meal_type = request.POST.get('meal_type', schedule.meal_type)
        schedule.save()
        return redirect('manage_feeding_schedule', pet_id=schedule.pet.id)
    
    return render(request, 'feedapp/edit_feeding_schedule.html', {'schedule': schedule})
