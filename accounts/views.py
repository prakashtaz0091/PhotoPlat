from django.shortcuts import render, redirect
from .admin import UserCreationForm
from django.contrib import messages

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