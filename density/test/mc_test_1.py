import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt
from PIL import Image

output_width = -1
output_height = -1
output_max = 20
input_img = 'test2.jpg'

I = image.imread(input_img)
list_I = I.tolist()
input_width = len(I[0])
input_height = len(I)
print("Image file name:", input_img)
print('Original image:\nWidth:', input_width, "\nHeight:", input_height)

rate = output_max / max(input_width, input_height)
I_out = np.zeros([int(input_height * rate), int(input_width * rate), 3])
I_out.tolist()
for i in range(int(input_height * rate)):
    for j in range(int(input_width * rate)):
        I_out[i][j] = list_I[int(i/rate)][int(j/rate)]
I_out = np.array(I_out)
temp = plt.imshow(I_out)
plt.show()


