from dataclasses import dataclass
from datetime import date
from typing import Protocol
from django.contrib import messages

@dataclass
class ToggleResult:
    done: bool
    streak: int

class ToggleComponent(Protocol):
    def run(self, request, habit, today: date) -> ToggleResult: ...

class ToggleCore:
    """Minimal core: flips today's completion and reports result."""
    def __init__(self, toggle_fn, streak_fn):
        self.toggle_fn = toggle_fn      # (habit, today) -> bool
        self.streak_fn = streak_fn      # (habit, today) -> int

    def run(self, request, habit, today: date) -> ToggleResult:
        done_now = self.toggle_fn(habit, today)
        return ToggleResult(done=done_now, streak=self.streak_fn(habit, today))

class BehaviorDecorator:
    """Base decorator that forwards to wrapped and can add side effects."""
    def __init__(self, wrapped: ToggleComponent):
        self.wrapped = wrapped

    def run(self, request, habit, today: date) -> ToggleResult:
        return self.wrapped.run(request, habit, today)

class ReminderBehavior(BehaviorDecorator):
    """If user unchecks a habit, nudge with a gentle reminder."""
    def run(self, request, habit, today: date) -> ToggleResult:
        result = super().run(request, habit, today)
        if not result.done:
            messages.info(request, f"Reminder: “Do {habit.name} later today.”")
        return result

class RewardBehavior(BehaviorDecorator):
    """If user checks a habit, celebrate and show streak."""
    def run(self, request, habit, today: date) -> ToggleResult:
        result = super().run(request, habit, today)
        if result.done:
            if result.streak > 1:
                messages.success(request, f"Nice! Marked done. 🔥 {result.streak}-period streak.")
            else:
                messages.success(request, "Nice! Marked done. Streak starts at 1.")
        return result

def build_pipeline(core: ToggleCore, *, use_reminder=True, use_reward=True) -> ToggleComponent:
    comp: ToggleComponent = core
    if use_reminder:
        comp = ReminderBehavior(comp)
    if use_reward:
        comp = RewardBehavior(comp)
    return comp