from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DonorForm
from .models import Donor
from django.http import JsonResponse

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        age = request.POST.get('age')
        phonenumber = request.POST.get('phonenumber')
        address = request.POST.get('address')
        
        try:
            # Create a new user instance
            user = User.objects.create_user(username=username, password=password)
            
            # Set additional user attributes
            user.profile.age = age
            user.profile.phonenumber = phonenumber
            user.profile.address = address
            
            # Save the user instance
            user.save()
            
            # Automatically log in the newly registered user
            user = authenticate(request, username=username, password=password)
            login(request, user)
            
            # Redirect to the home page or any desired page
            return redirect('/')
        except Exception as e:
            # Handle registration failure
            messages.error(request, 'Failed to register. Please try again later.')
    
    return render(request, 'register.html')

@login_required
def add_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user  # Assign the donor to the current user
            donor.save()
            return JsonResponse({'success': True, 'donor_added': True})  # Indicate success and donor added
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)  # Return errors if form is invalid
    else:
        form = DonorForm()
    
    return render(request, 'home.html', {'donor_form': form})

@login_required
def fetch_all_donor_details(request):
    donors = Donor.objects.all()
    donors_data = [
        {
            'name': donor.name,
            'father_name': donor.father_name,
            'mother_name': donor.mother_name,
            'date_of_birth': donor.date_of_birth,
            'age': donor.age,
            'mobile_number': donor.mobile_number,
            'blood_group': donor.blood_group,
            'city': donor.city,
            'address': donor.address
        } for donor in donors
    ]
    return JsonResponse({'donors': donors_data})

@login_required
def update_donor(request, donor_id):
    donor = Donor.objects.get(id=donor_id)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Donor details updated successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = DonorForm(instance=donor)
    
    return render(request, 'update_donor.html', {'form': form})


def home(request):
    return render(request, 'home.html')

def user_logout(request):
    logout(request)  # Logout the user
    return redirect('login')