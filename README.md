# google_calendar_milestones
### a fullstack API that enables you to chop your Big Goals into mini tasks.

## What are Milestones?

A Django Class Based Views API, that enables you to use your google calendar to approach goals, challenges and projects step by step: Break them into feasible milestones.

* Formulate your goals and color code them.

<p align="center">
  <img src="pics/create_goals.png" width="500" />
</p>



* Create the necessary steps to reach your goal; the milestones. Set a start and an end date and if necessary add a note to the milestone.
<p align="center">
  <img src="pics/create_milestones.png" width="500" />
</p>

* Comfortably switch between the goals or projects and consider their milestones
*
<p align="center">
  <img src="pics/show_milestones.png" width="500" />
</p>

* View your milestones as events on your Google Calendar, their color code relates to the goals they are linked to.

<p align="center">
  <img src="pics/calendar.png" width="500" />
</p>

Please note: The project is an ongoing permanent experiment in which I am trying different techniques (CBV vs. query approach), layouts (several views vs. one view) and designs (colors, size and positioning). Features such as error handling and updateviews are not yet included to facilitate modifications.
Currently there are two versions of this project: The main branch is what this Readme file is all about. The branch *creation_and_list_with_queries* is a little modified and basically displays the lists and creation views of both, Goals and Milestones on one page. 

## First steps: get access to google calendar
To use this app you need to communicate with your Google calendar. For that please follow these steps:
* create a new Google Calendar and call it Milestones. For security reasons do not use your personal Calendar. All Events that are not in your local database will be deleted. The Milestones Calendar can be displayed along with your personal Calendar. 

* go to Google Cloud Platform:
* create a google developers 
* then search for Google Calendar API
* enable the API
* go to Create Credentials:
  * create an OAuth-Consent Screen:
    * choose external
    * push create
  * choose  your Scopes:
    * Google Calendar :
      *"https://www.googleapis.com/auth/calendar"
  * register yourself as a Test user:
* back to Credentials:
  * create Credentials
    * create OAUthClient ID:
      * choose Desktop Application
  * Download your client_id.json


## Remarks on the code
### models. py
Two object classes are defined in *models.py*; **Goal** and **Milestone**, the latter linked with a Foreigneky to the first. In the following two important attributed color_id and color_code will be explained.
* The color_id attribute of the **Goal** class is used to color events in your Google Calendar. It must be manually selected by the user. The choices are stored within the COLOR list in the* models.py *. The color_id attribute of the **Milestone** class automatically corresponds to the one of **Goal**.  
* The attribute color_code is calculated from color_id and is used to color-code the HTML elements in your template files. 

<p align="center">
  <img src="pics/model.png" width="500" />
</p>



### forms.py
Despite having two model classes only one from class is used: MileStoneForm. The reason to use the MileStoneForm class was the design of the DataInput fields, which look nicer with the form model. 
### views.py
The *views.py* consists of three major parts:

* The **AccessToGoogleCalendar** class established the connection to your Google Calendar. On the first call, you will be redirected to a consent screen, where you permit access. Thereby a "token.pkl" is created and locally stored in your project directory. The token will then be used to access Google Calendar in all future calls.

<p align="center">
  <img src="pics/access.png" width="500" />
</p>

* The **EventManipulation** class that enables the app to list, create and delete Google Calendar events. Methods from the **AccessToGoogleCalendar** class are inherited.

* The third part consists of all the View classes to list, create and delete objects from the database. Those Views inherit from the previous parts **Eventmanipulation** and thereby from the **AccessToGoogleCalendar** class. There are three major views. The GoalsView, enables you to create a goal and lists all former goals to the right. The MilestoneCreateView does the same for Milestone objects. The MilestoneShowView enables you to comfortably display all Milestones of a certain Goal, with the list of Goals on the left and the list of Milestones on the right. 

* All those views combine a form to create an object and a list of either the same species or yet another object class. This is achieved by inheriting from different Django classes  **BaseCreateView, BaseListView, TemplateResponseMixin** for the **GoalsView** and **BaseDetailView, TemplateResponseMixin** for the **MilestoneShowView**. 

* The **MilestoneCreateView** inherits from the **CreateMilestone** instead of the **BaseCreateView** as the form has to be costumized (does not contain the *g_id* and *goals* attribut).
* To eventually display the list of objects as well as the creation form in the same template, the *get* methods are modified. An empty form is created by **BaseCreateview** or **CreateMilestone**. The lists are however queried in different ways: In the **GoalsView** by the **BaseListView** class. In the **MilestoneShowView** the Milestones are contained by the **BaseDetailView** of the considered Goal, whereas the Goals list is obtained by an ordinary query *Goal.objects.all()*. 
  
 <p align="center">
  <img src="pics/MilestoneShowView.png" width="500" />
</p>

  
* The only error that occurred during the development of this app in the **MilestoneCreateView** when the end date of the milestone was set before the start date. Google Calendar rejects this request and to avoid that the app crashes the *post* method of the milestoneCreateView will remind you of the incoherent input data.



* The **DeleteGoalView** and **DeleteMilestoneView** contain modified *get* methods to not only delete the Milestone from the local database but also the equivalent event in your calendar. In addition, the *success_url* attribute of the **DeleteMileStoneView** class is modified to stay on the same page by the *get_success_url* method.

  <p align="center">
  <img src="pics/DeleteMilestoneView.png" width="500" />
</p>

* An additional **SynchronizeView** enables you to adapt your local database if events in the Google Calendar have been deleted.

### optional iframe
In the template*milestones_list.html* an iframe is commented out with which you could potentially display the google calendar directly to the template. It is however not possible to see the color-coding in this iframe, which I thought is lame and not in the spirit of the project. 
