from django.shortcuts import render
from accounts.models import Profile, Speciality
from django.db.models import Count, Q

def home(request):
    
    photographers = Profile.objects.filter(kyc_verified="verified", email_verified="verified")
    # Here photographers is just a prepared query, it doesn't hits database yet. It's lazy.
    
    specialities = Speciality.objects.annotate(
        profile_count=Count("profiles", filter=Q(profiles__kyc_verified=Profile.KYC_STATUS.VERIFIED, profiles__email_verified=Profile.EMAIL_STATUS.VERIFIED), distinct=True)
    )
    context = {
        'photographers': photographers,
        'specialities': specialities
    }
    
    return render(request, "main/home.html", context)
