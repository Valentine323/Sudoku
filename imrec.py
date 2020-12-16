import cv2
import numpy as np
import matplotlib.pyplot as plt

img=cv2.imread('1.jpg',0)
print(img.shape)
(height, width)=img.shape
blurred=cv2.GaussianBlur(img,(11,11),1)
resized=cv2.resize(blurred,(int(5000*width/(width+height)+0.5), int(5000*height/(width+height)+0.5)))
print(resized.shape)
tresh=cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,3)
median=cv2.medianBlur(tresh,7)
closed=cv2.morphologyEx(median,cv2.MORPH_CLOSE,(11,11))

stats=cv2.connectedComponentsWithStats(closed)
indx=np.argsort(stats[2][:, -1])[::-1]
sorted=stats[2][indx]
grid=np.zeros(closed.shape,dtype=np.bool)
grid[stats[1]==indx[1]]=True;



plt.imshow(grid,'gray')
plt.show()

