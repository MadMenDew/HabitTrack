from django.db import models

class Habit(models.Model):
    name = models.CharField(max_length=100)
    habit_type = models.CharField(max_length=10, choices=[("daily", "Daily"), ("weekly", "Weekly")])
    strategy = models.CharField(max_length = 10, choices=[("strict", "Strict"), ("flexible", "Flexible")] )
    