from django.urls import path
from . import views

app_name = "milestones_app"
urlpatterns = [
    path("/delete/<int:pk>", views.DeleteMileStoneView.as_view(), name="deleteMileStone"),
]
