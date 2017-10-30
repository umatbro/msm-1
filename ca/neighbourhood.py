import random
import operator
from collections import namedtuple, Counter
from statistics import mode, StatisticsError

from ca.grain import Grain

Neighbours = namedtuple('Neighbours', ['left', 'topleft', 'top', 'topright', 'right',
                                       'botright', 'bot', 'botleft'])


def decide_state(neighbours):
    """
    Decide which state should be chosen based on amount of surrounding neighbours.

    :param neighbours: neighbour grains from which to pick state.
    :return: state to be set or None if state cannot be set.
    """
    # list of surrounding states
    unq_states = [neighbour.prev_state for neighbour in neighbours if
                  neighbour is not Grain.OUT_OF_RANGE and neighbour.prev_state > 0]

    if not unq_states:  # if states list is empty - return none
        return None
    try:
        # mode function returns the item that occurred most times in a list
        return mode(unq_states)
    except StatisticsError:
        # if the amount is the same - choose random element
        return random.choice(unq_states)


def decide_by_4_rules(moore_neighbours: Neighbours, probability=50):
    """
    Update grain field according to 4 consecutive rules:
    1. Moore (5-8 cells)
    2. Nearest Moore (min 3 neighbour cells)
    3. Further Moore (min 3 neighbour cells)
    4. Id of cell depends on cell of all neighbours and

    :param moore_neighbours:
    :param probability:
    :return: output state of the cell (based on neighbours or *None* if state could not be chosen
    """
    # rule 1
    mn = moore_neighbours
    states = [grain.prev_state for grain in mn if grain is not Grain.OUT_OF_RANGE and grain.has_unq_state]
    if not states:
        return None
    counter = Counter(states)
    value, occurrences = max(counter.items(), key=operator.itemgetter(1))
    if occurrences >= 5:
        return value

    # rule 2
    nearest_moore = mn.left, mn.top, mn.right, mn.bot
    counter = Counter(nearest_moore)
    value, occurrences = max(counter.items(), key=operator.itemgetter(1))
    if occurrences >= 3:
        return value

    # rule 3
    further_moore = mn.topleft, mn.topright, mn.botright, mn.botleft
    counter = Counter(further_moore)
    value, occurrences = max(counter.items(), key=operator.itemgetter(1))
    if occurrences >= 3:
        return value

    # rule 4
    try:
        return random.choice(states) if random.randint(0, 100) <= probability else None
    except IndexError:
        return None
