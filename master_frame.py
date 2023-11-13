import tkinter as tk
from tkinter import ttk
from base_frame import BaseFrame
from upper_frame import UpperFrame
from lower_frame import LowerFrame
from datetime import datetime

# # Today's date as str
today = datetime.now().strftime("%a %d.%m.%Y")


class MasterFrame(BaseFrame):
    def __init__(self, root, settings):
        """Initializes the master frame.

        Args:
            root: The root window of the application.
            settings: The settings object for the application
        """
        super().__init__(root, settings)
        # the root instance
        self.root = root

        # a 6x6 grid layout
        for grid in range(6):
            self.rowconfigure(grid, weight=1)
            self.columnconfigure(grid, weight=1)

        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the master frame.

        Returns:
            None
        """
        # the entry widget
        self.top_entry = ttk.Entry(
            self,
            width=63,
            textvariable=self.variables.mf_top_entry,
        )
        # register the top entry field
        self.settings.set_object("MF_Top_Entry", self.top_entry)
        self.top_entry.grid(row=0, column=0, columnspan=4, sticky=tk.EW)
        self.top_entry.focus_set()

        self.time_label = ttk.Label(self, text=today)
        self.time_label.grid(row=0, column=4, columnspan=2, sticky="e")

        # paned window
        self.pw = ttk.PanedWindow(
            self, orient=tk.VERTICAL, style="master.TPanedwindow"
        )
        self.pw.grid(row=1, rowspan=4, column=0, columnspan=6, sticky=tk.NSEW)

        # frames for the paned window
        self.frm_upper = UpperFrame(self.pw, self.settings)
        self.settings.set_object("UpperFrame", self.frm_upper)
        self.frm_lower = LowerFrame(self.pw, self.settings)

        # Add frames as panes to the PanedWindow
        self.pw.configure()
        self.pw.add(self.frm_upper, weight=1)
        self.pw.add(self.frm_lower, weight=1)

        # the buttom row of the MasterFrame
        # The button used to add a new task
        self.add_button = ttk.Button(
            self, text="add Task", width=12, command=self.frm_lower.add_item
        )
        # The button used to delete tasks
        delete_button = ttk.Button(
            self,
            text="delete Task",
            width=12,
            command=self.frm_lower.delete_item,
        )
        # The button used to update a task
        update_button = ttk.Button(
            self,
            text="update Task",
            width=12,
            command=self.frm_lower.update_item,
        )

        self.add_button.grid(row=5, column=3, sticky=tk.E)
        delete_button.grid(row=5, column=4)
        update_button.grid(row=5, column=5, sticky=tk.W)
