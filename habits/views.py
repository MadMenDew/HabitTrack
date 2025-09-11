from django.urls import reverse
from .forms import HabitForm


from datetime import date, timedelta
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

def _window_anchors(habit: Habit, today: date | None = None) -> list[date]:
    # build the list of period anchors we grade against
    today = today or date.today()
    start = habit.anchor_for(today)  # day or Monday
    if habit.habit_type == "daily":
        # last 7 days, newest first
        return [start - timedelta(days=i) for i in range(7)]
    else:
        # last 4 weeks by Monday anchors, newest first
        return [start - timedelta(days=7*i) for i in range(4)]

def _progress(habit: Habit, today: date | None = None) -> dict:
    # compute counts + pass/fail for strategy
    anchors = _window_anchors(habit, today)
    done_set = set(
        Completion.objects.filter(habit=habit, date__in=anchors, done=True)
        .values_list("date", flat=True)
    )
    marks = [(a, a in done_set) for a in anchors]  # keep order
    total = len(anchors)
    done_count = sum(1 for _, is_done in marks if is_done)
    pct = done_count / total if total else 0.0

    if habit.strategy == "strict":
        on_track = (done_count == total)
        rule_label = "Strict (all required)"
    else:
        on_track = (pct >= 0.70)  # 70% passes
        rule_label = "Flexible (≥70%)"

    window_label = "Last 7 days" if habit.habit_type == "daily" else "Last 4 weeks"

    return {
        "window_label": window_label,
        "rule_label": rule_label,
        "marks": marks,                # list[(date, bool)] newest -> oldest
        "done_count": done_count,
        "total": total,
        "percent": round(pct * 100),   # whole number percent
        "on_track": on_track,
    }

def habit_detail(request, pk: int):
    habit = get_object_or_404(Habit, pk=pk)
    today = date.today()
    anchor = _current_anchor(habit, today)

    completion = Completion.objects.filter(habit=habit, date=anchor).first()
    history = Completion.objects.filter(habit=habit).order_by("-date")[:14]

    progress = _progress(habit, today)

    context = {
        "habit": habit,
        "anchor": anchor,
        "completion": completion,
        "streak": _streak(habit),
        "history": history,
        "today": today,
        "progress": progress,           

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

def create_habit(request):
    # GET: blank form; POST: validate + save
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save()  # creates Habit row
            messages.success(request, f"Created habit: {habit.name}.")
            return redirect(reverse("habits:habit_detail", args=[habit.pk]))
    else:
        form = HabitForm()
    return render(request, "create.html", {"form": form})
