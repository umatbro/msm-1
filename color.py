from enum import Enum


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