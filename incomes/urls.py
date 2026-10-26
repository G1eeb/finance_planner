from django.urls import path
from . import views

app_name = "incomes"

urlpatterns = [
    path("", views.incomes, name="list"),
    path("filter/", views.income_filter, name="filter"),
    path("statistics/", views.income_statistics, name="statistics"),
    path("<int:income_id>/", views.income_detail, name="detail"),
]
