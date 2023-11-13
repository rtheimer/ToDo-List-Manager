import db, gui, re
import tkinter as tk
from datetime import datetime, date
from app_settings import AppSettings


def main():
    """This is the main entry point of the program"""

    # database: The path to the SQLite3 database file.
    # table_name: The name of the table in the database to store the tasks.
    database = "todo_manager.db"
    table_name = "tasks"

    # Initialize  the app's settings
    app_settings = AppSettings()

    # Functions to be registered in the settings object to validate data
    # and calculate days overdue.
    functions = (validate_entry, validate_date, calculate_days_overdue)

    # Register the functions tuple in the settings object to share them in
    # other modules and classes
    app_settings.functions = functions

    # Table structure to create the app's table in the database
    table_structure = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "title": "TEXT",
        "description": "TEXT",
        "duedate": "TEXT",
        "status": "TEXT",
    }

    # Connection to the database, which will be created if not exists
    tasks_db = db.DataManager(database)

    # Register the database in the settings object
    app_settings.set_object("DataManager", tasks_db)

    # Create the app's table if it does not exist
    create_table(tasks_db, table_name, table_structure)

    # The root window, titled "TodoListManager"
    root = tk.Tk(className="TodoListManager")

    # Initialize the App
    app = gui.TaskApp(root, app_settings)

    # run the App
    app.run()


def create_table(con: db.DataManager, table: str, structure: dict) -> bool:
    """Creates a new table in the database with the given name and column
    definitions.
    Returns True if the table was created successfully, or False otherwise.

    Args:
        con: A DataManager Object.
        table: The name of the table to create.
        structure: A dict of column definitions, where each definition
        is a string that specifies the name and data type of the column.
    """
    try:
        with con.connect():
            con.create_table(table, structure)
            res = con.table_exists(table)
            return res
    except Exception as error:
        raise error


def validate_entry(txt: str) -> bool:
    """Validates an entry string, ensuring it is at least 3 characters long and
    contains only letters, numbers, spaces, underscores, and hyphens.

    Args:
        txt: The string to validate.

    Returns:
        True if the entry is valid, False otherwise.
    """

    pattern = r"^[a-zA-Z]{3}[a-zA-Z0-9\s_-]*$"
    res = re.match(pattern, txt)

    return bool(res) if res else False


def validate_date(task_date: str) -> bool:
    """Validates a date string using a list of date formats.

    Args:
      date: The date string to validate.

    Returns:
      True if the date string is valid, False otherwise.
    """
    formats = [
        "%m-%d-%Y",
        "%m/%d/%Y",
    ]
    if not task_date:
        return False
    for f in formats:
        try:
            datetime.strptime(task_date, f)
            return True
        except ValueError:
            pass
    return False


def calculate_days_overdue(task_date: str) -> int:
    """Calculates the number of days overdue for a given task date, relative to
    today.

    Args:
        task_date: The task date, in one of the following formats:
            * `MM-DD-YYYY`
            * `MM/DD/YYYY`

    Returns:
        Negative numbers of days if the given day is in the past.
        Positive numbers if the given day is in the future.
        It returns None if the given term is in unsupported format or today.
    """
    formats = [
        "%m-%d-%Y",
        "%m/%d/%Y",
    ]
    today = date.today()
    for f in formats:
        try:
            x = datetime.strptime(task_date, f)
            y = datetime(today.year, today.month, today.day)
            # get the time delta
            days = x - y

            return days.days

        except ValueError:
            continue


if __name__ == "__main__":
    main()
