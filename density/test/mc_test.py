import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt

output_width = -1
output_height = -1
output_max = 128
input_img = 'test.jpg'

I = image.imread(input_img)
input_width = len(I[0])
input_height = len(I)
print("Image file name:", input_img)
print('Original image:\nWidth:', input_width, "\nHeight:", input_height)

window_height = -1
window_width = -1
if output_max != -1:
    print("Mode: max height/width =", output_max)
    m = max(input_width, input_height)
    window_width = window_height = m // output_max
    if window_width * (m // output_max) != input_width or

elif output_width != -1 and output_height == -1:
    print("Mode: width =", output_width, "(keep width/height rate)")
    window_width = window_height = input_width // output_width

elif output_height != -1 and output_width == -1:
    print("Mode: height =", output_height, "(keep width/height rate)")
    window_width = window_height = input_height / output_height
window_width_num = input_width // window_width
window_height_num = input_height // window_height


def avg_pixels_matrix(pixels):
    temp = pixels.sum(axis=0)
    temp = temp.sum(axis=0)
    temp = temp / (len(pixels) * len(pixels[0]))
    return temp

temp_output = []
for i in range(window_width_num - 1):
    temp_column = []
    for j in range(window_height_num - 1):
        p = avg_pixels_matrix(I[j * window_height:(j + 1) * window_height, i * window_width:(i + 1) * window_width])
        temp_column.append(p)
    if window_height * window_height_num != input_height:
        p = avg_pixels_matrix(I[window_height_num * window_height:, i * window_width:(i + 1) * window_width])
        temp_column.append(p)
    temp_output.append(temp_column)
    if window_width * window_width_num != input_width:
        temp_output = []
        for j in range(window_height_num - 1):
            p = avg_pixels_matrix(I[j * window_height:(j + 1) * window_height, window_width_num * window_width:])
            temp_column.append(p)
        if window_height * window_height_num != input_height:
            p = avg_pixels_matrix(I[window_height_num * window_height:, window_width_num * window_width:])
            temp_column.append(p)
        temp_output.append(temp_column)
print(temp_output)
output_matrix = np.array(temp_output)
print(output_matrix)
output_matrix.swapaxes(0, 1)



temp = plt.imshow(output_matrix)
plt.show()

