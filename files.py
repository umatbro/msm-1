from PIL import Image

from ca.grain_field import GrainField


def export_text(grain_field: GrainField, path_file='field.txt'):
    filename = path_file if path_file.endswith('.txt') else path_file + '.txt'
    with open(filename, 'w') as file:
        w, h = grain_field.width, grain_field.height
        # first line with size
        file.write('Size: {} {}\n'.format(w, h))
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
    pass


def import_img(source):
    pass

