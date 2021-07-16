from django.urls import path
from . import views

app_name = "milestones_app"
urlpatterns = [
    path("/delete/<int:pk>", views.DeleteGoalView.as_view(), name="delete_goal"),
    path(
        "/delete/milestone/<int:pk>",
        views.DeleteMilestoneView.as_view(),
        name="delete_milestone",
    ),
]
