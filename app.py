from flask import Flask, render_template, request
from datetime import datetime
from calendar import HTMLCalendar
from src.Entry import Entry
import xml.etree.ElementTree as ET

class WebApp():
    app = Flask(__name__)
    planner_entries: list[Entry]

    def run(self, *args, **kwargs):
        self.load_app_state()
        self.set_routes()
        self.app.run(*args, **kwargs)

    def load_app_state(self):
        entries_xml = ET.parse('out.xml').getroot()
        self.planner_entries = []

        for entry in entries_xml:
            a = Entry(
                ctime=entry.attrib['createTime'],
                title=entry.attrib['title'],
                desc=entry.attrib['description'],
                due=entry.attrib['dueDate'],
                est=entry.attrib['timeEstimation'],
                prio=entry.attrib['priority']
            )

            self.planner_entries.append(a)

    def set_routes(self):

        @self.app.route(rule='/', methods=['POST', 'GET'])
        def landing_page():
            if request.method == 'GET':
                pass

            elif request.method == 'POST':
                a = Entry(
                    ctime=datetime.now(),
                    title=request.form['new-entry-title'],
                    due=request.form['new-entry-due-date'],
                    est=" D: " + request.form['new-entry-time-est-days'] +
                        " H: " + request.form['new-entry-time-est-hours'] +
                        " M: " + request.form['new-entry-time-est-minutes'],
                    desc=request.form['new-entry-description'],
                    prio=int(request.form['new-entry-prio'])
                )

                self.planner_entries.append(a)

                with open('out.xml', 'w') as f:
                    f.write(render_template(
                       template_name_or_list='entry_save.xml.j2',
                        entries = self.planner_entries
                    ))

            return render_template(
                template_name_or_list='index.html',
                entries = self.planner_entries,
            )

        @self.app.route('/calendar/')
        def hello_world():
            current_date = datetime.now().strftime('%Y-%m')
            year, month = current_date.split('-')

            month_html = HTMLCalendar().formatmonth(theyear=int(year), themonth=int(month))

            return render_template(template_name_or_list='data.html', date=month_html)


if __name__ == '__main__':
    app = WebApp()
    app.run(debug=True)