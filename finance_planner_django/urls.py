from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("incomes/", include("incomes.urls")),
    path("expenses/", include("expenses.urls")),
    path("budgets/", include("budgets.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = "homepage.views.page_not_found"
