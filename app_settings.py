import tkinter as tk


class AppSettings:
    def __init__(self):
        """Creates a new instance of the `AppSettings` class.

        The `__objects` and `__functions` attributes are private to prevent
        users from modifying them directly.
        """
        # the frames and widget objects in use
        self.__objects = {}

        # shared functions
        self.__functions = ()

    def get_object(self, key) -> object:
        """Returns the shared frame or widget object associated with the given
        key.
        If the key does not exist, the function returns `None`.
        """
        return self.__objects.get(key)

    def set_object(self, key: str, obj: object):
        """Sets the object associated with the given key"""

        self.__objects[key] = obj

    @property
    def functions(self) -> tuple:
        """Returns a tuple of the shared functions."""

        return self.__functions

    @functions.setter
    def functions(self, func: list):
        """Sets the functions associated with the app.
        The functions are set to a tuple to make them immutable.
        """

        self.__functions = func

    def __repr__(self) -> str:
        return f"Settings()"

    def __str__(self) -> str:
        return f"Settings App"


class AppVars:
    """
    Class to manage tkinter variables for a multi-frame application.

    Encapsulates tkinter variables used in different frames or widgets.
    Provides a centralized place to manage state, making it easier to
    share and synchronize data between various parts of the application.
    """

    def __init__(self) -> None:
        # master frame top entry
        self.mf_top_entry = tk.StringVar()

        # upper frame
        # variable for the due date entry
        self.uf_due_date = tk.StringVar()

        # variable for the radiobutton group
        self.uf_task_state_var = tk.StringVar()
        # set intitial radiobutton
        self.uf_task_state_var.set(1)

        # variable for the message label
        self.uf_message_var = tk.StringVar()

        # Lower Frame
        self.lf_search_entry = tk.StringVar()
        # variables for the Checkbuttons
        self.lf_check_completed = tk.StringVar()
        self.lf_check_progress = tk.StringVar()
        self.lf_check_todo = tk.StringVar()
        self.lf_check_overdue = tk.StringVar()
