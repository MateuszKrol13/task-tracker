import sqlite3
import functools
from collections import namedtuple

Task = namedtuple("Task", ['id', 'title', 'description', 'time_est', 'due', 'priority'])

class NoConnectionException(Exception):
    pass

class IdAsFieldError(Exception):
    pass

class EmptyArguments(Exception):
    pass

def requires_connection(func):
    """Wrapper used for DataBase class to check if database operations can be performed?"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_db'):
            raise NoConnectionException("Not connected to database.")
        return func(self, *args, **kwargs)
    return wrapper

class TaskDB:
    """Note: for each operation, database connection is opened, operation is performed and database connection is
    terminated. Not time optimal, but should prevent weird crashes."""
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TaskDB, cls).__new__(cls)
        return cls.instance

    @classmethod
    def connect(cls, database_path: str) -> None:
        """Asigns database path that is later used by all"""
        cls._db = database_path

    @requires_connection
    def add(self, **kwargs) -> None:
        """Adds a database entry.

        Required Parameters:
            title (str): task title
            time_est (str): time estimation as string

        Optional Parameters:
            description (str): task description
            due (str): due date as string
            priority (int): priority integer

        Raises:
            IdAsFieldError: when "id" is part of kwargs keys
            EmptyArguments: when passed kwargs are an empty dict
            sqlite3.Error: when sqlite operation fails
        """
        if not kwargs:
            raise EmptyArguments("Passed empty dicitonary containing no fields")

        if "id" in kwargs.keys():
            raise IdAsFieldError("ID should not be passed as a field, because its autoincremented!")

        fields = ", ".join(kwargs.keys())
        placeholders = ", :".join(kwargs.keys())
        with sqlite3.connect(self._db) as conn:
            cursor = conn.cursor()
            print(f"INSERT INTO Tasks ({fields}) VALUES (:{placeholders})")
            cursor.execute(f"INSERT INTO Tasks ({fields}) VALUES (:{placeholders})", kwargs)
            conn.commit()

    @requires_connection
    def get(self, **kwargs) -> list[Task] | None:
        """Returns all the task entries that match criteria specified in kwargs

        Optional Parameters:
            title (str)
            description (str)
            due (str)
            priority (int)
            time_est (str)

        Raises:
            sqlite3.Error: if SQL operation fails

        Returns:
            list[Task]: list of Task namedtuple for any row that matches specified criteria

        """
        parameters = " WHERE " + " AND ".join(f"{key}=:{key}" for key in kwargs.keys()) if kwargs else ""

        with sqlite3.connect(self._db) as conn:
            # TODO: test or switch? or write more extensive factory function
            conn.row_factory = lambda _, row: Task(*row)  #!REQUIRES! testing that fields are aligned?
            c = conn.cursor()
            c.execute(f"SELECT * FROM Tasks {parameters}", kwargs)
            hits = c.fetchall()
        return hits

    @requires_connection
    def update(self, id_: int, **kwargs) -> None:
        """Updates field values of task entry with specified id number

            Optional Parameters:
                title (str)
                description (str)
                due (str)
                priority (int)
                time_est (str)

            Raises:
                KeyError: Element of specified id is not in database
                EmptyArguments: when passed kwargs are an empty dict
                sqlite3.Error: SQL operation fails
        """
        if not kwargs:
            raise EmptyArguments("Passed empty dicitonary containing no fields")

        if not self.get(id=id_):
            raise KeyError(f"Task of id={id_} not found in database.")

        fields = ""
        for k, v in kwargs.items():
            fields += f"{k}={v}" if not isinstance(v, str) else f"{k}='{v}'"

        with sqlite3.connect(self._db) as conn:
            c = conn.cursor()
            print(kwargs)
            print(f"UPDATE Tasks SET {fields} WHERE id={id_}")
            c.execute(f"UPDATE Tasks SET {fields} WHERE id={id_}")

    @requires_connection
    def remove(self, row_id: int) -> None:
        """Removes row from 'Tasks' table with given id

            Raises:
                Warning: Element of specified id is not in database
                sqlite3.Error: SQL operation fails
        """
        if not self.get(id=row_id):
            raise Warning("Task of given id was not found, skipping operation.")
        else:
            with sqlite3.connect(self._db) as conn:
                c = conn.cursor()
                c.execute(f"DELETE FROM Tasks WHERE id={row_id}")