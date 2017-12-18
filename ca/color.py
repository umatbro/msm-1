import operator

CONS = 5


def sub_tuples(a, b):
    return tuple(map(operator.sub, a, b))


def constrain(value, min_val, max_val):
    if value > max_val - 70:
        return max_val - 70
    return max(min_val, min(value, max_val))


class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (125, 124, 125)
    LIGHTPINK = (255, 182, 193)

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
        if state is 0 or state is None:
            return Color.WHITE

        if state % 5 == 0:
            return sub_tuples(Color.BLUE, (0, 0, constrain(state//3 * CONS, 0, 255)))
        if state % 5 == 1:
            return sub_tuples(Color.GREEN, (0, constrain(state//3 * CONS, 0, 255), 0))
        if state % 5 == 2:
            return sub_tuples(Color.RED, (constrain(state//3 * CONS, 0, 255), 0, 0))
        if state % 5 == 3:
            return (0, 255 - constrain(state//3 * CONS, 0, 255), 255 - constrain(state//3 * CONS, 0, 255))
        if state % 5 == 4:
            return (255 - constrain(state//3 * CONS, 0, 255), 255- constrain(state//3 * CONS, 0, 255), 0)
        return Color.GREY

    @staticmethod
    def convert_color_to_state(color) -> int:
        """
        Convert color (r, g, b) to a grain state (int)

        :param color: tuple with (r, g, b) values
        :return: integer with state
        """
        if len(color) is not 3:
            raise ValueError('Function parameter must be a 3 element tuple')
        if not all([0 <= value <= 255 for value in color]):
            raise ValueError('Invalid color values (must be between 0 - 255')
        if color is (255, 255, 255):
            return 0  # Grain.EMPTY
        if color is (0, 0, 0):
            return -1  # Grain.INCLUSION
        r, g, b = color

        def calc_state(value):
            return ((255 - value) * 3) // CONS

        if r and not g and not b:
            # value = 255 - state//3 * cons => state = (255 - value) * 3 / cons
            return calc_state(r)
        if g and not r and not b:
            return calc_state(r)


def hex2rgb(hex_code: str) -> tuple:
    h = hex_code.lstrip('#')
    return tuple(int(h[i: i+2], 16) for i in (0, 2, 4))
