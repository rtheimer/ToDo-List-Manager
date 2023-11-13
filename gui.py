import tkinter as tk
from tkinter import ttk
from master_frame import MasterFrame
from app_settings import AppVars


class AppStyle:
    """Initializes the Style for the App.
    Make all Style definitions here.
    """

    def __init__(self):
        # defining  the apps's colors
        self.colors = {
            "primary": "#3B71CA",
            "success": "#14A44D",
            "danger": "#DC4C64",
            "warning": "#E4A11B",
            "lightgreen": "#a5d6a7",
            "lightorange": "#ffe0b2",
            "darkorange": "dark orange",
            "lightgray": "#e0e0e0",
        }

        # the table_tags colors
        # Tag new
        self.color_tag_todo = self.colors["lightgray"]
        # Tag in progress
        self.color_tag_progress = self.colors["lightorange"]
        # Tag completed
        self.color_tag_completed = self.colors["lightgreen"]
        # Tag overdue
        self.color_tag_overdue = self.colors["danger"]

        # Create the style definitions
        self.style = ttk.Style()

        # generally style settings for the ttk widgets
        # the theme
        self.style.theme_use("default")

        # the TFrame
        self.style.configure("TFrame", background=self.colors["primary"])

        # the TLabel
        self.style.configure(
            "TLabel",
            background=self.colors["primary"],
            foreground="white",
            padding=(10),
        )

        # the Tradiobutton
        self.style.map(
            "TRadiobutton",
            indicatorcolor=[("selected", self.colors["danger"])],
            background=[("active", self.colors["primary"])],
        )
        self.style.configure(
            "TRadiobutton",
            background=self.colors["primary"],
            foreground="white",
        )

        # the TCheckbutton
        self.style.map(
            "TCheckbutton",
            indicatorcolor=[
                ("selected", self.colors["danger"]),
                ("pressed", self.colors["primary"]),
            ],
            background=[("active", self.colors["primary"])],
        )
        self.style.configure(
            "TCheckbutton",
            background=self.colors["primary"],
            foreground="white",
        )

        # the Treeview
        self.style.configure(
            "Treeview", fieldbackground=self.colors["lightgray"]
        )

        # custom style settings
        # message Label Box
        self.style.configure(
            "Mlabel.TLabel",
            foreground=self.colors["darkorange"],
            font=("", 10, "bold"),
        )

        # MasterFrame Paned window
        self.style.configure("master.TPanedwindow", background="black")

        # Invalid.TEntry
        self.style.configure(
            "Invalid.TEntry",
            fieldbackground=self.colors["danger"],
            foreground=self.colors["lightgray"],
        )
        # Valid.TEntry
        self.style.configure(
            "Valid.TEntry",
            fieldbackground=self.colors["lightgreen"],
            foreground="black",
        )

        # styling the tk widgets
        self.font = ("", 10, "")


class TaskApp:
    """
    The main class for the Task App.
    This class initializes the root window, creates the main frame, and starts
    the mainloop.
    """

    def __init__(self, root, settings):
        # the root window
        self.root = root
        # settings object
        self.settings = settings

        # the root window
        self.root.title("Todo List Manager")
        self.root.geometry("800x700")
        self.root.minsize(width=800, height=700)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # initialize the style for the App
        self.app_style = AppStyle()
        # register the App Style Object
        self.settings.set_object("AppStyle", self.app_style)

        # initialize the Shared Variables Object for the App
        self.app_vars = AppVars()

        # register the App Variables Object
        self.settings.set_object("AppVars", self.app_vars)

        # create the widgets
        self.create_widgets()

    def create_widgets(self):
        # master frame
        self.frame = MasterFrame(self.root, self.settings)
        # register the Master Frame Object
        self.settings.set_object("MasterFrame", self.frame)
        # put the Frame on the Grid
        self.frame.grid(padx=30, pady=5, sticky=tk.NSEW)

    # Method for running the application
    def run(self):
        self.root.mainloop()
