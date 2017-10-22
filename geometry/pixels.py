from math import sqrt


def rectangle(x, y, w, h):
    """
    Get pixels to draw a rectangle

    :param x: top left corner x
    :param y: top left corner y
    :param w: width of the rectangle
    :param h: height of the rectangle
    :return: all pixels belonging to rectangle as (x, y) tuple
    """

    result = []
    for xx in range(w):
        for yy in range(h):
            result.append((xx + x, yy + y))

    return result


def circle(x_center, y_center, radius, filled=True):
    """
    Get pixels to draw a circle

    :param x_center: x coordinate of circle center
    :param y_center: y coordinate of circle center
    :param radius: radius of the circle
    :param filled: if false only pixels on the border will be returned
    :return: pixels belonging to the circle
    """
    points = []
    octant = []  # list with (x, y) tuples of points in first octant
    x, y = radius, 0

    octant.append((x, y))  # first point being (r, 0)
    # calculate first octant (arc 0 - 45 deg)
    while x > y:
        # increment y
        y += 1
        # do calculations
        # x = sqrt(r^2 - y^2)
        # src: https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
        x = int(round((sqrt(radius ** 2 - y ** 2)), 0))
        octant.append((x, y))

    # translations, source: https://www.tutorialspoint.com/computer_graphics/circle_generation_algorithm.htm
    for a, b in octant:
        points.extend([
            (a, b),     # 0 - 45
            (b, a),     # 45 - 90
            (-b, a),    # 90 - 135
            (-a, b),    # 135 - 180
            (-a, -b),   # 180 - 225
            (-b, -a),   # 225 - 270
            (b, -a),    # 270 - 315
            (a, -b),    # 315 - 360
        ])
    result = []
    for a, b in points:
        a += x_center
        b += y_center
        result.append((a, b))

    if not filled:
        return result

