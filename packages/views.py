from django.shortcuts import render, redirect
from packages.forms import PackageForm
from main.models import Package


def packages(request):
    # packages = Package.objects.filter(
    #     photographer=request.user.profile
    # ) 
    packages = Package.objects.for_profile(request.user.profile)
    
    # in above cases, both does same work, we just kept the filter logic inside for_profile method in manager
    
    context = {
        'packages': packages,
        'currency_display_text': request.user.profile.get_currency_display
    }
    return render(request, "packages/packages.html", context)


def packages_create(request):
    form = PackageForm(request.POST or None)
    if form.is_valid():
        pkg = form.save(commit=False)
        pkg.photographer = request.user.profile
        pkg.save()
        return redirect('packages_page')
    context = {
        'form': form,
        'currency_display_text': request.user.profile.get_currency_display
    }
    return render(request, "packages/packages-form.html", context)