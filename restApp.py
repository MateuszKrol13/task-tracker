import sqlite3

from flask import Flask, render_template, request, jsonify, make_response
from data.database_wrapper import TaskDB, IdAsFieldError, EmptyArguments

#TODO: More verbose sql errors
#TODO: Logging module
#TODO: Row factory?
#TODO: Tests
#TODO: make responses more sensible way
#TODO: Remove random leftover prints
#TODO: React/bootstrap?
#RODO: Never share user data!

class WebApp:
    _app = Flask(__name__)

    _db = TaskDB()
    _db.connect('data/database.db')

    def run(self, *args, **kwargs):
        self.set_routes()
        self._app.run(*args, **kwargs)

    def set_routes(self):
        @self._app.route(rule='/tasks/<int:id_>', methods=['PATCH', 'DELETE', 'GET'])
        def specific_task(id_):
            if 'GET' == request.method:
                try:
                    hits = self._db.get(id=id_)[0]  # get first element, fetchall() is called
                    return make_response((hits._asdict(), 200))
                except sqlite3.Error as e:
                    print("SQL operation failed, aborting fetching... ", e)

            if 'PATCH' == request.method:
                try:
                    self._db.update(id_=id_, **request.args.to_dict())
                    return make_response((f"Updated task id={id_}", 200))
                except KeyError:
                    print("Element of given Id not in database, aborting...")
                    return make_response(("Element of given id not found in database", 404))
                except EmptyArguments as e:
                    print("Input args are empty", e)
                    return make_response(("Input is empty", 422))
                except sqlite3.Error as e:
                    print("SQL operation failed, aborting update... ", e)
                    return make_response(("Something on server side failed", 500))

            if 'DELETE' == request.method:
                try:
                    self._db.remove(row_id=id_)
                    return make_response((f"Removed task id={id_}", 200))
                except Warning:
                    return make_response(("Task of given id not found in database", 200))
                except sqlite3.Error as e:
                    print("SQL operation failed, removing failed...", e)
                    return make_response(("Something on server side failed", 500))

            return "Failed to make meaningful response", 500

        @self._app.route(rule='/tasks', methods=['POST', 'GET'])
        def task_resource():
            if request.method == 'POST':
                try:
                    self._db.add(**request.args.to_dict())
                    return make_response(("Succesfully added a task!", 200))
                except IdAsFieldError:
                    print("Id passed as field in request, adding to database aborted...")
                    return make_response(("Wrong input, id passed as field", 422))
                except EmptyArguments as e:
                    print("Input args are empty", e)
                    return make_response(("Input is empty", 422))
                except sqlite3.Error as e:
                    print("SQL operation failed, database not updated: ", e)
                    make_response(("SQL operation failed, adding resource failed", 500))

            if request.method == 'GET':
                try:
                    hits = self._db.get()
                    return make_response(({"tasks" : [task._asdict() for task in hits]}, 200))  # jsonify handles this poorly
                except sqlite3.Error as e:
                    print("SQL operation failed, data not fetched: ", e)
                    return make_response(("Fetching failed.", 500))

            return "Failed to make meaningful response", 500

        @self._app.route(rule='/', methods=['POST', 'GET'])
        def landing_page():
            # TODO: revive landing page...
            return "<html>Hello World!</html>"

if __name__ == "__main__":
    app = WebApp()
    app.run(debug=True, port=5050)