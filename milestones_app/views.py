# Libs to interact with Google Calendar
from __future__ import print_function
from django.http.response import HttpResponse
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
from django.http import HttpResponseRedirect
from django.views.generic.list import BaseListView, ListView
from django.views.generic import DeleteView
from django.views.generic.edit import (
    View,
    BaseCreateView,
    CreateView,
    TemplateResponseMixin,
    BaseDetailView,
    FormView,
)
from django.views.generic.detail import SingleObjectMixin

# Local import
from .models import Milestone, Goal
from .forms import MileStoneForm, GoalForm


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

        # start = str(start).split()[0] + "T" + str(start).split()[1]
        # end = str(end).split()[0] + "T" + str(end).split()[1]
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
class GoalsView(CreateView, ListView, TemplateResponseMixin):  # BaseListView,
    fields = ("title", "color_id")
    model = Goal
    template_name = "milestones_app/combined_view.html"
    success_url = ""

    def get(self, request, *args, **kwargs):
        print(request.GET, args, kwargs)
        form_view = CreateView.get(self, request, *args, **kwargs)
        form_data = form_view.context_data["form"]  # form to create a goal
        list_view = ListView.get(self, request, *args, **kwargs)
        print(list_view.context_data)
        list_data = list_view.context_data["object_list"]  # list of all goals

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
        for object in list_data:
            object.color_code = hex_color_code[int(object.color_id)]
            object.save()

        return render(
            request,
            self.template_name,
            {
                "goal_form": form_data,
                "goals": list_data,
            },
        )


class CombinedCreateView(
    SingleObjectMixin,
    FormView,
    EventManipulation,
):
    template_name = "milestones_app/combined_view.html"

    # Create a success_url that includes a variable; here the id of the goal
    # def get_success_url(self):
    #     return reverse("combined", kwargs={"pk": self.object.goal.id})

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

        milestone_form = MileStoneForm()
        goal_form = GoalForm()
        goal = Goal.objects.get(id=kwargs["pk"])
        milestones = goal.milestones.all()
        goals = Goal.objects.all()

        context = {
            "milestone_form": milestone_form,
            "goal": goal,
            "goals": goals,
            "milestones": milestones,
            "goal_form": goal_form,
        }

        return render(
            request,
            self.template_name,
            context,
        )

    def post(self, request, *args, **kwargs):
        context = kwargs
        print(request.POST)
        # print(context)
        # print("create_goal" in request.POST, request.POST["create_goal"])
        if "create_goal" in request.POST:
            new_goal = Goal()
            new_goal.title, new_goal.color_id = (
                request.POST["title"],
                request.POST["color_id"],
            )
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
            new_goal.color_code = hex_color_code[int(new_goal.color_id)]
            new_goal.save()
        else:
            new_milestone = Milestone()
            (
                new_milestone.title,
                new_milestone.text,
                new_milestone.start,
                new_milestone.end,
                new_milestone.goal,
                new_milestone.g_id,
            ) = (
                request.POST["title"],
                request.POST["text"],
                request.POST["start"],
                request.POST["end"],
                Goal.objects.get(id=request.POST["goal"]),
                self.generate_event_id(),
            )
            print(
                "create",
                (
                    str(new_milestone.goal),
                    str(new_milestone.title),
                    str(new_milestone.text),
                    new_milestone.start,
                    new_milestone.end,
                    str(new_milestone.g_id),
                    str(new_milestone.color_id),
                ),
            )

            self.create_event(
                str(new_milestone.goal),
                str(new_milestone.title),
                str(new_milestone.text),
                new_milestone.start + ":00",
                new_milestone.end + ":00",
                str(new_milestone.g_id),
                str(new_milestone.color_id),
            )

            print("create")
            new_milestone.color_code = new_milestone.goal.color_code

            print("create")
            new_milestone.save()
            print("create")

        milestone_form = MileStoneForm()
        goal_form = GoalForm()
        goal = Goal.objects.get(id=kwargs["pk"])
        milestones = goal.milestones.all()
        goals = Goal.objects.all()

        context = {
            "milestone_form": milestone_form,
            "goal": goal,
            "goals": goals,
            "milestones": milestones,
            "goal_form": goal_form,
        }

        return render(
            request,
            self.template_name,
            context,
        )


class DeleteGoalView(EventManipulation, DeleteView):
    model = Goal
    success_url = "/"

    def get(self, request, *args, **kwargs):
        adhered_milestones = [
            stone.g_id for stone in Goal.objects.get(id=kwargs["pk"]).milestones.all()
        ]
        for g_id in adhered_milestones:
            if g_id in self.get_events():
                self.delete_event(g_id)
        return self.post(request, *args, **kwargs)


class DeleteMilestoneView(EventManipulation, DeleteView):
    model = Milestone

    def get_success_url(self):
        return reverse("combined", kwargs={"pk": self.object.goal.id})

    def get(self, request, *args, **kwargs):
        g_id = Milestone.objects.get(id=kwargs["pk"]).g_id
        if g_id in self.get_events():
            self.delete_event(g_id)
        return self.post(request, *args, **kwargs)
