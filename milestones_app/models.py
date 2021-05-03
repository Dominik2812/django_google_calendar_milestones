from django.db import models
from django.urls import reverse

# For the drop down menu
COLORS = [
    ("0", "who knows"),
    ("1", "Lavender"),
    ("2", "Sage"),
    ("3", "Grape"),
    ("4", "Flamingo"),
    ("5", "	Banana"),
    ("6", "Tangerine"),
    ("7", "Peacock"),
    ("8", "	Graphite"),
    ("9", "Blueberry"),
    ("10", "Basil"),
    ("11", "Tomato"),
]


class Goal(models.Model):
    title = models.CharField(max_length=200)
    color_id = models.CharField(max_length=33, default="0", choices=COLORS)
    color_code = models.CharField(max_length=33, default="#039be5")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("goals")


class Milestone(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
        default="Why I chose this to be my first Milestone:",
    )

    start = models.DateTimeField(
        null=True,
        blank=True,
    )
    end = models.DateTimeField(
        null=True,
        blank=True,
    )

    goal = models.ForeignKey(
        Goal,
        null=True,
        blank=True,
        related_name="milestones",
        db_column="goal",
        on_delete=models.CASCADE,
    )

    g_id = models.CharField(max_length=200, null=True, blank=True)

    color_id = models.CharField(max_length=3, default="0")
    color_code = models.CharField(max_length=3, default="#039be5")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("goals")
