from django.db import models
from datetime import date
from .utils import period_anchor_for

class Habit(models.Model):
    name = models.CharField(max_length=100)
    habit_type = models.CharField(max_length=10, choices=[("daily", "Daily"), ("weekly", "Weekly")])
    strategy = models.CharField(max_length = 10, choices=[("strict", "Strict"), ("flexible", "Flexible")] )
    
    def __str__(self):
        return self.name
    
    def anchor_for(self, d: date) -> date:
        # wrapper so views don’t repeat logic
        return period_anchor_for(self.habit_type, d)

class Completion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="completions")
    date = models.DateField()          # daily: actual day; weekly: anchor day (Monday)
    done = models.BooleanField(default=False)

    class Meta:
        unique_together = ("habit", "date")   # one row per habit per period
        ordering = ["-date"]