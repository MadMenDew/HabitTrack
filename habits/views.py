from django.shortcuts import render
from .models import Habit

def home(request):
    habits = Habit.objects.all()
    return render(request, "habits/home.html", {"habits": habits})
