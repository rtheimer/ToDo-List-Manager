import tkinter as tk
from tkinter import ttk
from base_frame import BaseFrame


class UpperFrame(BaseFrame):
    def __init__(self, root, settings):
        super().__init__(root, settings)
        self.root = root
        self.settings = settings
        self.mf_top_entry = settings.get_object("MF_Top_Entry")
        # self.obj = mf

        # a 6x6 grid layout
        for grid in range(6):
            self.rowconfigure(grid, weight=1)
            self.columnconfigure(grid, weight=1)

        # Top Label
        label = ttk.Label(self, text="Task Description")
        label.grid(row=0, column=0, sticky=tk.NW)

        # START control Frame definition --------------------------------------
        c_frm = ttk.Frame(self)
        c_frm.grid(row=1, rowspan=4, column=4, columnspan=2, sticky=tk.NSEW)

        # upper control frame Label
        label_due = ttk.Label(c_frm, text="Due Date")
        label_due.configure(anchor="center")
        label_due.pack(fill="x", expand=False, anchor="center")

        # Due Date Entry Box
        # register validation function
        valCommand = (c_frm.register(self.validate_date_entry), "%P")
        self.due_entry = ttk.Entry(
            c_frm,
            validate="focusout",
            textvariable=self.variables.uf_due_date,
            validatecommand=valCommand,
            invalidcommand=self.invalid_date,
        )
        self.due_entry.pack()

        # Tasks State Label
        label_state = ttk.Label(c_frm, text="Tasks States")
        label_state.configure(anchor="center")
        label_state.pack(fill="x", anchor="center")

        # Radio Button group for the task status
        n_button = ttk.Radiobutton(
            c_frm,
            text="ToDo",
            width=10,
            variable=self.variables.uf_task_state_var,
            value=1,
        )
        n_button.pack()
        p_button = ttk.Radiobutton(
            c_frm,
            text="In Progress",
            width=10,
            variable=self.variables.uf_task_state_var,
            value=2,
        )
        p_button.pack()
        c_button = ttk.Radiobutton(
            c_frm,
            text="Completed",
            width=10,
            variable=self.variables.uf_task_state_var,
            value=3,
        )
        c_button.pack()

        # Warning Message Label
        message_label = ttk.Label(
            c_frm,
            textvariable=self.variables.uf_message_var,
            style="Mlabel.TLabel",
        )
        message_label.pack(expand=True)
        # END control Frame definition ----------------------------------------

        # scrollbar
        self.v_scroll = ttk.Scrollbar(self)
        self.v_scroll.grid(row=1, column=4, rowspan=4, sticky="ns, w")

        # Description Text Box
        self.desc = tk.Text(
            self,
            height=12,
            width=50,
            font=self.style.font,
            yscrollcommand=self.v_scroll.set,
            wrap="word",
        )
        # self.desc.bind("<FocusOut>", obj.func[1])
        self.desc.grid(
            row=1, column=0, rowspan=4, columnspan=4, sticky=tk.NSEW
        )

        # Attach scrollbar to Text Box
        self.v_scroll.configure(command=self.desc.yview)

        # Button CLS
        self.cls_button = ttk.Button(self, text="clear all", command=self.cls)
        self.cls_button.grid(row=5, column=0)
        # TODO: remove, only for testing
        self.set_message("Hallo User")

    # methods for the TEXT widget
    def set_text(self, val) -> None:
        self.del_text()
        self.desc.insert("1.0", val)

    def get_text(self) -> None:
        return self.desc.get("1.0", "end-1c")

    def del_text(self) -> None:
        self.desc.delete("1.0", "end")

    # method for the message Label
    def set_message(self, text: str) -> None:
        self.variables.uf_message_var.set(text)

    # methods for the date Entry widget
    def invalid_date(self) -> None:
        self.set_message("invalid date")
        self.due_entry.configure(style="Invalid.TEntry")

    def validate_date_entry(self, date: str) -> None:
        result = self.func[1](date)
        if result == True:
            self.due_entry.configure(style="Valid.TEntry")
            self.set_message("")
            return result
        return False

    # method for the cls Button
    def cls(self) -> None:
        # delete text
        self.del_text()
        # delete entry
        self.variables.mf_top_entry.set("")
        self.mf_top_entry.configure(style="TEntry")
        # delete due date
        self.variables.uf_due_date.set("")
        # set radio button
        self.variables.uf_task_state_var.set(1)
        # set default entry style
        self.due_entry.configure(style="TEntry")
        # empty message Label
        self.set_message("")
