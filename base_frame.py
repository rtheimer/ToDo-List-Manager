from tkinter import ttk

# TODO: Annotations
class BaseFrame(ttk.Frame):
    """
    Base class for all frames in the Task App.
    Provides common functionality for accessing settings, style, database, and
    variables.
    """
    def __init__(self, root, settings):
        super().__init__(root)

        self.settings = settings
        self.root=root
        self.func = settings.functions
        self.style = self.settings.get_object("AppStyle")
        self.database = self.settings.get_object("DataManager")
        self.variables = self.settings.get_object("AppVars")
