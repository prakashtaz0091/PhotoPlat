from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # for language switch
    path('api/', include("packages_api.urls")),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]


if settings.DEBUG == True:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("accounts/", include("accounts.urls")),
    path("packages/", include("packages.urls")),
    path("bookings/", include("bookings.urls")),
    path("subscriptions/", include("subscriptions.urls")),
)


