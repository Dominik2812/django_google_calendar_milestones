# Libs to interact with Google Calendar
from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Libs to make local data readable for Google
import datetime
import os.path
import pickle
import random
import string

# Django Libs
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import BaseListView
from django.views.generic import DeleteView
from django.views.generic.edit import (
    BaseCreateView,
    CreateView,
    TemplateResponseMixin,
    BaseDetailView,
)

# Local import
from .models import Milestone, Goal
from .forms import MileStoneForm


########################################################################
# get access to google calendar
########################################################################

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class AcccessToGoogleCalendar:

    # Creates a "token.pkl" Pickelfile when you first try to get in touch with your Google Calendar.....
    def get_token(self):
        creds = InstalledAppFlow.from_client_secrets_file(
            "milestones_app/client_secret.json", SCOPES
        )
        token = creds.run_local_server(port=0)
        pickle.dump(token, open("token.pkl", "wb"))

    # .....for any future call the token will be simply read from "token.pkl"
    def load_token(self):
        token = pickle.load(open("token.pkl", "rb"))
        return token

    def verify(self):
        if not os.path.exists("token.pkl"):
            self.get_token()
        token = self.load_token()
        enter = build("calendar", "v3", credentials=token)
        return enter


########################################################################
# Methods applicable to Google Calendar Events
########################################################################
class EventManipulation(AcccessToGoogleCalendar):
    def get_events(self):
        enter = self.verify()
        events_result = (
            enter.events()
            .list(
                calendarId="primary",
            )
            .execute()
        )
        events = events_result.get("items", [])
        event_list = []
        for event in events:
            event_list.append(event["id"])
        return event_list

    def create_event(self, goal, title, text, start, end, g_id, color_id):
        enter = self.verify()

        start = str(start).split()[0] + "T" + str(start).split()[1]
        end = str(end).split()[0] + "T" + str(end).split()[1]
        goal_milestone = goal + ":  " + title
        event = {
            "id": g_id,
            "summary": goal_milestone,
            "description": text,
            "colorId": str(color_id),
            "start": {
                "dateTime": start,
                "timeZone": "Europe/Amsterdam",
            },
            "end": {
                "dateTime": end,
                "timeZone": "Europe/Amsterdam",
            },
        }

        e = (
            enter.events()
            .insert(calendarId="primary", sendNotifications=True, body=event)
            .execute()
        )

    def delete_event(self, event_id):
        enter = self.verify()
        enter.events().delete(calendarId="primary", eventId=event_id).execute()


########################################################################
# Views, interacting with objects of local database
########################################################################

# create goals and list then on one page
class GoalsView(BaseCreateView, BaseListView, TemplateResponseMixin):
    fields = ("title", "color_id")
    model = Goal
    template_name = "milestones_app/goals.html"
    success_url = ""

    def get(self, request, *args, **kwargs):
        formView = BaseCreateView.get(self, request, *args, **kwargs)
        listView = BaseListView.get(self, request, *args, **kwargs)
        # print(request)
        # print(args, kwargs)
        formData = formView.context_data["form"]  # form to create  a goal
        listData = listView.context_data["object_list"]  # list of all goals

        # Assign the  goal.color_code depending on which color_id was chosen.
        # This color code is used to mark your goals within your templates.
        # The color_id however assigns a color within Google Calendar.
        hex_color_code = [
            "#039be5",
            "#7986cb",
            "#33b679",
            "#8e24aa",
            "#e67c73",
            "#f6c026",
            "#f5511d",
            "#039be5",
            "#616161",
            "#3f51b5",
            "#0b8043",
            "#d60000",
        ]
        for object in listData:
            object.color_code = hex_color_code[int(object.color_id)]
            object.save()

        return render(
            request,
            self.template_name,
            {"goal_form": formData, "goals": listData},
        )


# Used as a parent class for the MilestoneView
class CreateMileStone(CreateView):
    model = Milestone
    form_class = MileStoneForm


# This view lists all milestones of a chosen goal. milestones can be created here.
class MilestoneShowView(CreateMileStone, BaseDetailView, TemplateResponseMixin):
    model = Goal
    template_name = "milestones_app/goals.html"

    # Create a success_url that includes a variable; here the id of the goal
    def get_success_url(self):
        return reverse("detailGoal", kwargs={"pk": self.object.goal.id})

    # Create an evevnt_id for Google Calendar
    # def generate_event_id(self):
    #     code = ""
    #     for _ in range(10):
    #         code = (
    #             code
    #             + random.choice(string.ascii_lowercase[:15])
    #             + str(random.randint(0, 9))
    #         )
    #     return code

    # Process the request
    def get(self, request, *args, **kwargs):
        print("----------------------------Show")
        create_milestone_form_view = CreateMileStone.get(self, request, *args, **kwargs)
        goal_detail_view = BaseDetailView.get(self, request, *args, **kwargs)

        # kwargs = {}
        # goals_list_view = BaseListView.get(self, request, *args, **kwargs)
        create_milestone_form_data = create_milestone_form_view.context_data["form"]
        goal_detail_data = goal_detail_view.context_data["object"]
        goals_list_data = Goal.objects.all()

        # goals_list_data = goals_list_view.context_data["object"]
        # print(
        #     [element for element in list(goals_list_data)],
        #     type(goal_detail_data),
        #     "listData",
        # )

        # Assign a google calendar event_id to the objects in the database
        for milestone in goal_detail_data.milestones.all():
            milestone.color_id = goal_detail_data.color_id
            if milestone.g_id == None:
                milestone.g_id = self.generate_event_id()
                print("-----------------Im not in there")
                milestone.save()
        return render(
            request,
            self.template_name,
            {
                # "milestone_form": create_milestone_form_data,
                "goal": goal_detail_data,
                "goals": [element for element in list(goals_list_data)],
            },
        )


# This view lists all milestones of a chosen goal. milestones can be created here.
class MilestoneCreateView(
    EventManipulation, CreateMileStone, BaseDetailView, TemplateResponseMixin
):
    model = Goal
    template_name = "milestones_app/create_milestone.html"

    # Create a success_url that includes a variable; here the id of the goal
    def get_success_url(self):
        return reverse("createMilestone", kwargs={"pk": self.object.goal.id})

    # Create an evevnt_id for Google Calendar
    def generate_event_id(self):
        code = ""
        for _ in range(10):
            code = (
                code
                + random.choice(string.ascii_lowercase[:15])
                + str(random.randint(0, 9))
            )
        return code

    # Process the request
    def get(self, request, *args, **kwargs):
        print("Create......................................")
        formView = CreateMileStone.get(self, request, *args, **kwargs)
        detailView = BaseDetailView.get(self, request, *args, **kwargs)
        formData = formView.context_data["form"]
        print(request)

        listData = detailView.context_data["object"]

        # Assign a google calendar event_id to the objects in the database
        for milestone in listData.milestones.all():
            milestone.color_id = listData.color_id
            if milestone.g_id == None:
                milestone.g_id = self.generate_event_id()
                print("-----------------Im not in there")
                title, text, start, end, g_id, color_id = (
                    str(milestone.title),
                    str(milestone.text),
                    milestone.start,
                    milestone.end,
                    str(milestone.g_id),
                    str(milestone.color_id),
                )
                goal = str(milestone.goal)
                self.create_event(goal, title, text, start, end, g_id, color_id)
                milestone.save()
        return render(
            request,
            self.template_name,
            {"milestone_form": formData, "goal": listData},
        )


class DeleteGoalView(EventManipulation, DeleteView):
    model = Goal
    success_url = "/"

    def get(self, request, *args, **kwargs):
        print(Goal.objects.get(id=kwargs["pk"]).milestones.all())
        adhered_milestones = [
            stone.g_id for stone in Goal.objects.get(id=kwargs["pk"]).milestones.all()
        ]
        # print(adhered_milestones)
        for g_id in adhered_milestones:
            if g_id in self.get_events():
                self.delete_event(g_id)
        return self.post(request, *args, **kwargs)


class DeleteMileStoneView(EventManipulation, DeleteView):
    model = Milestone

    def get_success_url(self):
        return reverse("detailGoal", kwargs={"pk": self.object.goal.id})

    def get(self, request, *args, **kwargs):
        # print("delete", self, request, args, kwargs, kwargs["pk"])
        # print([stone.g_id for stone in Milestone.objects.all()])
        # print(Milestone.objects.get(id=kwargs["pk"]).g_id)
        g_id = Milestone.objects.get(id=kwargs["pk"]).g_id
        if g_id in self.get_events():
            self.delete_event(g_id)
        return self.post(request, *args, **kwargs)


# #######################################################################
# Views, interacting with objects of local database
# #######################################################################

# Calling this view projects all milestones from the database to Google Calendar. Events that cannot be found in the database will be deleted.
# class SynchronizeView(EventManipulation, MilestoneShowView):
#     def synchronize(self):
#         db_milestones = Milestone.objects.all()
#         google_milestones = self.get_events()

#         Send the milestone from database to google calendar
#         if len(db_milestones) > len(google_milestones):
#             for milestone in db_milestones:
#                 if str(milestone.g_id) not in google_milestones:
#                     title, text, start, end, g_id, color_id = (
#                         str(milestone.title),
#                         str(milestone.text),
#                         milestone.start,
#                         milestone.end,
#                         str(milestone.g_id),
#                         str(milestone.color_id),
#                     )
#                     goal = str(milestone.goal)
#                     self.create_event(goal, title, text, start, end, g_id, color_id)

#         Delete all events in google calendar that are not in teh database
#         else:
#             Filter  out the google calendar ids
#             db_milestones = [str(milestone.g_id) for milestone in db_milestones]
#             for milestone in google_milestones:
#                 if milestone not in db_milestones:
#                     self.delete_event(milestone)

#     def get(self, request, *args, **kwargs):
#         formView = CreateMileStone.get(self, request, *args, **kwargs)
#         detailView = BaseDetailView.get(self, request, *args, **kwargs)
#         formData = formView.context_data["form"]
#         listData = detailView.context_data["object"]
#         for milestone in listData.milestones.all():
#             milestone.color_id = listData.color_id
#             if milestone.g_id == None:
#                 milestone.g_id = self.generate_event_id()
#                 milestone.save()
#         self.synchronize()

#         return render(
#             request,
#             self.template_name,
#             {"milestone_form": formData, "goal": listData},
#         )
