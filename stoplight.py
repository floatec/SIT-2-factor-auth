class Stoplight(object):
    __slots__ = 'state'

    def __init__(self, initial_state):
        self.state = initial_state

    def set_state(self, s):
        self.state = s

    def get_state(self):
        return self.state

    def change(self):
        if self.state == 'red':
            self.state = 'red yellow'
        elif self.state == 'red yellow':
            self.state = 'green'
        elif self.state == 'green':
            self.state = 'yellow'
        elif self.state == 'yellow':
            self.state = 'red'

    def get_lamps(self):
        lamps = (False, False, False)
        if self.state == 'red':
            lamps = (True, False, False)
        elif self.state == 'red yellow':
            lamps = (True, True, False)
        elif self.state == 'green':
            lamps = (False, False, True)
        elif self.state == 'yellow':
            lamps = (False, True, False)
        return lamps