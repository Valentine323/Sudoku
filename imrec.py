import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import trackbars as tb

file_names=os.listdir(os.getcwd()+'\Pictures')#path to the folder where the puzzles are stored
base_path = lambda bp: os.getcwd()+'\Pictures'+'\\'+bp
paths=np.array([base_path(p) for p in file_names])

#coefficients to resize the image
resize_coeff_h=0.25
resize_coeff_w=0.5
#passing it to tupple
resize_coeff_vec=np.array([resize_coeff_w,resize_coeff_h])

# for path in paths:
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
#median "blur" in order to remove noise (7x7 kernel) #not needed, just damages the results
# median = cv2.medianBlur(tresh, 7)
#performing morphological closure to connect fractured lines (11x11 kernel) #not needed, just damages the results
# closed = cv2.morphologyEx(tresh, cv2.MORPH_CLOSE, (11, 11))
#get the stats of connected components
stats = cv2.connectedComponentsWithStats(tresh)
#sort the pixel count of the different connected components
indx = np.argsort(stats[2][:, -1])[::-1]
#sort the whole stats matrix with the pixel count
sorted = stats[2][indx]
#create an empty image
grid = np.zeros(tresh.shape, dtype=np.uint8)
#set pixel values to white, where the largest connected component was located (1st entry is white - 0th is the background)
grid[stats[1] == indx[1]] = 255

#Canny trackbar
# tb.trackbar(resized,np.array([['low',0,255],['high',0,255]],dtype=object),'canny')
#ConnComp trackbar
# tb.trackbar(canny,np.array([['no.',0,100]],dtype=object),'connectedComp')
#Closing trackbar
# tb.trackbar(canny,np.array([['close',3,30]],dtype=object),'close')

#canny edge detection with optimal parameters found by trackbars
canny=cv2.Canny(resized,50,150)

#displaing some results:original image, image after canny, largest component, contours
# _,sub=plt.subplots(1,4)
# sub[0].imshow(cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
# sub[1].imshow(canny,cmap=plt.cm.gray)
# sub[2].imshow(grid,cmap=plt.cm.gray)

#finding all the contours in the canny image (looks more stable)
canny=cv2.morphologyEx(canny,cv2.MORPH_CLOSE,(3,3))
contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
con= np.zeros((tresh.shape[0],tresh.shape[1],3), dtype=np.uint8)
#draw all contours to the image
cv2.drawContours(con, contours, -1, (0, 255, 0), 3)
#show the drawn contours
# sub[3].imshow(con,cmap=plt.cm.gray)
# plt.show()
# plt.imshow(con)
# plt.show()

#largest contour by arrea
largest_cnt= max(contours, key = cv2.contourArea)
#perimeter of the largest contour
perimeter = cv2.arcLength(largest_cnt,True)

#create and image to draw the contour to
largest= np.zeros((tresh.shape[0],tresh.shape[1],3), dtype=np.uint8)
cv2.drawContours(largest, largest_cnt, -1, (0, 255, 0), 3)
#BB of largest contour
c,r,w,h = cv2.boundingRect(largest_cnt)
#BB of largest element
NoN_zero_points=cv2.findNonZero(grid)
c2,r2,w2,h2=cv2.boundingRect(NoN_zero_points)

#displaying result
_,subplt=plt.subplots(1,2)
cv2.rectangle(largest,(c,r),(c+w,r+h),(0,0,255),2)
subplt[0].imshow(largest)
part=tresh[c:c+h,r:r+w]
grid_rgb=np.zeros((grid.shape[0],grid.shape[1],3),dtype=np.uint8)
grid_rgb[:,:,1]=grid
cv2.rectangle(grid_rgb,(c2,r2),(c2+w2,r2+h2),(0,0,255),2)
subplt[1].imshow(grid_rgb)
plt.show()

#drawing the BBs to binary images to easier calculate the IoU
bb_cc=np.zeros(grid.shape,dtype=np.bool)
bb_cc[r2:r2+h2,c2:c2+w2]=True
bb_cont=np.zeros(grid.shape,dtype=np.bool)
bb_cont[r:r+h,c:c+w]=True
uni=bb_cc|bb_cont.astype(np.uint8)
inter=bb_cc&bb_cont.astype(np.uint8)

#getting the IoU
bb_uni=cv2.countNonZero(uni)
bb_inter=cv2.countNonZero(inter)
bb_inter=cv2.countNonZero(inter)
IoU=bb_inter/bb_uni

#arreas of the BBs
bb_cont_area=h*w
bb_cc_area=h2*w2

#storing the areas into additional variables (smaller, larger)
if bb_cont_area>bb_cc_area:
    larger_bb=np.array([c,r,w,h])
    smaller_bb = np.array([c2,r2,w2,h2])
else:
    larger_bb = np.array([c2,r2,w2,h2])
    smaller_bb = np.array([c,r,w,h])

#vector for storing values of the puzzles BB
puzzle_bb=np.zeros(4)
#deciding which BB is better - works quite well
if IoU>0.8:#if the overlap is larger than 80%, get the larger
    puzzle_bb[:2]=larger_bb[:2]#/resize_coeff_vec
    puzzle_bb[2:]=larger_bb[2:]#/resize_coeff_vec
    puzzle_bb_small=larger_bb
    print('Larger 1')
elif larger_bb[2]*larger_bb[3]-smaller_bb[2]*smaller_bb[3]>0.5*larger_bb[2]*larger_bb[3]:#if the smaller is a lot smaller, than get the larger
    puzzle_bb[:2]=larger_bb[:2]#/resize_coeff_vec
    puzzle_bb[2:]=larger_bb[2:]#/resize_coeff_vec
    puzzle_bb_small = larger_bb
    print('Larger 2')
elif puzzle_bb[0]+larger_bb[2]==tresh.shape[1] or larger_bb[1]+larger_bb[3]==tresh.shape[0] or puzzle_bb[0]==0 or puzzle_bb[1]:#if the larger would be too large (touches the edge of the image), get the smaller
    puzzle_bb[:2]=smaller_bb[:2]#/resize_coeff_vec
    puzzle_bb[2:]=smaller_bb[2:]#/resize_coeff_vec
    puzzle_bb_small = smaller_bb
    print('Smaller')
else:#if none is true, just say, taht there is no puzzle in the picture
    print('NO PUZZLE FOUND')

#unwrap the bounding box's values to c,r,w,h
pc,pr,pw,ph=puzzle_bb.astype(int)
#cut out the BB area from the original image
puzzle_cut=img[pr:pr+ph,pc:pc+pw]
puzzle_cut_small=resized[puzzle_bb_small[1]:puzzle_bb_small[1]+puzzle_bb_small[-1],puzzle_bb_small[0]:puzzle_bb_small[0]+puzzle_bb_small[-2]]
#display the result




#AdaptiveTresh trackbar
# tb.trackbar(puzzle_cut_small,np.array([['kernel',3,17],['minus',0,20]],dtype=object),'tresh')
# #Gaussian blurr trackbar
# tb.trackbar(puzzle_cut_small,np.array([['kernel',3,17],['sigma',0,20]],dtype=object),'gaussBlurr')
#
# plt.imshow(puzzle_cut_small,cmap='Greys')
# plt.show()


#start to unwarp the puzzle
puzzle_blurred = cv2.GaussianBlur(puzzle_cut_small, (11, 11), 1)
# puzzle_bin=cv2.Canny(puzzle_blurred,50,150)
puzzle_bin=cv2.adaptiveThreshold(puzzle_blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,3)
puzzle_stats = cv2.connectedComponentsWithStats(puzzle_bin)

indx = np.argsort(puzzle_stats[2][:, -1])[::-1]
#sort the whole stats matrix with the pixel count
sorted = puzzle_stats[2][indx]
#create an empty image
puzzle_grid = np.zeros((puzzle_bb_small[3],puzzle_bb_small[2],3), dtype=np.uint8)
#find contours in the binary image
contours, _= cv2.findContours(puzzle_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
largest=0
for contour in contours:
    epsilon = 0.1 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    if len(approx) == 4:
        area=cv2.contourArea(contour)
        c=contour
        print('puzzle found')
        break

#set pixel values to white, where the largest connected component was located (1st entry is white - 0th is the background)
puzzle_grid[puzzle_stats[1] == indx[1],:] = 255
# cv2.drawContours(puzzle_grid, c, -1, (0,255,0), 3)
cv2.imshow('asd',puzzle_grid)
cv2.waitKey()





#OLD perspective removal for the whole puzzle: IT works quite well, if the whole puzzle is visible, and no distortions other than perspective are present
# #Get the 4 corners of the sudoku
# corners=np.reshape(max_contour,(4,2))
# TL=corners[(corners[:,0]+corners[:,1]).argmin(),:]
# TR=corners[(corners[:,0]-corners[:,1]).argmin(),:]
# BR=corners[(corners[:,0]+corners[:,1]).argmax(),:]
# BL=corners[(corners[:,0]-corners[:,1]).argmax(),:]
# #Calculate the position of the rows in the full-sized image
# TLx,TLy=(TL/resize_coeff_vec).astype(int)
# TRx,TRy=(TR/resize_coeff_vec).astype(int)
# BRx,BRy=(BR/resize_coeff_vec).astype(int)
# BLx,BLy=(BL/resize_coeff_vec).astype(int)



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
# moving_points=np.array([[TLx,TLy],[BLx,BLy],[BRx,BRy],[TRx,TRy]],np.float32)
# fixed_points=np.array([[0,0],[width,0],[width,width],[0,width]],np.float32)
# projection_mat=cv2.getPerspectiveTransform(moving_points,fixed_points)
# img_wop=cv2.warpPerspective(img, projection_mat, (width,width))


# #show the puzzle with removed persoectuve and the original image side-by-side
# _,sub=plt.subplots(1,2)
# sub[0].imshow(cv2.cvtColor(img_wop,cv2.COLOR_RGB2BGR))
# sub[1].imshow(cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
# # plt.imshow(gridBGR,'Greys')
# plt.show()
# cv2.waitKey()


