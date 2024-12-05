
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('add_dogorcat/', views.add_dogorcat, name='add_dogorcat'),
    path('add_pet_dog/', views.add_pet_dog, name='add_pet_dog'),
    path('add_pet_cat/', views.add_pet_cat, name='add_pet_cat'),
    path('pet_list/', views.pet_list, name='pet_list'),   
    path('edit_pet/<int:pet_id>/', views.edit_pet, name='edit_pet'),
    path('delete_pet/<int:pet_id>/', views.delete_pet, name='delete_pet'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('manage-feeding-schedule/<int:pet_id>/', views.manage_feeding_schedule, name='manage_feeding_schedule'),
    path('add-feeding-schedule/<int:pet_id>/', views.add_feeding_schedule, name='add_feeding_schedule'),
    path('edit-feeding-schedule/<int:schedule_id>/', views.edit_feeding_schedule, name='edit_feeding_schedule'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)