from django.urls import path
from . import views

app_name = "milestones_app"
urlpatterns = [
    path("/delete/<int:pk>", views.DeleteGoalView.as_view(), name="delete_goal"),
    path("/detail/<int:pk>", views.MilestoneShowView.as_view(), name="detail_goal"),
    path("/delete/milestone/<int:pk>", views.DeleteMileStoneView.as_view(), name="delete_milestone"),
    path(
        "/create/<int:pk>", views.MilestoneCreateView.as_view(), name="create_milestone"
    ),

    path("/synchronize", views.SynchronizeView.as_view(), name="synchronize"),
    
]
