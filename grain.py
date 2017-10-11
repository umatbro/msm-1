class Grain:
    def __init__(self, state=None, screen=None):
        self.screen = screen
        self.prev_state = state
        self.state = None

    def check_neighbours(self):
        pass

    def __repr__(self):
        return str(self.state)

    def __bool__(self):
        return self.prev_state
