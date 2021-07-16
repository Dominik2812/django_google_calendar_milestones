from random import choices
from django import forms
from django.forms import ModelForm
from django.forms.widgets import DateTimeBaseInput, TextInput, Textarea

from .models import Goal, Milestone, COLORS


class DateInput(forms.DateInput):
    input_type = "datetime-local"


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = ["title", "color_id"]
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control w-100 m-3",
                    "placeholder": "name your Milestone",
                    "required": "True",
                }
            ),
            "color_id": forms.Select(
                attrs={
                    "class": "form-control w-100 m-3",
                    "cols": "20",
                    "rows": "auto",
                    "placeholder": "Any important Notes? ",
                },
                choices=COLORS,
            ),
        }


class MileStoneForm(ModelForm):
    class Meta:
        model = Milestone
        fields = ["title", "text", "start", "end", "goal"]
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control w-100 m-3",
                    "placeholder": "name your Milestone",
                    "required": "True",
                }
            ),
            "text": Textarea(
                attrs={
                    "class": "form-control w-100 m-3",
                    "cols": "20",
                    "rows": "auto",
                    "placeholder": "Any important Notes? ",
                }
            ),
            "start": DateInput(
                attrs={
                    "class": "form-control w-100 m-3",
                    "required": "True",
                }
            ),
            "end": DateInput(
                attrs={
                    "class": "form-control w-100 m-3",
                    "required": "True",
                }
            ),
            "goal": forms.Select(
                attrs={
                    "class": "form-control w-100 m-3",
                    "required": "True",
                }
            ),
        }
