from color import Color


class Grain:
    def __init__(self, state=None):
        self.prev_state = state
        self.state = state

    def check_neighbours(self):
        pass

    @property
    def color(self):
        state = self.prev_state
        if state is 0 or state is None:
            return Color.WHITE.value
        if state is 1:
            return Color.RED.value
        if state is 2:
            return Color.GREEN.value
        if state is 3:
            return Color.BLUE.value
        return Color.GREY.value
