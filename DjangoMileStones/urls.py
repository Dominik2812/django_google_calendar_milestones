"""DjangoMileStones URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from milestones_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.GoalsView.as_view(), name="goals"),
    path("/delete/<int:pk>", views.DeleteGoalView.as_view(), name="deleteGoal"),
    path("/detail/<int:pk>", views.MilestoneShowView.as_view(), name="detailGoal"),
    path(
        "/create/<int:pk>", views.MilestoneCreateView.as_view(), name="createMilestone"
    ),
    path("/synchronize/<int:pk>", views.SynchronizeView.as_view(), name="synchronize"),
    path("milestones", include("milestones_app.urls"), name="milestones"),
]
