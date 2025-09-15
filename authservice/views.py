from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        print(mobile_number, password)

        # Authenticate user using mobile number and password
        user = authenticate(request, username=mobile_number, password=password)

        if user is not None:
            # Log the user in correctly
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('core_service:entry_view')  # Replace with your actual dashboard URL
        else:
            messages.error(request, 'Invalid mobile number or password.')

    return render(request, 'pages/auth/login.html')

def user_logout(request):
    # Log the user out
    logout(request)

    # Display a success message
    messages.success(request, 'You have successfully logged out.')

    # Redirect to the login page
    return redirect('auth_service:login')  # Or redirect to another page like 'home'

def registration_step_01(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        role = request.POST.get('role')
        return redirect('auth_service:registration-step-02', mobile_number=mobile_number, role=role)
    return render(request,'pages/auth/registraion/step_01.html',context={})
def registration_step_02(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        otp = request.POST.get('role')
        return redirect('auth_service:registration-step-03', mobile_number=mobile_number)
    return render(request,'pages/auth/registraion/step_02.html',context={})

def registration_step_03(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        return redirect('auth_service:login')
    return render(request,'pages/auth/registraion/step_03.html',context={})
