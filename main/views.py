from django.shortcuts import render, redirect
from accounts.models import Profile, Speciality
from django.db.models import Count, Q
from django.contrib import messages


# http://127.0.0.1:8000
# http://127.0.0.1:8000/?category=all
# http://127.0.0.1:8000/?category=wedding
# http://localhost:8000/?speciality=corporate&max_price=5000
def home(request):
    photographers = Profile.objects.filter(kyc_verified="verified", email_verified="verified")
    speciality_slug = request.GET.get('speciality')
    
    # filter by speiciality
    if speciality_slug is not None and speciality_slug != "all":
        speciality = Speciality.objects.get(slug=speciality_slug)
        photographers = photographers.filter(specialities=speciality)   

    # filter by per day fee max 
    if request.GET.get('max_price') is not None and len(request.GET.get('max_price')) != 0:
        try:
            max_price_param = int(request.GET.get('max_price'))
        except (ValueError, TypeError):
            messages.error(request, "Please provide correct price value")
            return redirect('home_page')
        else:
            if max_price_param < 0:
                messages.warning(request, "Per day fee cannot be less than 0")
                return redirect('home_page')
            
            photographers = photographers.filter(per_day_fee__lte=max_price_param)
    
    # Here photographers is just a prepared query, it doesn't hits database yet. It's lazy.
    
    specialities = Speciality.objects.annotate(
        profile_count=Count("profiles", filter=Q(profiles__kyc_verified=Profile.KYC_STATUS.VERIFIED, profiles__email_verified=Profile.EMAIL_STATUS.VERIFIED), distinct=True)
    )
    context = {
        'photographers': photographers,
        'specialities': specialities
    }
    
    return render(request, "main/home.html", context)
