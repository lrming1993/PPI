from PIL import Image
import numpy as np
import math

color_dic = {"white": (231, 234, 235),
             "orage": (239, 113, 5),
             "magenta": (185, 62, 175),
             "light_blue": (47, 164, 212),
             "yellow": (248, 197, 33),
             "lime": (112, 185, 18),
             "pink": (238, 139, 171),
             "gray": (60, 66, 69),
             "silver": (141, 141, 134),
             "cyan": (13, 142, 148),
             "purple": (125, 39, 176),
             "blue": (49, 52, 156),
             "brown": (119, 73, 38),
             "green": (83, 107, 21),
             "red": (161, 34, 29),
             "black": (11, 12, 17)}

max_size = 128
pic = Image.open('test2.jpg')
in_width = pic.width
in_height = pic.height
rate = max_size / max(pic.width, pic.height)
pic = pic.resize((int(in_width * rate), int(in_height * rate)))
pic_array = np.array(pic)
pic_list = pic_array.tolist()


def nearest_color(c):
    min_distance = 65535
    best = "NULL"
    for i in color_dic:
        d = math.sqrt((c[0] - color_dic[i][0])**2 + (c[1] - color_dic[i][1])**2 + (c[2] - color_dic[i][2])**2)
        if d < min_distance:
            best = i
            min_distance = d
    return best

print(nearest_color((250, 194, 221)))

for i in range(len(pic_list)):
    for j in range(len(pic_list[0])):
        best = nearest_color(pic_list[i][j])
        pic_list[i][j] = color_dic[best]


pic_out_array = np.array(pic_list)

img_out = Image.fromarray(np.uint8(pic_out_array))
img_out.show()
