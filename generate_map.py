from io import BytesIO
from PIL import Image

ARROW_PATH = 'maps/arrow_blue_trans.tif'
MAP_PATH = 'maps/new_map.jpg'

def generate_map(route, angle):
    arrow = Image.open(ARROW_PATH)
    arrow = arrow.convert('RGBA')
    arrow_w, arrow_h = arrow.size
    map = Image.open(MAP_PATH)
    map = map.convert('RGBA')
    map_w, map_h = map.size
    background = Image.new('RGBA', (map_w, map_h), (0, 0, 0, 0))

    # Offset of arrow on the map
    offset = ((map_w - arrow_w) // 2, (map_h - arrow_h) // 15)

    # rotation of arrow
    arrow_rt = arrow.rotate(angle)
    # Arrow_rt.show()

    # Pasting of arrow to Map
    # Map.paste(Arrow_rt, offset)
    background.paste(arrow_rt, offset)
    # Map = Map.convert('RGB')
    map = Image.alpha_composite(background, map)
    map = Image.alpha_composite(map, background)
    map = map.convert('RGB')
    # save

    # map.save(map_with_arrow, format='JPEG')
    image_bytes = BytesIO()
    image_bytes.name = 'result.jpeg'
    map.save(image_bytes, format='JPEG')
    image_bytes.seek(0)
    return image_bytes


def rotate(image):
    image.rotate()

