import random
from enum import Enum, auto

import numpy as np

import pygame
from ca.color import Color
from geometry import pixels as px

from ca.grain import Grain, GrainType
from ca.neighbourhood import decide_by_4_rules, Neighbours

CA_METHOD = 'Cellular automata'
MC_METHOD = 'Monte Carlo'

SXRMC = auto()


class FieldVisualisationType(Enum):
    NUCLEATION = auto()
    ENERGY_DISTRIBUTION = auto()


class EnergyDistribution(Enum):
    HETEROGENEOUS = 'heterogeneous'
    HOMOGENEOUS = 'homogeneous'

    def __str__(self):
        return str(self.value)


class NucleationModule(Enum):
    SITE_SATURATED = 'Site saturated'  # constant from beginning
    CONSTANT = 'Constant'  # constant number added after iterations
    INCREASING = 'Increasing'  # increasing number


class FieldNotFilledException(Exception):
    pass


class GrainField:
    def __init__(self, x_size, y_size):
        if type(x_size) or type(y_size) is float:
            x_size = int(x_size)
            y_size = int(y_size)
        self.width = x_size
        self.height = y_size

        # init list
        self.field = [Grain() for y in range(self.height) for x in range(self.width)]
        self.field = np.reshape(np.array(self.field), (self.width, self.height))
        self.coords_list = [(x, y) for y in range(self.height) for x in range(self.width)]
        self.iteration = 0

    @property
    def grains(self):
        """
        :return: all grains in the field
        """
        return self.field.flatten('C')

    @property
    def grains_and_coords(self):
        """
        :return: 3 element tuple (grain, x, y) where grain is Grain object, x, y are coordinates
        """
        result = []
        for x in range(self.field.shape[0]):
            for y in range(self.field.shape[1]):
                result.append((self[x, y], x, y))

        return result

    @property
    def grains_boundaries_points(self):
        """
        :return: point coordinates that lay on grain boundaries.
        """
        result = []
        already_in = set()
        for grain, x, y in self.grains_and_coords:
            # if grain.lock_status is Grain.RECRYSTALIZED:
            if grain.energy_value == 0 or grain.is_locked:
                continue
            if any([neighbour.state != grain.state and neighbour not in already_in
                    for neighbour in self.moore_neighbourhood(x, y) if neighbour is not Grain.OUT_OF_RANGE]):
                result.append((x, y))
            already_in.add(grain)

        return result

    @property
    def grain_boundary_percentage(self):
        """
        :return: The percent of cells that are occupied by INCLUSION state
        """
        # count grain boundary points
        gb_amount = 0
        for grain in self.grains:
            gb_amount += 1 if grain.state is Grain.INCLUSION else 0
        return gb_amount / len(self.grains)

    @property
    def full(self):
        return all([grain.state for grain in self.grains])

    def von_neumann(self, x, y):
        """
        Check grain neighbours in x, y coordinates

        :return: tuple (left, top, right, bottom)
        """
        return (
            self[x - 1, y] if x > 0 else Grain.OUT_OF_RANGE,  # left
            self[x, y - 1] if y > 0 else Grain.OUT_OF_RANGE,  # top
            self[x + 1, y] if x < self.width - 1 else Grain.OUT_OF_RANGE,  # right
            self[x, y + 1] if y < self.height - 1 else Grain.OUT_OF_RANGE,  # bottom
        )

    def moore_neighbourhood(self, x, y):
        """
        Get Moore neighbourhood of cell in given x, y coordinates

        :return: tuple with Grain objects (left, top-left, top, top-right, right, bottom-right, bottom, bottom-left)
        """
        return Neighbours(
            left=self[x - 1, y],  # left
            topleft=self[x - 1, y - 1],  # top-left
            top=self[x, y - 1],  # top
            topright=self[x + 1, y - 1],  # top-right
            right=self[x + 1, y],  # right
            botright=self[x + 1, y + 1],  # bottom-right
            bot=self[x, y + 1],  # bottom
            botleft=self[x - 1, y + 1]  # bottom-left
        )

    def further_moore(self, x, y):
        """
        Get further moore neighbours of cell in given x, y coordinates

        :return: tuple with Grain objects (top-left, top-right, bottom-right, bottom-left)
        """
        return (
            self[x - 1, y - 1],  # top-left
            self[x + 1, y - 1],  # top-right
            self[x + 1, y + 1],  # bottom-right
            self[x - 1, y + 1],  # bottom-left
        )

    def boundary_energy(self, x, y, state: int = None, add_energy: bool = False):
        """
        Calculate boundary energy

        :param x: coord
        :param y: coord
        :param state: state of current cell, can be set to a future cell state (if
        not provided it will be fetched automatically)
        :param add_energy: parameter used during sxrmc simulation. If it's true energy value will be added to the result
        """
        if state is None:
            state = self[x, y].state
        result = 0
        for neighbour in self.moore_neighbourhood(x, y):
            try:
                result += 1 if neighbour.state is not state else 0
            except AttributeError:  # is risen when neighbour is Grain.OUT_OF_RANGE
                pass
        return result if not add_energy else result + self[x, y].energy_value

    def update_mc(self):
        """
        Update field using Monte Carlo method.

        :return: self
        """
        np.random.shuffle(self.coords_list)
        for x, y in self.coords_list:
            if self[x, y].is_locked:
                continue
            neighbours = self.moore_neighbourhood(x, y)
            neighbours = [n for n in neighbours if n is not Grain.OUT_OF_RANGE and not n.is_locked]
            if all([n.state is self[x, y].state for n in neighbours]):
                continue  # all neighbours are same state as considered cells - there will be no change
            energy_before = self.boundary_energy(x, y)
            while True:
                choice = random.choice(neighbours)
                try:
                    if choice.state is self[x, y].state:
                        continue  # choice has the same state as currently considered cell
                except AttributeError:
                    continue  # Grain.OUT_OF_RANGE was chosen
                else:
                    energy_after = self.boundary_energy(x, y, choice.state)
                    break
            de = energy_after - energy_before
            if de <= 0:
                self[x, y].state = choice.state

        self.iteration += 1
        return self

    def update_ca(self, probability=100):
        """
        update grain field state within 1 time step

        :param probability: probability used in rule 4 from decide_state method
        """
        # go through all grains
        # check state - if prev state is not none go next
        # if prev state is none check neighbours and set state
        # update prev state
        for grain, x, y in self.grains_and_coords:
            if not grain.can_be_modified:
                continue
            neighbours = self.moore_neighbourhood(x, y)
            decided_state = decide_by_4_rules(neighbours, probability)
            grain.state = decided_state if decided_state is not None else grain.prev_state

        # after all current states are set - update prev state
        for grain in self.grains:
            grain.prev_state = grain.state

        self.iteration += 1
        return self

    def update_sxrmc(self, nucleation_module=NucleationModule.SITE_SATURATED, iteration_cycle=0, increment=0):
        """
        Update field in terms of SRXMC.

        :param nucleation_module: type of nucleation module
        :param iteration_cycle: number of iterations after which new grains will be added
        :param increment: amount of new grains that will be added
        :return: self
        """
        np.random.shuffle(self.coords_list)
        for x, y in self.coords_list:
            grain = self[x, y]  # type: Grain
            if grain.lock_status is Grain.RECRYSTALIZED or grain.is_locked:
                continue
            neighbours = self.moore_neighbourhood(x, y)
            if not any([grain.lock_status is Grain.RECRYSTALIZED for grain in neighbours if
                        grain is not Grain.OUT_OF_RANGE]):
                continue  # if there are no recrystalized grains in neighbourhood - just continue

            candidate_grain = random.choice(
                [neighbour for neighbour in neighbours if neighbour is not Grain.OUT_OF_RANGE
                 and neighbour.lock_status is Grain.RECRYSTALIZED]
            )

            # calculate energy before
            energy_before = self.boundary_energy(x, y, add_energy=True)
            energy_after = self.boundary_energy(x, y, state=candidate_grain.state, add_energy=False)

            if energy_after <= energy_before:  # accept the change
                # update state to the same as chosen one
                grain.state = candidate_grain.state
                grain.lock_status = Grain.RECRYSTALIZED

        # do actions depending on nucleation module
        if nucleation_module is not NucleationModule.SITE_SATURATED:
            try:
                if not self.iteration % iteration_cycle:  # the moment when we add new grains
                    number_of_grains_to_add = increment * self.iteration // iteration_cycle \
                        if nucleation_module is NucleationModule.INCREASING else increment
                    self.add_recrystalized_grains(number_of_grains_to_add)
            except ZeroDivisionError:  # iteration cycle is 0 - we won't be adding any new grains
                pass

        self.iteration += 1
        return self

    def update(self, simulation_method=CA_METHOD, probability=100):
        if simulation_method == CA_METHOD:
            return self.update_ca(probability)
        elif simulation_method == MC_METHOD:
            return self.update_mc()
        elif simulation_method == SXRMC:
            return self.update_sxrmc()
        return self

    def display(self, screen, resolution, visualisation_type=FieldVisualisationType.NUCLEATION):
        rect = pygame.Rect(0, 0, resolution, resolution)
        max_energy = max([grain.energy_value for grain in self.grains])
        try:
            min_energy = max(min([grain.energy_value for grain in self.grains if grain.energy_value > 0]), 1)
        except ValueError:  # all grains have energy = 0
            min_energy = 1
        for grain, x, y in self.grains_and_coords:
            rect.x = x * resolution
            color = None
            if visualisation_type is FieldVisualisationType.NUCLEATION:
                color = grain.color
            elif visualisation_type is FieldVisualisationType.ENERGY_DISTRIBUTION:
                # color = grain.energy_color
                color = grain.nrg_color(min_energy, max_energy)
            rect.y = y * resolution
            pygame.draw.rect(screen, color, rect)
            # if resolution is less than 5 don't draw borders
            if resolution > 5:
                pygame.draw.rect(screen, Color.BLACK, rect, 1)

    def set_grain_state(self, x, y, state):
        grain = self[x, y]  # type: Grain
        grain.state, grain.prev_state = state, grain.state

    def set_grains(self, pixels, grain_type: GrainType, grain_state=0):
        for x, y in pixels:
            if self.width > x >= 0 and self.height > y >= 0:
                grain = self[x, y]
                grain.type = grain_type
                grain.prev_state = grain_state

    def add_recrystalized_grains(self, num_of_new_grains, on_boundaries=True):
        """
        Add new grains with energy_value = 0.
        Reset iteration amount to 0.

        :param num_of_new_grains:
        :param on_boundaries: determine whether new grains will lay on grain boundaries
        :return: self
        :raises ValueError: when sample size (new number of grains) is larger than number of boundary points
        """
        if all([grain.lock_status is not Grain.ALIVE for grain in self.grains]):
            return self
        # get the maximum state value that is currently present in the field,
        # new grains will have states with higher numbers
        max_state_value = max([max([grain.state for grain in self.grains]), 0])
        max_energy = max([grain.energy_value for grain in self.grains])
        try:
            grains_to_change = random.sample(
                [(x, y) for grain, x, y in self.grains_and_coords if grain.energy_value == max_energy],
                # self.grains_boundaries_points,
                num_of_new_grains
            ) if on_boundaries else \
                random.sample(list(map(lambda item: (item[1], item[2]), self.grains_and_coords)), num_of_new_grains)
        except ValueError:  # sample size is bigger than population
            pass
        else:
            # choose random coords to add new grains
            for x, y in grains_to_change:
                grain = self[x, y]
                grain.state = max_state_value
                grain.energy_value = 0
                grain.lock_status = Grain.RECRYSTALIZED

                max_state_value += 1

        self.iteration = 0

        return self

    def add_inclusion(self, location, size, type='square'):
        """
        Add single inclusion to the field

        :param location: tuple with (x, y) location of the inclusion
        :param size: in case of the square - length of the side, circle - radius
        :param type: either 'circle' or 'square' (must be a string)
        """
        type = type.lower()
        if type != 'square' and type != 'circle':
            type = 'square'

        x_, y_ = location
        coords = []

        if type == 'square':
            coords = px.rectangle(x_, y_, size, size)

        elif type == 'circle':
            coords = px.circle(x_, y_, size)

        for x, y in coords:
            if self.width > x >= 0 and self.height > y >= 0:
                # self[x, y].type = GrainType.INCLUSION
                self[x, y].state = Grain.INCLUSION

    def cells_of_state(self, state):
        """
        Get all cells of one state

        :param state: state to be searched
        :return: list with references to cells of given state
        """
        return [grain for grain in self.grains if grain.state == state]

    def cells_and_coords_of_state(self, state):
        return [(grain, x, y) for grain, x, y in self.grains_and_coords if grain.prev_state == state]

    def cells_of_state_boundary_points(self, state):
        """
        :param state: state to be searched
        :return: list of cells laying on the boundary
        """
        cells = self.cells_and_coords_of_state(state)
        return [(x, y) for grain, x, y in cells if any([
            neighbour.state != grain.state for neighbour in self.moore_neighbourhood(x, y)
            if neighbour is not Grain.OUT_OF_RANGE
        ])]

    def clear_field(self, dual_phase=False, clear_inclusions=False):
        """
        Set all cell states to empty.
        Do not change state of inclusions and locked cells (by default).
        Also set iteration amount to 0.

        :param clear_inclusions:
        :param dual_phase: if set to true, selected grains will be locked and set as dualphase
        :return:
        """
        # first clear all cells that are neither locked nor selected
        for grain in self.grains:
            if grain.state is Grain.INCLUSION and clear_inclusions:
                grain.state = Grain.EMPTY
                continue
            if grain.lock_status is Grain.ALIVE and Grain.state is not Grain.INCLUSION:
                grain.state = Grain.EMPTY
                grain.prev_state = Grain.EMPTY

        # then lock selected
        for grain in self.grains:
            if grain.lock_status is Grain.SELECTED:
                grain.lock_status = Grain.LOCKED if not dual_phase else Grain.DUAL_PHASE

        self.iteration = 0

        return self

    def distribute_energy(self, energy_distribution: EnergyDistribution = EnergyDistribution.HETEROGENEOUS,
                          energy_inside=2, energy_on_edges=5):
        """
        Distribute energy.

        :param energy_distribution: type of energy distribution.
        """
        if not self.full:
            raise FieldNotFilledException('Could not distribute energy. Field is not fully filled.')
        if energy_distribution is EnergyDistribution.HOMOGENEOUS:
            for grain in self.grains:
                grain.energy_value = energy_inside
        elif energy_distribution is EnergyDistribution.HETEROGENEOUS:
            for grain in self.grains:
                grain.energy_value = energy_inside
            for x, y in self.grains_boundaries_points:
                self[x, y].energy_value = energy_on_edges

    def random_inclusions(self, num_of_inclusions, inclusion_size=1, inclusion_type='square'):
        """
        Add random inclusion to field. If field is not empty inclusions will be added on grain boundaries,
        otherwise inclusions will appear in random places.

        :param num_of_inclusions: number of inclusion to be added
        :param inclusion_size: characteristic dimension (radius for circle, side length for square)
        :param inclusion_type: can be either ``'square'`` or ``'circle'``
        :return: self
        """
        if not self:  # if field is empty - put inclusions wherever
            for i in range(num_of_inclusions):
                x, y = random.randrange(0, self.width), random.randrange(1, self.height)
                self.add_inclusion((x, y), inclusion_size, inclusion_type)

        else:  # else put them on grain boundaries
            available_points = self.grains_boundaries_points
            for i in range(num_of_inclusions):
                x, y = random.choice(available_points)
                self.add_inclusion(
                    (x - random.randint(0, inclusion_size // 2), y - random.randint(0, inclusion_size // 2)),
                    inclusion_size,
                    inclusion_type
                )

        return self

    def random_grains(self, num_of_grains):
        """
        Add random grains to the field.

        :param num_of_grains: number of grains to be added.
        """
        for i in range(num_of_grains):
            x, y = random.randrange(1, self.width), random.randrange(1, self.height)
            # if self[x, y].can_be_modified:
            #     self.set_grain_state(x, y, i + 1)
            while self[x, y].lock_status is not Grain.ALIVE:
                x, y = random.randrange(1, self.width), random.randrange(1, self.height)

            self.set_grain_state(x, y, i + 1)
        return self

    def fill_field_with_random_cells(self, num_of_states):
        """
        Fill all field cells with random ids.

        :param num_of_states: number of unique ids that will occur in the field
        """
        if num_of_states is 0:
            return self
        for grain in self.grains:
            if not grain.is_locked:
                val = random.randint(1, num_of_states)
                grain.state = val
                grain.prev_state = val

        return self

    def print_field(self):
        result = '\n'
        for grain, x, y in range(self.width):
            for y in range(self.height):
                grain = self[x, y]
                result += '{} '.format(grain.state)
            result += '\n'
        return result

    def __str__(self):
        result = 'Field {} x {}'.format(self.width, self.height)
        grains = []
        for x in range(self.width):
            for y in range(self.height):
                grains.append(self[x, y])

        if not any([grain.state for grain in grains]):
            return result + ' (empty)'
        elif not all([grain.state for grain in grains]):
            return result + ' (not full)'
        else:
            return result + ' (full)'

    def __bool__(self):
        return any([grain for grain in self.grains])

    def __getitem__(self, item):
        try:
            if item[0] < 0 or item[1] < 0:  # get rid of negative indices
                raise IndexError
            return self.field[item[0], item[1]]
        except IndexError:
            return Grain.OUT_OF_RANGE

    def __setitem__(self, key, value):
        self[key] = value

    def __iter__(self):
        return self.field.__iter__()


def random_field(size_x, size_y, num_of_grains):
    field = GrainField(size_x, size_y)
    for x in range(num_of_grains):
        field.set_grain_state(
            random.randrange(1, size_x),
            random.randrange(1, size_y),
            x + 1
        )

    return field
