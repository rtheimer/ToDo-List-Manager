import sqlite3
from contextlib import contextmanager


class DataManager:
    def __init__(self, database: str) -> None:
        """Initializes the class with the path to the SQLite3 database file.

        Args:
            database: The path to the SQLite3 database file.
        """
        # the database working with
        self.db = database

    @contextmanager
    def connect(self) -> None:
        """Opens a database connection and yields the cursor. The connection is
            closed automatically when the context manager exits, even if an
            exception is raised.

        Raises:
            sqlite3.Error: If an error occurs while connecting to or closing
            the database.
        """
        # open a database connection or create new if it does not exist
        con = sqlite3.connect(self.db)
        # the database cursor
        cur = con.cursor()
        try:
            yield cur
            con.commit()
        except sqlite3.Error as e:
            raise e
        finally:
            cur.close()
            con.close()

    # create table
    def create_table(self, table: str, cols: dict) -> None:
        """Creates a new table in the database with the given name and column
        definitions.

        Args:
            table: The name of the table to create.
            cols: A dict of column definitions, where each
            definition is a string that specifies the name and data type of the
            column.

        Returns:
            None
        """
        with self.connect() as (cur):
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    {",".join(f"{c} {t}" for c, t in cols.items())}
                    )"""
            )

    def table_exists(self, table: str) -> bool:
        """Verifies if a table exists in the database.

        Args:
            table: The name of the table to check.

        Returns:
            True if the table exists, False otherwise.
        """
        with self.connect() as (cur):
            res = cur.execute(
                f"""
                SELECT name FROM sqlite_master WHERE type='table' AND
                name='{table}'
                """
            )
            res = res.fetchall()
            return len(res) > 0

    def insert_data(self, table: str, data: list) -> int:
        """Inserts data into a table in the database.

        Args:
            table: The name of the table to insert data into.
            data: A list of tuples, where each tuple represents a row of
            data to insert.

        Returns:
            The last row ID of the inserted row
        """

        with self.connect() as (cur):
            cur.execute(
                f"""
                INSERT INTO {table}  (title, description, duedate, status)
                VALUES {data}
                """
            )
            # retrieve the primary key value of the last inserted row
            last_id = cur.lastrowid

            return last_id

    def select_data(self, column: str, table: str) -> list:
        """Retrieves data from a table in the database.

        Args:
            column: The name of the column(s) to select
            table: The name of the table to insert data into.

        Returns:
            A list of rows, where each row is a tuple of values
        """
        with self.connect() as (cur):
            cur.execute(f"SELECT {column} FROM {table}")
            data = cur.fetchall()
            return data

    def select_desc(self, id: int) -> str:
        """Selects description of a task for a given ID

        Args:
            id: The ID of the row to select

        Returns:
            a String with the Description or None
        """
        with self.connect() as (cur):
            cur.execute(f"SELECT description from tasks where id = {id}")
            # access the first value in the tuple [0]
            data = cur.fetchone()[0]
            return data

    def update_data(self, table: str, data: list, id: int) -> None:
        """Updates the task for the given ID

        Args:
            table: The name of the table to update data
            data: A tuple with the data (task, desc, due_date, status)
            id: The ID of the row to select

        Returns:
            None
        """

        with self.connect() as (cur):
            cur.execute(
                f"""
                UPDATE {table} SET title=?, description=?, duedate=?, status=?
                WHERE id = {id}
                """,
                data,
            )

    # delete row
    def delete_data(self, id: int) -> None:
        """
        Delete a row from the 'tasks' table based on the given ID.

        Args:
            id: The ID of the row to be deleted.

        Returns:
            None
        """
        with self.connect() as cur:
            cur.execute(f"DELETE FROM tasks WHERE id = ?", (id,))
