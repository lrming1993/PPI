import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt

I = image.imread('test.jpg')
print(I.shape)
print(len(I[0]))
plt.imshow(I)

