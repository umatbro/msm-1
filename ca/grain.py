from ca.color import Color


class Grain:
    def __init__(self, state=None):
        self.prev_state = state
        self.state = state

    def check_neighbours(self):
        pass

    @property
    def color(self):
        return Color.state_color(self.state)
