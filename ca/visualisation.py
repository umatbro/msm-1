import itertools
import pygame

from ca.grain import Grain
from ca.grain_field import GrainField, FieldVisualisationType, NucleationModule, CA_METHOD, MC_METHOD, SXRMC
from files import export_image, export_text, import_text

MAX_FRAMES = 60


def run_field(
        grain_field: GrainField,
        resolution: int=1,
        simulation_method=CA_METHOD,
        probability: int=100,
        iterations_limit: int=10,
        paused=False,
        update_function=None,
):
    """
    Visualise grain field

    :param grain_field: field to be visualized
    :param resolution: length of square side (in pixels)
    :param simulation_method: method used to simulate growth (can be either ca or mc)
    :param probability: probability used in ca method
    :param paused: whether simulation starts paused or not
    :param iterations_limit: number of iterations after which visualisation will pause
    :param update_function: custom function that can be provided to update grain field
    :return: grain field object after visualisation
    """
    if update_function is None:
        update_function = lambda: grain_field.update(simulation_method, probability)
    pygame.init()

    window_width = grain_field.width * resolution
    window_height = grain_field.height * resolution

    # create screen
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Grain field')

    # create clock
    clock = pygame.time.Clock()
    total_time = 0

    # selected cells
    selected_cells = {}
    iterations_num_font = pygame.font.SysFont('monospace', 48 if resolution >= 6 else 24, bold=True)

    visualisation_type = FieldVisualisationType.NUCLEATION
    visualisation_type_toggler = itertools.cycle(FieldVisualisationType.__members__.values())

    # main loop
    while 1337:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                return grain_field, selected_cells
                # sys.exit(0)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
                pygame.quit()
                return grain_field, selected_cells
                # sys.exit(0)
            elif event.type is pygame.KEYDOWN:
                if event.key is pygame.K_SPACE:
                    update_function()
                elif event.key is pygame.K_TAB:
                    visualisation_type = next(visualisation_type_toggler)
                elif event.key is pygame.K_e:
                    grain_field.distribute_energy()
                elif event.key is pygame.K_i:
                    export_image(grain_field)
                elif event.key is pygame.K_t:
                    export_text(grain_field)
                elif event.key is pygame.K_l:
                    grain_field = import_text('field.txt')
                elif event.key is pygame.K_p:
                    paused = not paused
                elif event.key is pygame.K_n:
                    grain_field.clear_field(dual_phase=True)
                elif event.key is pygame.K_b:
                    points = []
                    if not any([grain.lock_status is Grain.SELECTED for grain in grain_field.grains]):
                        points = grain_field.grains_boundaries_points
                    else:
                        for state, cells in selected_cells.items():
                            points.extend(grain_field.cells_of_state_boundary_points(state))
                            for cell in cells:
                                cell.lock_status = Grain.ALIVE
                    # points = grain_field.cells_of_state_boundary_points(1)
                    for point in points:
                        grain_field[point].state = Grain.INCLUSION
                    print(grain_field.grain_boundary_percentage)
            elif event.type is pygame.MOUSEBUTTONDOWN:
                # clicking on grains selects them
                gx, gy = mouse2grain_coords(pygame.mouse.get_pos(), resolution)
                grain = grain_field[gx, gy]
                if simulation_method == CA_METHOD:
                    state = grain.prev_state
                elif simulation_method == MC_METHOD:
                    state = grain.state
                else:
                    state = grain.state

                if grain.lock_status is Grain.SELECTED:
                    # unlock it then
                    for cell in selected_cells[state]:
                        cell.lock_status = Grain.ALIVE
                    del selected_cells[state]
                elif state is not Grain.INCLUSION and not grain.is_locked or grain.lock_status is not Grain.RECRYSTALIZED:
                    selected_cells[state] = grain_field.cells_of_state(state)
                    for cell in selected_cells[state]:  # type: Grain
                        cell.lock_status = Grain.SELECTED
                print('selected {} (lock_state: {})'.format(state, grain.lock_status))

        total_time += clock.tick(MAX_FRAMES)

        # m_pos = pygame.mouse.get_pos()
        # display iterations
        label = iterations_num_font.render('{}'.format(grain_field.iteration), 1, (0, 0, 0))

        if grain_field.iteration == iterations_limit:
            paused = True if not grain_field.iteration == 0 else False

        grain_field.display(screen, resolution, visualisation_type)
        screen.blit(label, (window_width - 80, window_height - 80))
        pygame.display.update()

        if not paused:
            update_function()
            # grain_field.update(simulation_method, probability)
            if simulation_method == CA_METHOD and grain_field.full:
                paused = True
            if simulation_method == SXRMC and all([grain.energy_value == 0 for grain in grain_field.grains]):
                paused = True


def mouse2grain_coords(mpos, resolution):
    """Get mouse coords and convert to field coords based on given resolution"""
    mx, my = mpos
    return mx//resolution, my//resolution


if __name__ == '__main__':
    import os
    from files import import_text, import_pickle
    field = import_pickle(os.path.join(os.getcwd(), '..', 'example_fields', 'mc_300x300.pickle'))
    field.distribute_energy(energy_on_edges=5, energy_inside=2)
    field.add_recrystalized_grains(10)
    update_function = lambda: field.update_sxrmc(
        nucleation_module=NucleationModule.INCREASING,
        iteration_cycle=5,
        increment=10
    )
    gf=GrainField(100, 100)
    gf.random_grains(10)
    run_field(field, resolution=2, iterations_limit=10, probability=50, simulation_method=SXRMC, paused=True, update_function=update_function)