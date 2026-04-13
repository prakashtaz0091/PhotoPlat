from django.shortcuts import render, redirect
from .admin import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def logout_view(request):
    logout(request)
    return redirect("login_page")

def login_view(request):
    
    if request.method == "POST":
        print(request.POST)
        user = authenticate(request,
                            email=request.POST.get("email"),
                            password=request.POST.get("password")
                            )
        if user is not None:
            # actual user handling
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home_page")
        else:
            # user doesn't exist handling
            messages.error(request, "User with these credentials doesn't exist")
            return redirect("login_page")
    
    return render(request, "accounts/login.html")
    
def register(request):
    # If post request, post request in this view means, user is trying to submit registeration form
    if request.method == "POST":
        print("this is post request", request.POST)
        submitted_form = UserCreationForm(request.POST)
        
        if submitted_form.is_valid():
            submitted_form.save()
            messages.success(request, "Registration successful. Please login and complete the verification process")
        else:
            print("-----------No it's not valid")
            
        return redirect("home_page")
    
    # If get request, give the registration page
    return render(request, "accounts/register.html")