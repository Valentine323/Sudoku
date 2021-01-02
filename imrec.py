import cv2
import numpy as np
import matplotlib.pyplot as plt

img=cv2.imread('1.jpg',0)
print(img.shape)
(height, width)=img.shape
blurred=cv2.gaussianblur(img,(11,11),1)
resized=cv2.resize(blurred,(int(5000*width/(width+height)+0.5), int(5000*height/(width+height)+0.5)))
print(resized.shape)
tresh=cv2.adaptivethreshold(resized, 255, cv2.adaptive_thresh_gaussian_c, cv2.thresh_binary_inv,11,3)
median=cv2.medianblur(tresh,7)
closed=cv2.morphologyex(median,cv2.morph_close,(11,11))

stats=cv2.connectedcomponentswithstats(closed)
indx=np.argsort(stats[2][:, -1])[::-1]
sorted=stats[2][indx]
grid=np.zeros(closed.shape,dtype=np.bool)
grid[stats[1]==indx[1]]=True;



plt.imshow(grid,'gray')
plt.show()

