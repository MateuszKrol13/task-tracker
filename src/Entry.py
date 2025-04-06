class ClassNotInitialized(Exception):
    pass

class Entry:
    id_counter = None

    # TODO: come up with more elegant solution
    def __init__(self, id_=None, ctime='', title='', due='', est='', desc='', prio=0, load_obj=False):

        self.title = title
        self.create_time = ctime
        self.due_date = due
        self.time_estimation = est
        self.description = desc
        self.priority = prio

        if not load_obj and Entry.id_counter is None:
            raise ClassNotInitialized("Static entitiy counter not updated before trying to create a new object")

        elif load_obj:
            self.id=id_

        else:
            self.id = Entry.id_counter
            Entry.id_counter += 1

    def to_dict(self):
        return{**self.__dict__}