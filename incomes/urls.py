from django.urls import path
from . import views

app_name = "incomes"

urlpatterns = [
    path("", views.incomes, name="list"),
    path("<int:income_id>/", views.income_detail, name="detail"),
]
