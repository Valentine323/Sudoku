import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

#TRACKBAR
def nothing(x):
    pass

file_names=os.listdir(os.getcwd()+'\Pictures')#path to the folder where the puzzles are stored
base_path = lambda bp: os.getcwd()+'\Pictures'+'\\'+bp
paths=np.array([base_path(p) for p in file_names])
resize_coeff_h=0.5
resize_coeff_w=0.5
resize_coeff_vec=np.array([resize_coeff_h,resize_coeff_w])
img = cv2.imread(paths[5], 0)
print(img.shape)
(height, width)=img.shape
blurred = cv2.GaussianBlur(img, (11, 11), 1)
resized = cv2.resize(blurred, (int(width*resize_coeff_w+0.5),int(height*resize_coeff_h+0.5)))
print(resized.shape)
tresh = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)
median = cv2.medianBlur(tresh, 7)
closed = cv2.morphologyEx(median, cv2.MORPH_CLOSE, (11, 11))

stats = cv2.connectedComponentsWithStats(closed)
indx = np.argsort(stats[2][:, -1])[::-1]
sorted = stats[2][indx]
grid = np.zeros(closed.shape, dtype=np.uint8)
grid[stats[1] == indx[1]] = 255


#adding trackbar
win_name='canny'
cv2.namedWindow(win_name)
cv2.createTrackbar('low_tresh',win_name,0,255,nothing)
cv2.createTrackbar('high_tresh',win_name,0,255,nothing)
low=10
high=200
while True:
    cv2.imshow(win_name, cv2.Canny(resized,low,high))
    # get current positions of four trackbars
    low = cv2.getTrackbarPos('low_tresh',win_name)
    high = cv2.getTrackbarPos('high_tresh',win_name)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

(contours, _) = cv2.findContours(grid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
help_list = []
max_countour=[]
epsilon=[1,2,3,4,5]
for e in epsilon:
    for contour in contours:
        # Vypočtení obvodu uzavřených kontur, vrací obvod kontury
        perimeter = cv2.arcLength(contour,True)
        for i in range(5):
            # Zjednodušení kontury
            contour_approx = cv2.approxPolyDP(contour, e*0.01*perimeter, True)
            # Pokud se povedlo zjednodušit konturu na čtyřúhelník
            if len(contour_approx) == 4:
                # Zjištění obsahu plochy, který ohraničuje kontura
                area = cv2.contourArea(contour_approx)
                # Pokud je obsah plochy kontury větší, než 30% plochy obrázku
                if area > 0.3*(np.size(grid, 0)*np.size(grid, 1)):
                    help_list.append(area)
                    max_contour=contour_approx

#Get the 4 corners of the sudoku
corners=np.reshape(max_contour,(4,2))
TL=corners[(corners[:,0]+corners[:,1]).argmin(),:]
TR=corners[(corners[:,0]-corners[:,1]).argmin(),:]
BR=corners[(corners[:,0]+corners[:,1]).argmax(),:]
BL=corners[(corners[:,0]-corners[:,1]).argmax(),:]
#Calculate the position of the rows in the full-sized image
TLx,TLy=(TL/resize_coeff_vec).astype(int)
TRx,TRy=(TR/resize_coeff_vec).astype(int)
BRx,BRy=(BR/resize_coeff_vec).astype(int)
BLx,BLy=(BL/resize_coeff_vec).astype(int)



# Draw rows
# resized=cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
# font=cv2.FONT_HERSHEY_SIMPLEX
# # cv2.drawContours(img, [max_contour], -1, (0,255,0), thickness=cv2.FILLED)
# cv2.circle(img,(TLx,TLy),5,255,-1)
# cv2.putText(img,'TL',(TLx,TLy), font, 1,(0,255,0),2)
# cv2.circle(img,(TRx,TRy),5,255,-1)
# cv2.putText(img,'TR',(TRx,TRy), font, 1,(0,255,0),2)
# cv2.circle(img,(BRx,BRy),5,255,-1)
# cv2.putText(img,'BR',(BRx,BRy), font, 1,(0,255,0),2)
# cv2.circle(img,(BLx,BLy),5,255,-1)
# cv2.putText(img,'BL',(BLx,BLy), font, 1,(0,255,0),2)

#Remove perspective view
moving_points=np.array([[TLx,TLy],[BLx,BLy],[BRx,BRy],[TRx,TRy]],np.float32)
fixed_points=np.array([[0,0],[width,0],[width,width],[0,width]],np.float32)
projection_mat=cv2.getPerspectiveTransform(moving_points,fixed_points)
img_wop=cv2.warpPerspective(img, projection_mat, (width,width))

plt.imshow(cv2.cvtColor(img_wop,cv2.COLOR_RGB2BGR))
# plt.imshow(gridBGR,'gray')
plt.show()
cv2.waitKey()


