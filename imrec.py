import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import trackbars as tb

file_names=os.listdir(os.getcwd()+'\Pictures')#path to the folder where the puzzles are stored
base_path = lambda bp: os.getcwd()+'\Pictures'+'\\'+bp
paths=np.array([base_path(p) for p in file_names])

#coefficients to resize the image
resize_coeff_h=0.5
resize_coeff_w=0.5
#passing it to tupple
resize_coeff_vec=np.array([resize_coeff_h,resize_coeff_w])

#reading image
img = cv2.imread(paths[0], 0)
#getting the shape of the image
(height, width)=img.shape
#blurring the image with a 11x11 kernel gaussian filter with mean=1sigma
blurred = cv2.GaussianBlur(img, (11, 11), 1)
#resizing the image to a smaller size
resized = cv2.resize(blurred, (int(width*resize_coeff_w+0.5),int(height*resize_coeff_h+0.5)))
#treshold the image with adaptive treshold (again using an 11x11 kernel) + subtracting constant 3 (works quite well)
tresh = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)
#median "blur" in order to remove noise (7x7 kernel)
median = cv2.medianBlur(tresh, 7)
#performing morphological closure to connect fractured lines (11x11 kernel)
closed = cv2.morphologyEx(median, cv2.MORPH_CLOSE, (11, 11))
#get the stats of connected components
stats = cv2.connectedComponentsWithStats(closed)
#sort the pixel count of the different connected components
indx = np.argsort(stats[2][:, -1])[::-1]
#sort the whole stats matrix with the pixel count
sorted = stats[2][indx]
#create an empty image
grid = np.zeros(closed.shape, dtype=np.uint8)
#set pixel values to white, where the largest connected component was located (1st entry is white - 0th is the background)
grid[stats[1] == indx[1]] = 255


#Canny trackbar
# tb.trackbar(resized,np.array([['low',0,255],['high',0,255]],dtype=object),'canny')
canny=cv2.Canny(resized,50,150)
#ConnComp trackbar
# tb.trackbar(canny,np.array([['no.',0,100]],dtype=object),'connectedComp')
#Closing trackbar
# tb.trackbar(canny,np.array([['close',3,30]],dtype=object),'close')

#displaing some results:original image, image after canny, largest component, contours
_,sub=plt.subplots(1,4)
sub[0].imshow(cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
sub[1].imshow(canny,cmap=plt.cm.gray)
sub[2].imshow(grid,cmap=plt.cm.gray)

#finding all the contours in the canny image (looks more stable)
contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
con= np.zeros((closed.shape[0],closed.shape[1],3), dtype=np.uint8)
#draw all contours to the image
cv2.drawContours(con, contours, -1, (0, 255, 0), 3)
#show the drawn contours
sub[3].imshow(con,cmap=plt.cm.gray)
plt.show()
help_list = []
max_contour=[]
#constant for testing different tresholds for line fitting
epsilon=[1,2,3,4,5]
area_max=0
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
                # Pokud je obsah plochy kontury větší, než 20% plochy obrázku
                if area > 0.2*(np.size(grid, 0)*np.size(grid, 1)):
                    help_list.append(area)
                    max_contour=contour_approx
                # if area>area_max:
                #     area_max=area
                #     max_contour=contour_approx

#Get the 4 corners of the sudoku
corners=np.reshape(max_contour,(1,2))
TL=corners[(corners[:,0]+corners[:,1]).argmin(),:]
TR=corners[(corners[:,0]-corners[:,1]).argmin(),:]
BR=corners[(corners[:,0]+corners[:,1]).argmax(),:]
BL=corners[(corners[:,0]-corners[:,1]).argmax(),:]
#Calculate the position of the rows in the full-sized image
TLx,TLy=(TL/resize_coeff_vec).astype(int)
TRx,TRy=(TR/resize_coeff_vec).astype(int)
BRx,BRy=(BR/resize_coeff_vec).astype(int)
BLx,BLy=(BL/resize_coeff_vec).astype(int)



# Draw the cornerpoints to the original image
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

#Remove perspective view from the whole puzzle
moving_points=np.array([[TLx,TLy],[BLx,BLy],[BRx,BRy],[TRx,TRy]],np.float32)
fixed_points=np.array([[0,0],[width,0],[width,width],[0,width]],np.float32)
projection_mat=cv2.getPerspectiveTransform(moving_points,fixed_points)
img_wop=cv2.warpPerspective(img, projection_mat, (width,width))


#show the puzzle with removed persoectuve and the original image side-by-side
_,sub=plt.subplots(1,2)
sub[0].imshow(cv2.cvtColor(img_wop,cv2.COLOR_RGB2BGR))
sub[1].imshow(cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
# plt.imshow(gridBGR,'gray')
plt.show()
cv2.waitKey()


