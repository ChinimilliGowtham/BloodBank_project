from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('add_new_donor/', views.add_donor, name='add_new_donor'),
    path('fetch_all_donor_details/', views.fetch_all_donor_details, name='fetch_all_donor_details'),  # New URL pattern
    path('update_donor/', views.update_donor, name='update_donor'),
    path('', views.home, name='home'),
]
