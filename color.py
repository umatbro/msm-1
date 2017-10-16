from enum import Enum
import operator


def sub_tuples(a, b):
    return tuple(map(operator.sub, a, b))


def constrain(value, min_val, max_val):
    # if value > max_val - 70:
    #     return max_val - 70
    return max(min_val, min(value, max_val))


class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (125, 124, 125)

    default_colors = [
        RED,
        GREEN,
        BLUE
    ]

    @staticmethod
    def get_color(index):
        return Color.default_colors[index]

    @staticmethod
    def state_color(state):
        cons = 10
        if state is 0 or state is None:
            return Color.WHITE.value
        if state % 3 == 0:
            return sub_tuples(Color.BLUE.value, (0, 0, constrain(state/3 * cons, 0, 255)))
        if state % 3 == 1:
            return sub_tuples(Color.GREEN.value, (0, constrain(state/3 * cons, 0, 255), 0))
        if state % 3 == 2:
            return sub_tuples(Color.RED.value, (constrain(state/3 * cons, 0, 255), 0, 0))
        return Color.GREY.value
