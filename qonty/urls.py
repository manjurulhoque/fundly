from django.contrib import admin
from django.urls import path, include

from qonty import settings
from dashboard.views.admin_views import AdminDashboardView, AdminCampaignsView

urlpatterns = [
    path("super-admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("campaign/", include("campaign.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("", include("core.urls")),
    path(
        "admin/",
        include("dashboard.admin_urls"),
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
