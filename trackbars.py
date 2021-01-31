import cv2
import numpy as np
#TRACKBAR function, does nothing, but the create trackbar function requires it
def nothing(x):
    pass

#the main function, which draws the trackbars and displays the result after changing the trackbar's values
def trackbar(img,tb,operation):
    #name of the window
    cv2.namedWindow(operation)
    #creating as many trackbars as many were given in the argument
    for i in range(tb.shape[0]):
        cv2.createTrackbar(tb[i][0], operation, tb[i][1], tb[i][2], nothing)

    #matrix to store trackbar values
    positions = np.zeros((tb.shape[0]), dtype=np.uint8)

#MAIN PART FOR DECIDING WHICH PART OF CODE IS CALLED

    #canny edge detector with 2 trackbars
    if operation == 'canny':
        while True:
            cv2.imshow(operation, cv2.Canny(img, positions[0], positions[1]))
            for i in range(tb.shape[0]):
                positions[i] = cv2.getTrackbarPos(tb[i][0], operation)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyWindow(operation)
                break

    #morphological closing with kernel size only
    if operation == 'close':
        position=5
        while True:
            M = cv2.getStructuringElement(cv2.MORPH_CROSS, (position,position))
            cv2.imshow(operation, cv2.morphologyEx(img, cv2.MORPH_CLOSE, M))
            position= cv2.getTrackbarPos(tb[i][0], operation)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyWindow(operation)
                break

    #connected component - going for 1st larges - smallest
    #most unstable (as not every time is know how many CCs they are and the trackbar limits are passed as arguments
    if operation == 'connectedComp':
        stats = cv2.connectedComponentsWithStats(img)
        indx = np.argsort(stats[2][:, -1])[::-1]
        sorted = stats[2][indx]
        position=0
        while True:
            grid = np.zeros(img.shape, dtype=np.uint8)
            grid[stats[1] == indx[position]] = 255
            cv2.imshow(operation, grid)
            positions = cv2.getTrackbarPos(tb[i][0], operation)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyWindow(operation)
                break