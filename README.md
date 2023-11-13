# ToDo List Manager
#### Video Demo: https://youtu.be/5HPfT2VQ_Qo
#### Description:
The **ToDo List Manager** is a simple yet powerful application for managing
tasks. It allows you to add, delete, and update tasks, as well as filter and
search tasks. You can also mark tasks as unstarted(ToDo), in progress, or completed,
and add a description to each task.
The ToDo List Manager is built using the Tkinter library for the GUI and
SQLite3 for storing the tasks.

## Key Features
The Task App offers a variety of features to help you stay organized and on top
of your tasks, including:

* **Task management:** Add, delete, and update tasks with ease.
* **Task filtering:** Filter tasks by status, due date, or both to find the
tasks you need to work on quickly and easily.
* **Task searching:** Search tasks by title to find the specific task you're
looking for.
* **Task prioritization:** Mark tasks as unstarted (ToDO), in progress, or completed
to prioritize your work and stay focused on the most important tasks.
* **Task descriptions:** Add a description to each task to provide more context
and information.
* **Overdue task tracking:** View a list of all overdue tasks, so you can
easily see which tasks are past their due date and need to be completed.
* **Task sorting:** Sort tasks by ID or due date, in ascending or descending
order.

## App Structure

The ToDo List Manager is structured using classes. There are classes for the
frames, a database class, a settings class for sharing objects, widget
references and variables around the frames and a style class.

**Frame classes:**

Each frame in the app has its own class. This allows for modularity and code
reuse. For example, the `MasterFrame` class contains all of the code for the
master frame of the app, while the `UpperFrame` class contains all of the code
for the upper frame in a paned window.

**DataManager class:**

The `DataManager` class handles all of the interactions with the SQLite3
database. This includes creating the database, inserting, updating, and
deleting data from the database, and querying the database.

**AppSettings class:**

The `AppSettings` class is used to share objects, widget references, and
function references around the frames. This prevents duplicate code and makes
it easier to maintain the app.

**AppVars class:**
The `AppVars` class encapsulates tkinter variables used in different frames or
widgets.Provides a centralized place to manage state, making it easier to share
and synchronize data between various parts of the application.

**AppStyle class:**

The `Style` class contains all of the styling information for the app. This
includes the colors, fonts, and appearence of the different widgets.



## Usage

The Task App is easy to use and navigate. To get started, simply open the
application and start adding tasks. You can add a task by clicking the "Add
Task" button and entering the task name, due date, and description.

To filter tasks, click on the corresponding Checkbutton and select the desired
filter criteria. For example, you can filter tasks by status, due date, or
both.

To search tasks, type the search term in the search field and the table will
update instantly. The application will search the task titles and descriptions
for the search term.

To mark a task as unstarted, in progress, or completed, simply click on the
corresponding radiobox next to the task.

To sort tasks, click on the table heading.You can sort tasks by ID or due date,
in ascending or descending order.


## Installation
To use the **ToDo List Manager**, follow these steps:
1. Install Python 3.11 or above if you have not already done so.
2. Clone the repository to your local machine.
3. To install the required dependencies, run the following command: `pip
install -r requirements.txt`.
4. Run the app using `python project.py`.
5. "To run tests using the provided `test_project.py` script, execute the
following command: `pytest test_project.py`

## Finally

Thanks to the team of
[CS50's Introduction to Programming with Python](https://www.edx.org/learn/python/harvard-university-cs50-s-introduction-to-programming-with-python)
for the great course.

#### This was CS50P!
