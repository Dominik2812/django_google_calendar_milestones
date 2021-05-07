# google_calendar_milestones

## What are milestones about?

* Use a fake google calendar to break problems, challenges and projects into milestones.

* Formulate your goals.

![loadData](pics/goals.png?raw=true "loadData")


* Go to milestones and create the necessary steps to reach your goal; the milestones.

![loadData](pics/milestones.png?raw=true "loadData")


* synchronize your local database with your Google Calendar and send all milestones. An " on-demand " data transfer is preferred as you might first want to brainstorm about your milestones before transferring them. 

* View your milestones as events on your Google Calendar, their color code relates to the goals they are linked to.

![loadData](pics/calendar.png?raw=true "loadData")

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
* The color_id attribute of the **Goal** class is used to color events in your Google Calendar. It must be manually selected by the user. The choices are stored within the COLOR list in the* models.py *. The color_id attribute of the ** Milestone ** class automatically corresponds to the one of ** Goal **.  
* The attribute color_code is calculated from color_id and is used to color-code the HTML elements in your template files. 
![loadData](pics/model.png?raw=true "loadData")
### forms.py
Despite having two model classes only one from class is used: MileStoneForm. The reason to use the MileStoneForm class was the design of the DataInput fields, which look nicer with the form model. 
### views.py
The * views.py * consists of four major parts:
* The **AccessToGoogleCalendar** class established the connection to your Google Calendar. On the first call, you will be redirected to a consent screen, where you permit access. Thereby a "token.pkl" is created and locally stored in your project directory. The token will then be used to access Google Calendar in all future calls.

![loadData](pics/access.png?raw=true "loadData")

* The **EventManipulation** class that enables the app to list, create and delete Google Calendar events.

* The third part consists of all the View classes to list, create and delete objects from the database. 

  * To display the list of objects as well as the creation form in the same template, the *get* method of the **GoalsView** as well as the **MilestoneView** has been modified in the following manner.
  
  ![loadData](pics/create_list.png?raw=true "loadData")
  
  * The *success_url* attribute of the **DeleteMileStoneView** class is modified to stay on the same page by the *get_success_url* method.
  
  ![loadData](pics/delete.png?raw=true "loadData")
  
* Finally the **SynchronizeView**  queries all milestones from the database and mirrors them as Google Calendar events. Eventually, events that do not have an equivalent milestone in the database are deleted. This view applies in the method *synchronize* all the methods that are inherited from the **Eventmanipulation** class. As it also inherits from the **MilestoneView**, the *get* method will render the '"milestones_app/detail_goal.html" template. 

![loadData](pics/synchronize.png?raw=true "loadData")

### optional iframes
In the templates *goals.html* and *detail_goal.html* an iframe is commented out with which you couldd potenitally display the google calendar directly to the template. It is however not possible to see the color-coding in this iframe, which I thought is lame and not in the spirit of the project. 
