from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("accounts/", include("accounts.urls")),
    path("packages/", include("packages.urls")),
    path("bookings/", include("bookings.urls")),
    path("subscriptions/", include("subscriptions.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


