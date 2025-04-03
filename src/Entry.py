class Entry:
    def __init__(self, ctime='', title='', due='', est='', desc='', prio = 0):
        self.title = title
        self.create_time = ctime
        self.due_date = due
        self.time_estimation = est
        self.description = desc
        self.priority = prio