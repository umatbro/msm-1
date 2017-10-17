import sys

from PIL import Image

from ca.grain_field import GrainField


def export_text(grain_field: GrainField, path_file='field.txt'):
    filename = path_file if path_file.endswith('.txt') else path_file + '.txt'
    with open(filename, 'w') as file:
        w, h = grain_field.width, grain_field.height
        # first line with size
        file.write('{} {}\n'.format(w, h))
        for x in range(w):
            for y in range(h):
                file.write('{x} {y} {id}\n'.format(x=x, y=y, id=grain_field.field[x][y].state))

    print('Text file saved successfully')


def export_image(grain_field, path_file='field_img.png'):
    filename = path_file if path_file.endswith('.png') else path_file + '.png'

    w, h = grain_field.width, grain_field.height

    image = Image.new('RGB', (w, h))
    pixels = image.load()
    for x in range(w):
        for y in range(h):
            r, g, b = grain_field.field[x][y].color
            pixels[x, y] = (r, g, b)

    image.save(filename, 'PNG')
    print('Image saved successfully')


def import_text(source):
    """
    Read text file and get grain field stored in it

    :param source: path to the file
    :return: GrainField object
    """
    with open(source, 'r') as file:
        lines = file.readlines()
        x_size, y_size = tuple(map(int, lines[0].rstrip().split(' ')))  # rstrip removes newline character at the end of the line

        resolution = 6 if x_size <= 300 and y_size <= 150 else 1

        grain_field = GrainField(x_size, y_size, resolution)
        for i, line in enumerate(lines[1:]):
            try:
                x, y, state = line.rstrip().split(' ')
                x, y = tuple(map(int, (x, y)))
                state = 0 if state == 'None' else int(state)
                grain_field.set_grain_state(x, y, state)
                # grain_field.field[x][y].state = state
                # grain_field.field[x][y].prev_state = state
            except ValueError:
                print('Error in line {}'.format(i + 2))

        return grain_field


def import_img(source):
    pass

