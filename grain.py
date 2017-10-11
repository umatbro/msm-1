from color import Color


class Grain:
    def __init__(self, state=None):
        self.prev_state = state
        self.state = state

    def check_neighbours(self):
        pass

    @property
    def color(self):
        if self.state is 0 or self.state is None:
            return Color.WHITE.value
        if self.state is 1:
            return Color.RED.value
        if self.state is 2:
            return Color.GREEN.value
