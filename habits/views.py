from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Habit, Completion
from .utils import consecutive_anchors 

def home(request):
    habits = Habit.objects.all().order_by("name")
    return render(request, "habits/home.html", {"habits": habits})

def _current_anchor(habit: Habit, today: date | None = None) -> date:
    # figure out the right anchor for today
    today = today or date.today()
    return habit.anchor_for(today)

def _streak(habit: Habit) -> int:
    # grab all done completions and count run
    done_dates = list(
        Completion.objects.filter(habit=habit, done=True)
        .order_by("-date")
        .values_list("date", flat=True)
    )
    return consecutive_anchors(done_dates) if done_dates else 0

def habit_detail(request, pk: int):
    habit = get_object_or_404(Habit, pk=pk)
    today = date.today()
    anchor = _current_anchor(habit, today)

    completion = Completion.objects.filter(habit=habit, date=anchor).first()
    history = Completion.objects.filter(habit=habit).order_by("-date")[:14]

    context = {
        "habit": habit,
        "anchor": anchor,
        "completion": completion,
        "streak": _streak(habit),
        "history": history,
        "today": today,
    }
    return render(request, "habits/detail.html", context)

def toggle_completion(request, pk: int):
    habit = get_object_or_404(Habit, pk=pk)
    anchor = _current_anchor(habit)

    obj, created = Completion.objects.get_or_create(
        habit=habit, date=anchor, defaults={"done": True}
    )
    if not created:
        obj.done = not obj.done
        obj.save(update_fields=["done"])
        state = "done" if obj.done else "not done"
        messages.info(request, f"{habit.name} set to {state} for {anchor}.")
    else:
        messages.success(request, f"Marked {habit.name} as done for {anchor}.")

    return redirect("habits:habit_detail", pk=habit.pk)
