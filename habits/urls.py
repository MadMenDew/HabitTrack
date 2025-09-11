from django.urls import path
from . import views

app_name = "habits"

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_habit, name="create_habit"),
    path("habit/<int:pk>/", views.habit_detail, name="habit_detail"),
    path("habit/<int:pk>/toggle/", views.toggle_completion, name="toggle_completion"),
]

