from PIL import Image

from ca.grain_field import GrainField
from ca.grain import Grain, GrainType


def export_text(grain_field: GrainField, path_file='field.txt'):
    """
    Export grain field to a text file

    :param grain_field: GrainField object to be exported
    :param path_file: path to the file

    First line of the file contains grid dimensions.
    Following lines: <x> <y> <state>
    """
    filename = path_file if path_file.endswith('.txt') else path_file + '.txt'
    with open(filename, 'w') as file:
        # first line with size
        file.write('{} {}\n'.format(grain_field.width, grain_field.height))
        for grain, x, y in grain_field.grains_and_coords:
            file.write('{x} {y} {id}\n'.format(
                x=x,
                y=y,
                id=grain.state if grain.type is not GrainType.INCLUSION else -1
            ))

    print('Text file saved successfully')


def export_image(grain_field: GrainField, path_file='field_img.png'):
    """
    Export grain field as a png image

    :param grain_field: GrainField object to be exported
    :param path_file: path to save the image
    """
    filename = path_file if path_file.endswith('.png') else path_file + '.png'
    print(filename)

    image = Image.new('RGB', (grain_field.width, grain_field.height))
    pixels = image.load()
    for grain, x, y in grain_field.grains_and_coords:
        pixels[x, y] = grain.color

    image.save(filename, 'PNG')
    print('Image saved successfully')


def import_text(source: str) -> GrainField:
    """
    Read text file and get grain field stored in it

    :param source: path to the file
    :return: GrainField object
    """
    with open(source, 'r') as file:
        lines = file.readlines()
        x_size, y_size = tuple(map(int, lines[0].rstrip().split(' ')))  # rstrip removes newline character at the end of the line

        grain_field = GrainField(x_size, y_size)
        for i, line in enumerate(lines[1:]):
            try:
                x, y, state = line.rstrip().split(' ')
                x, y = tuple(map(int, (x, y)))
                state = 0 if state == 'None' else int(state)
                if state is not Grain.INCLUSION:
                    grain_field.set_grain_state(x, y, state)
                else:
                    grain_field.add_inclusion((x, y), 1, type='square')
            except ValueError:
                print('Error in line {}'.format(i + 2))

        return grain_field


def import_img(source: str) -> GrainField:
    pass

