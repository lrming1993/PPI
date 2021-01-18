from PIL import Image
import numpy as np
import math

color_dic = {"white": (255, 255, 255),
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
pic = Image.open('test.jpg')
in_width = pic.width
in_height = pic.height
rate = max_size / max(pic.width, pic.height)
pic = pic.resize((int(in_width * rate), int(in_height * rate)))
pic_array = np.array(pic)
pic_list = pic_array.tolist()


def nearest_color(c):
    min_distance = 65535
    best = "NULL"
    r = c[0]
    g = c[1]
    b = c[2]
    if r + g + b == 0:
        r = g = b = 1
    k = math.sqrt(r**2 + g**2 + b**2)
    r_ = r/k
    g_ = g/k
    b_ = b/k
    w0 = 1      # rgb 2-norm
    w1 = 1      # normalized rgb vector distance
    w2 = 1      # brightness
    w3 = 1      # rgb 1-norm
    w4 = 1      # normalized rgb 2-norm
    w5 = 1
    for i in color_dic:

        # d = abs(c[0] - color_dic[i][0]) + abs(c[1] - color_dic[i][1]) +abs(c[2] - color_dic[i][2])
        _r = color_dic[i][0]
        _g = color_dic[i][1]
        _b = color_dic[i][2]
        _k = math.sqrt(_r**2 + _g**2 + _b**2)
        _r_ = _r/_k
        _g_ = _g/_k
        _b_ = _b/_k

        # d0 = abs(c[0] - color_dic[i][0]) + abs(c[1] - color_dic[i][1]) +abs(c[2] - color_dic[i][2])
        d0 = math.sqrt((r - _r)**2 + (g - _g)**2 + (b - _b)**2) / math.sqrt(255**2 * 3)
        d1 = - (r_*_r_ + g_*_g_ + b_*_b_ - 1)/2
        d2 = abs(k/255 - _k/255)
        d3 = (abs(r - _r) + abs(g - _g) + abs(b - _b)) / (255*3)
        d4 = math.sqrt((r_ - _r_)**2 + (g_ - _g_)**2 + (b_ - _b_)**2)
        avg = (r + _r) / 2
        d5 = math.sqrt((2 + avg/256)*(r - _r)**2 + 4*(g - _g)**2 + (2 + (255 - avg)/256)*(b - _b)**2) / (3*255)
        d = w0*d0 + w1*d1 + w2*d2 + w3*d3 + w4*d4 + w5*d5
        if d < min_distance:
            best = i
            min_distance = d
    return best

# print(nearest_color((250, 194, 221)))

for i in range(len(pic_list)):
    for j in range(len(pic_list[0])):
        best = nearest_color(pic_list[i][j])
        pic_list[i][j] = color_dic[best]


pic_out_array = np.array(pic_list)

img_out = Image.fromarray(np.uint8(pic_out_array))
img_out.show()
