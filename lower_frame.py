import tkinter as tk
from tkinter import ttk
from base_frame import BaseFrame
from operator import itemgetter
from datetime import datetime


class LowerFrame(BaseFrame):
    """
    The lower frame of the Task App.

    This frame contains a table of tasks, as well as checkboxes for filtering
    the tasks by status and a search field for filtering the tasks by title.
    """

    def __init__(self, root, settings):
        super().__init__(root, settings)
        self.root = root

        # frame objects
        self.frm_upper = settings.get_object("UpperFrame")
        self.mf_top_entry = settings.get_object("MF_Top_Entry")

        # toggle the table sort
        self.toggle_id = False
        self.toggle_duedate = False

        # initialize the Checkbuttons
        self.variables.lf_check_overdue.set(0)
        self.variables.lf_check_progress.set(0)
        self.variables.lf_check_completed.set(0)

        # a 6x7 grid layout
        for grid in range(6):
            # self.rowconfigure(grid, weight=1)
            self.columnconfigure(grid, weight=1)
        for grid in range(7):
            self.rowconfigure(grid, weight=1)
            # self.columnconfigure(grid, weight=1)

        self.create_widgets()

        # load the data from database
        self.data_list = self.load_tasks()
        # insert the data into the table
        self.insert_table_data(self.data_list)

        # the list with the detached iid's from Checkbuttons
        self.detached_items = []

        # list with the selected iid's from checkbuttons
        self.selected_items = self.table.get_children()

        # detached iid's from Search Field
        self.detached_items_search = []

    def create_widgets(self) -> None:
        """Creates the widgets for the frame"""
        # search Entry Filed
        vcmd_search_entry = (self.register(self.search_task), "%P")
        self.search_entry = ttk.Entry(
            self, validate="key", textvariable=self.variables.lf_search_entry
        )
        self.search_entry.configure(validatecommand=vcmd_search_entry)

        # the search label
        search_label = ttk.Label(self, text="search tasks")

        # Checkbutton Overdue
        cb_overdue = ttk.Checkbutton(
            self,
            text="Overdue",
            width=12,
            variable=self.variables.lf_check_overdue,
            command=self.filter_task,
        )
        # Checkbutton ToDo
        cb_todo = ttk.Checkbutton(
            self,
            text="ToDo",
            width=12,
            variable=self.variables.lf_check_todo,
            command=self.filter_task,
        )
        # Checkbutton In Progress
        cb_progress = ttk.Checkbutton(
            self,
            text="In Progress",
            width=12,
            variable=self.variables.lf_check_progress,
            command=self.filter_task,
        )
        # Checkbutton Completed
        cb_completed = ttk.Checkbutton(
            self,
            text="Completed",
            width=12,
            variable=self.variables.lf_check_completed,
            command=self.filter_task,
        )

        # define scrollbar for the table
        self.v_scroll = ttk.Scrollbar(self)
        # using the ttk.Treeview for the table
        self.table = ttk.Treeview(
            self,
            columns=["ID", "Task", "Duedate", "State"],
            show="headings",
            yscrollcommand=self.v_scroll.set,
        )

        # define the columns
        self.table.column("ID", width=50)
        self.table.heading(
            "ID", text="ID" + " ▼▲", command=self.sort_id_column
        )

        self.table.column("#2", width=330)
        self.table.heading("#2", text="Task")

        self.table.column("#3", width=150)
        self.table.heading(
            "Duedate", text="Due Date" + " ▼▲", command=self.sort_date_column
        )

        self.table.column("#4", width=150)
        self.table.heading("State", text="Task Status")

        self.table.tag_configure("ToDo", background=self.style.color_tag_todo)
        self.table.tag_configure(
            "In_Progress", background=self.style.color_tag_progress
        )
        self.table.tag_configure(
            "Completed", background=self.style.color_tag_completed
        )
        self.table.tag_configure(
            "Overdue", background=self.style.color_tag_overdue
        )

        # Attach the scrollbar
        self.v_scroll.configure(command=self.table.yview)

        # the Layout
        self.search_entry.grid(row=0, column=0, columnspan=2, sticky="ew")
        search_label.grid(row=0, column=2, sticky="w")
        cb_overdue.grid(row=1, column=2)
        cb_todo.grid(row=1, column=3)
        cb_progress.grid(row=1, column=4)
        cb_completed.grid(row=1, column=5)
        self.table.grid(
            row=2, rowspan=5, column=0, columnspan=6, sticky="nsew"
        )
        self.v_scroll.grid(row=2, rowspan=5, column=6, sticky="ns")

        # events
        self.search_entry.bind("<BackSpace>", self.reset_detached_search_items)
        self.table.bind("<<TreeviewSelect>>", self.fill_form_selection)

    def load_tasks(self) -> list:
        """
        Loads all tasks from the database
        """
        res = self.database.select_data("id, title, duedate, status", "tasks")
        data_list = []
        for items in res:
            d_tuple = (items[0], items[1], items[2], items[3])
            data_list.append(d_tuple)
        return data_list

    def insert_table_data(self, data: tuple) -> None:
        """Inserts the given task data into the table."""

        for items in data:
            status_tag = items[3]
            due_date = items[2]
            if status_tag == "In Progress":
                status_tag = "In_Progress"
            if self.func[2](due_date) < 0 and items[3] != "Completed":
                status_tag = "Overdue"
            self.table.insert("", index=0, values=items, tags=(status_tag))

    def fill_form_selection(self, _) -> None:
        """Fills the Form Fields with the selected tasks values

        Returns:
            None.
        """
        # check if there are there any selected items
        selected_item = self.table.focus()
        if not selected_item:
            return

        # set the item value in the entry field
        self.variables.mf_top_entry.set(
            self.table.item(selected_item, "values")[1]
        )

        # set the item value in the due date entry field
        self.variables.uf_due_date.set(
            self.table.item(selected_item, "values")[2]
        )

        # set the status to Radio Button
        status_text = self.table.item(selected_item, "values")[3]
        match status_text:
            case "ToDo":
                status = 1
            case "In Progress":
                status = 2
            case "Completed":
                status = 3
        self.variables.uf_task_state_var.set(status)

        # reset the message box Label
        self.variables.uf_message_var.set("")

        # get the description text from database as it is not part of the table
        res = self.database.select_desc(
            self.table.item(selected_item, "values")[0]
        )
        # set the decription in the Text Field
        self.frm_upper.set_text(res)

    def add_item(self) -> None:
        """Adds a new task to the database and to the treeview table,
        if no field is empty and all entries are validated
        """

        # get all data from the fields
        # get the entry text
        task = self.variables.mf_top_entry.get()
        # get the description text
        desc = self.frm_upper.get_text()
        # get the task state
        status_number = self.variables.uf_task_state_var.get()
        # get the due date
        due_date = self.variables.uf_due_date.get()

        if self.validate_items(task, due_date) == False:
            return

        match status_number:
            case "1":
                status = "ToDo"
            case "2":
                status = "In Progress"
            case "3":
                status = "Completed"
            case _:
                status = "unknown"

        # write to database and get the lastrow id
        id = self.database.insert_data("tasks", (task, desc, due_date, status))

        # insert into table if we got a id
        # if task date is overdue, set a second tag to table "Overdue"
        status_tag = status
        if id is not None:
            if status_tag == "In Progress":
                status_tag = "In_Progress"
            # if the task is overdue
            if self.func[2](due_date) < 0 and status_tag != "Completed":
                status_tag = "Overdue"

            self.table.insert(
                "",
                index=0,
                values=(id, task, due_date, status),
                # if over due
                tags=(status_tag),
            )
            # update data_list
            self.data_list = self.load_tasks()
            # clear boxes
            self.frm_upper.cls()

    def delete_item(self) -> None:
        """Deletes the selected task's in the database and the table.

        Returns:
            None.
        """
        selected_items = self.table.selection()
        # check if almost one item is selected
        if len(selected_items) == 0:
            self.frm_upper.set_message("no item selected")
            return
        # delete items from database
        for id in self.table.selection():
            item = self.table.item(id, "values")[0]
            self.database.delete_data(item)
        # delete items from table
        for item in self.table.selection():
            self.table.delete(item)
        # update data_list
        self.data_list = self.load_tasks()
        # clear boxes
        self.frm_upper.cls()

    def update_item(self) -> None:
        """Updates the selected task in the database and the table

        Returns:
            None
        """
        item = self.table.focus()
        if not item:
            self.frm_upper.set_message("no item selected")
            return

        id = self.table.item(item, "values")[0]
        # get the entry text
        task = self.variables.mf_top_entry.get()
        # get the description text
        desc = self.frm_upper.get_text()
        # get the task state
        status_number = self.variables.uf_task_state_var.get()
        # get the due date
        due_date = self.variables.uf_due_date.get()

        if self.validate_items(task, due_date) == False:
            return

        match status_number:
            case "1":
                status = "ToDo"
            case "2":
                status = "In Progress"
            case "3":
                status = "Completed"
            case _:
                status = "unknown"

        # update database
        self.database.update_data("tasks", (task, desc, due_date, status), id)

        # update table
        status_tag = status

        if status_tag == "In Progress":
            status_tag = "In_Progress"

        if self.func[2](due_date) < 0 and status != "Completed":
            status_tag = "Overdue"
        self.table.item(
            item,
            values=(id, task, due_date, status),
            tags=(status_tag),
        )
        # update data_list
        self.data_list = self.load_tasks()
        # remove the selection from the item
        self.table.selection_remove(item)
        # remove the focus from the item !!!
        self.table.focus("")
        # clear boxes
        self.frm_upper.cls()

    def validate_items(self, task: str, due_date: str) -> bool:
        """Validates the task and due date

        Args:
            task: The task string.
            due_date: The due date string

        Returns:
            True if the entries are valid, False otherwise
        """
        # Task Entry Validation
        if self.func[0](task) != True:
            self.mf_top_entry.config(style="Invalid.TEntry")
            self.frm_upper.set_message("Task must begin\nwith 3 Letters")
            return False
        else:
            self.mf_top_entry.config(style="Valid.TEntry")

        # Due Date Entry Validation
        val = self.func[1](due_date)
        if val == False:
            self.frm_upper.due_entry.config(style="Invalid.TEntry")
            self.frm_upper.set_message("Dateformat:\nmm-dd-yyyy\nmm/dd/yyyy")
            return False
        else:
            self.frm_upper.due_entry.config(style="Valid.TEntry")

        return True

    def filter_task(self) -> bool:
        """Filters the tasks in the table by the selected checkbuttons

        Returns:
            True if the filter was successful
        """
        # restore table / move items back from search detached
        self.reset_detached_search_items("")

        # move back detached items from the checkbuttons
        if len(self.detached_items) > 0:
            for item in self.detached_items:
                self.table.move(item, "", tk.END)
            # reset the list with the detached iid's
            self.detached_items = []

        # tuple containing the iid values of the top-level items
        iid_all = self.table.get_children()
        # collect the items to stay attached
        iid_selected = []

        # get the Checkbutton states
        overdue = self.variables.lf_check_overdue.get()
        todo = self.variables.lf_check_todo.get()
        progress = self.variables.lf_check_progress.get()
        completed = self.variables.lf_check_completed.get()

        # if overdue or progress or completed
        if (
            overdue == "1"
            or todo == "1"
            or progress == "1"
            or completed == "1"
        ):
            # if overdue is selected get all iid's from "tags"
            if overdue == "1":
                for item in iid_all:
                    if "Overdue" in self.table.item(item)["tags"][0]:
                        iid_selected.append(item)

            # if todo is selected get all iid's from "tags"
            if todo == "1":
                for item in iid_all:
                    if "ToDo" in self.table.item(item)["values"][3]:
                        iid_selected.append(item)

            # if progress is selected get all iid's
            if progress == "1":
                for item in iid_all:
                    if "Progress" in self.table.item(item)["values"][3]:
                        iid_selected.append(item)

            # if completed get all iid's
            if completed == "1":
                for item in iid_all:
                    if "Completed" in self.table.item(item)["values"][3]:
                        iid_selected.append(item)

            # store selected items
            self.selected_items = iid_selected
            # detach all iid's not selected
            self.detach_unselected_items(iid_selected)

        else:
            for item in self.detached_items:
                self.table.move(item, "", tk.END)
            self.selected_items = self.table.get_children()

        # sort table by ID
        self.sort_id_column(False)
        return True

    def detach_unselected_items(self, selected: list) -> None:
        """Detaches all items from the table that are not selected.

        Args:
            selected: A list of the selected item IDs.

        Returns:
            None
        """
        # tuple with the detached iid's
        detached_items = ()
        # check all ids' wether they are not selected, then detach them
        for item in self.table.get_children():
            if item not in selected:
                detached_items = detached_items + (item,)
                self.table.detach(item)
        # update the list with detached items
        self.detached_items = detached_items

    def search_task(self, value: str) -> bool:
        """Searches for tasks in the table by title.

        Args:
            value: The search term.

        Returns:
            True if the search was successful, False otherwise
        """
        # restore table / move items back from search detached
        if value == "":
            self.reset_detached_search_items("")

        # get the set of selected items from Checkbuttons
        items_selected = self.selected_items
        if len(items_selected) == 0:
            items_selected = self.table.get_children()

        detached_items = ()

        # collect items that match value
        iid_selected = []
        for item in items_selected:
            if value in (self.table.item(item)["values"][1]):
                iid_selected.append(item)

        # check all ids' wether they are not selected, then detach them
        for item in items_selected:
            if item not in iid_selected:
                detached_items = detached_items + (item,)
                self.table.detach(item)

        # update attribute
        self.detached_items_search = detached_items
        # sort table by ID
        self.sort_id_column(False)
        return True

    def reset_detached_search_items(self, event) -> None:
        """Resets the table and moves back detached items from search.

        Args:
            event: The event that triggered the function call

        Returns:
            None
        """
        # reset the table / move back detached items from search

        for item in self.detached_items_search:
            self.table.move(item, "", tk.END)
        # if the function was called without the <BackSpace> event
        # set the textvariable to ""
        if not event:
            self.variables.lf_search_entry.set("")
        # self.detached_items = []

    def sort_date_column(self) -> None:
        """Sorts the tasks in the table by Date"""

        # Toggle
        reverse = self.toggle_duedate
        if self.toggle_duedate == False:
            self.toggle_duedate = True
        else:
            self.toggle_duedate = False

        data = []
        formats = [
            "%m-%d-%Y",
            "%m/%d/%Y",
        ]
        # get the children
        children = self.table.get_children()

        # get the data from children
        for child in children:
            data.append(
                [
                    child,
                    self.table.set(
                        child,
                        column="#3",
                    ),
                ]
            )
        # sort the data
        i = 0
        for date_ in data:
            # parse string to time
            for f in formats:
                try:
                    date_obj = datetime.strptime(date_[1], f)
                    data[i][1] = date_obj
                    break
                except ValueError:
                    pass
            i += 1
        data_sorted = sorted(data, key=itemgetter(1), reverse=reverse)
        count = 0
        for item in data_sorted:
            self.table.move(item[0], "", count)
            count += 1

    def sort_id_column(self, reverse: bool = None) -> None:
        """Sorts the tasks in the table by ID.

        Args:
            reverse: Whether to sort in reverse order
        """

        if reverse is not None:
            reverse = reverse
        else:
            reverse = self.toggle_id
            if self.toggle_id == False:
                self.toggle_id = True
            else:
                self.toggle_id = False

        children = self.table.get_children()

        data = []
        # get the data from children
        for child in children:
            data.append(
                [
                    child,
                    int(
                        self.table.set(
                            child,
                            column="#1",
                        )
                    ),
                ]
            )

        data_sorted = sorted(data, key=itemgetter(1), reverse=reverse)
        count = 0
        for item in data_sorted:
            self.table.move(item[0], "", count)
            count += 1
