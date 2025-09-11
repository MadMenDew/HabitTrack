# habits/forms.py
from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    # nicer label and placeholder
    name = forms.CharField(
        label="Habit name",
        widget=forms.TextInput(attrs={"placeholder": "ex) Read 10 pages"}),
        max_length=100,
    )

    class Meta:
        model = Habit
        fields = ["name", "habit_type", "strategy"]
        widgets = {
            "habit_type": forms.RadioSelect,
            "strategy": forms.RadioSelect,
        }

    def clean_name(self):
        # trim spaces
        return self.cleaned_data["name"].strip()
