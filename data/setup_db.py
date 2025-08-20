import sqlite3
import os

DATABASE = '..//database.db'
TABLE = '''CREATE TABLE Tasks (
    id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    time_est TEXT NOT NULL,
    due INTEGER,
    priority INTEGER,
    PRIMARY KEY("id" AUTOINCREMENT)
);'''


def setup_db():
    print("Attempting setting up database...")
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(TABLE)
            conn.commit()
        print("Setup successful!")

    except sqlite3.OperationalError as e:
        print("Failed to create tables! ", e)


if "__main__" == __name__:
    print("Running database setup script...")

    if os.path.exists(DATABASE):
        ans = input("WARNING! file 'database.db' found! Do you wish to proceed? (Y/N): ")
        match ans:
            case "Y":
                try:
                    os.remove(DATABASE)
                    setup_db()
                except FileNotFoundError:
                    print("Database does not exist?")
                except PermissionError as e:
                    print("PermissionError: ", e)
                except sqlite3.Error as e:
                    print("SQLite error: ", e)
            case "N":
                print("Skipping operation...")
                pass
            case _:
                print("Wrong key goofyaah")
    else:
        setup_db()