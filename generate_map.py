from io import BytesIO
from PIL import Image, ImageDraw

MAP_PATH = 'maps/new_map.jpg'
RED_POINT_PATH = "maps/red_point.png"
VIEW_CON_PATH = "maps/view_con.png"
PICTURE_ROOT = "maps/pictures"
EM_LIST_PATH = {1: "banana.png", 2: "pineapple.png", 3: "apple.png", 4: "cherry.png", \
                5: "beer.png", 6: "bomb.png", 7: "watergun.png", 8: "18.png", \
                9: "mushroom.png", 10: "palm.png", 11: "burger.png", 12: "chocolate.png"}


#coordinates of qr-codes on the map
QR_LIST = {"1": (100, 100), "2": (100, 250), "3": (100, 400), "4": (100, 550), "5": (100, 700), "6": \
  (350, 700), "7": (350, 550), "8": (350, 400), "9": (350, 250), "10": (350, 100), "11":(600, 100), \
  "12": (600, 250), "13": (600, 400), "14": (600, 550), "15": (600, 700)}

CORNER_LIST = {1: ((180, 180), (218, 337)), 2: ((180, 339), (220, 490)), 3: ((180, 492), (219, 648)), \
               4: ((223, 492), (262, 647)), 5: ((223, 339), (263, 490)), 6: ((223, 183), (264, 337)), \
               7: ((440, 183), (480, 338)), 8: ((440, 341), (480, 489)), 9: ((441, 492), (479, 645)), \
               10: ((484, 492), (524, 646)), 11: ((485, 341), (524, 489)), 12: ((484, 183), (524, 339))}

#draw points on the path
#1 yes
#0 no
SHOW_POINTS = 1

#draw line between two points
def draw_line(point1, point2, draw) :
  draw.line((point1[0], point1[1]) + (point2[0], point2[1]), fill=(243, 70, 0), width = 3)

#draw all path using path and map
def draw_path(route, map):
  draw = ImageDraw.Draw(map)
  for i in range(len(route) - 1):
    draw_line(QR_LIST[route[i]], QR_LIST[route[i+1]], draw)

#draw a rectangle using number of shelf
def draw_rect(num, map):
  draw = ImageDraw.Draw(map)
  draw.rectangle(CORNER_LIST[num], fill = (242, 119, 119, 100))

def generate_map(route, angle, shelf):
    #open blank map, convert to RGBA, get a size
    map = Image.open(MAP_PATH)
    map = map.convert("RGBA")
    map_w, map_h = map.size

    #open picture of point, convert to RGBA, get a size
    red_point = Image.open(RED_POINT_PATH)
    red_point = red_point.convert("RGBA")
    red_point_w, red_point_h = red_point.size
    
    #image of view cone
    view_con = Image.open(VIEW_CON_PATH)
    view_con = view_con.convert("RGBA")
    view_con_w, view_con_h = view_con.size

    #angle contraclockwise from vertical
    view_con = view_con.rotate(angle)

    #Layer for adding some objects with alpha chanel
    Overlayer = Image.new("RGBA", (map_w, map_h), (0,0,0,0))
    draw_path(route, map)
    if SHOW_POINTS != 0:
      for i in range(len(route)):
        offset = QR_LIST[route[i]][0] - (red_point_w // 2), QR_LIST[route[i]][1] - (red_point_h // 2)
        Overlayer.paste(red_point,offset)
    offset = QR_LIST[route[0]][0] - (view_con_w // 2), QR_LIST[route[0]][1] - (view_con_h // 2)
    Overlayer.paste(view_con,offset)
    draw_rect(shelf, Overlayer)
    
    Overlayer2 = Image.new("RGBA", (map_w, map_h), (0,0,0,0))
    for i in range(12):
      pic = Image.open(PICTURE_ROOT + "/" + EM_LIST_PATH[i + 1])
      pic.convert("RGBA")
      pic_w, pic_h = pic.size
      offset = (CORNER_LIST[i + 1][0][0] + CORNER_LIST[i + 1][1][0] - pic_w) // 2, (CORNER_LIST[i + 1][0][1] + CORNER_LIST[i + 1][1][1] - pic_h) // 2
      Overlayer2.paste(pic, offset)
      
    map = Image.alpha_composite(map,Overlayer)
    map = Image.alpha_composite(map,Overlayer2)

    map = map.convert("RGB")

    image_bytes = BytesIO()
    image_bytes.name = 'result.jpeg'
    map.save(image_bytes, format='JPEG')
    image_bytes.seek(0)
    return image_bytes



