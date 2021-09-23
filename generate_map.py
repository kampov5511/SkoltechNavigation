from io import BytesIO
import sys
from PIL import Image, ImageDraw


#MAP_PATH = "/content/sample_data/map_pr.jpg"
MAP_PATH = ['map/1fl_light_LR.png','map/2fl_light_LR.png','map/3fl_light_LR.png']
MAP_RES_NAME = ["1fl_result.jpg", "2fl_result.jpg", "3fl_result.jpg"]
RED_POINT_PATH = "map/red_point.png"
VIEW_CON_PATH = "map/view_con.png"
angle = 50
num_shelf = 3

QR_FL = {'201': 2, '202': 2, '203': 2, '204': 2, '205': 2, 
           '206': 2, '207': 2, '301': 3, '302': 3, '303': 3,
           '304': 3, '305': 3, '306': 3, '307': 3}
QR_LIST = {'201': (646, 817), '202': (518, 722), '203': (455, 618), '204': (429, 511), '205': (442, 452), 
           '206': (415, 361), '207': (718, 786), '301': (420, 349), '302': (474, 337), '303': (533, 337),
           '304': (588, 333), '305': (415, 622), '306': (471, 660), '307': (531, 655)}

route = ['201', '202', '203', '204', '205', '206', '301', '302']

#draw points on the path
#1 yes
#0 no
SHOW_POINTS = 1

#draw line between two points
def draw_line(point1, point2, draw) :
  draw.line((point1[0], point1[1]) + (point2[0], point2[1]), fill=(243, 70, 0), width = 3)

#draw all path using path and map
def draw_path(route, map):
  draw = []
  for i in range(3):
    draw.append(ImageDraw.Draw(map[i]))
  for i in range(len(route) - 1):
    if QR_FL[route[i]] == QR_FL[route[i+1]]:
      draw_line(QR_LIST[route[i]], QR_LIST[route[i+1]], draw[QR_FL[route[i]]-1])

#draw a rectangle using number of shelf
def draw_rect(num, map):
  draw = ImageDraw.Draw(map)
  draw.rectangle(CORNER_LIST[num], fill = (242, 119, 119, 100))

def generate_map(route):
    #open blank map, convert to RGBA, get a size
    flag = [0, 0, 0]
    for i in range(len(route)):
      flag[QR_FL[route[i]] - 1] = 1
    map_w = []
    map_h = []
    map = [Image.open(MAP_PATH[0]), Image.open(MAP_PATH[1]), Image.open(MAP_PATH[2])]
    for i in range(3):
      map[i] = map[i].convert("RGBA")
      map_w.append(map[i].size[0])
      map_h.append(map[i].size[1])

    #open picture of point, convert to RGBA, get a size
    red_point = Image.open(RED_POINT_PATH)
    red_point_w, red_point_h = red_point.size
    

    #Layer for adding some objects with alpha chanel
    Overlayer = []
    for i in range(3): 
      Overlayer.append(Image.new("RGBA", (map_w[i], map_h[i]), (0,0,0,0))) 
    draw_path(route, map)
    if SHOW_POINTS != 0:
      for i in range(len(route)):
        offset = QR_LIST[route[i]][0] - (red_point_w // 2), QR_LIST[route[i]][1] - (red_point_h // 2)
        Overlayer[QR_FL[route[i]]-1].paste(red_point,offset)
    #offset = QR_LIST[route[0]][0] - (view_con_w // 2), QR_LIST[route[0]][1] - (view_con_h // 2)
    
    Background = Image.new("RGBA", (map_w[1], map_h[1]), (255,255,255,255))
    for i in range(3):
      map[i] = Image.alpha_composite(Background, map[i])     
      map[i] = Image.alpha_composite(map[i],Overlayer[i])
    
    image_bytes = []
    for i in range(3):
      map[i] = map[i].convert("RGB")
      if flag[i]:
        image_bytes.append(BytesIO())
        image_bytes[-1].name = MAP_RES_NAME[i]  
        map[i].save(image_bytes, format = "JPEG")
        image_bytes[-1].seek(0)  
    return image_bytes    
