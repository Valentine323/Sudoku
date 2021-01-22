import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('1.jpg', 0)
print(img.shape)
(height, width)=img.shape
blurred = cv2.GaussianBlur(img, (11, 11), 1)
resized = cv2.resize(blurred, (int(5000*width/(width+height)+0.5), int(5000*height/(width+height)+0.5)))
print(resized.shape)
tresh = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)
median = cv2.medianBlur(tresh, 7)
closed = cv2.morphologyEx(median, cv2.MORPH_CLOSE, (11, 11))

stats = cv2.connectedComponentsWithStats(closed)
indx = np.argsort(stats[2][:, -1])[::-1]
sorted = stats[2][indx]
grid = np.zeros(closed.shape, dtype=np.uint8)
grid[stats[1] == indx[1]] = 255

(contours, _) = cv2.findContours(grid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
help_list = []
max_countour=[]
for contour in contours:
    # Vypočtení obvodu uzavřených kontur, vrací obvod kontury
    perimeter = cv2.arcLength(contour,True)
    for i in range(5):
        # Zjednodušení kontury
        contour_approx = cv2.approxPolyDP(contour, 5*0.01*perimeter, True)
        # Pokud se povedlo zjednodušit konturu na čtyřúhelník
        if len(contour_approx) == 4:
            # Zjištění obsahu plochy, který ohraničuje kontura
            area = cv2.contourArea(contour_approx)
            # Pokud je obsah plochy kontury větší, než 15% plochy obrázku
            if area > 0.15*(np.size(grid, 0)*np.size(grid, 1)):
                help_list.append(area)
                max_countour=contour_approx



# Draw all contours
vis = np.zeros((height, width, 3), np.uint8)
cv2.drawContours(vis, contours, -1, (128,255,255), thickness=cv2.FILLED)

cv2.waitKey()
# plt.imshow(grid,'gray')
plt.imshow(vis,'gray')
plt.show()

