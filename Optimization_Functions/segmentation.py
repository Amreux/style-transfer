import cv2
import numpy as np
from Common_Functions.CommonFunctions import *


def segement(image):

    mask = np.zeros(image.shape[:2], np.uint8)
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)

    img_height=image.shape[0]
    img_width= image.shape[1]
    rectangle = (1,1,img_width,img_height)

    cv2.grabCut(image, mask, rectangle, backgroundModel, foregroundModel, 10, cv2.GC_INIT_WITH_RECT)

    mask_forground = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
    result_img = image * mask_forground[:, :, np.newaxis]
    result_mask = np.where((result_img>0),1,0).astype(float)
    # print(result_mask.shape)
    return result_mask

def region_filling (image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
    se=np.ones((7,7),np.uint8)
    # se2=np.ones((3,3),np.uint8)
    # can = canny(gray, low_threshold=20, high_threshold=180).astype(int)*244

    can=cv2.Canny(gray,10,100)
    # can1=cv2.erode(can,se2,iterations=1)
    can2=cv2.dilate(can,se,iterations=3)
    can3=cv2.erode(can2,se,iterations=3)

    # print(np.max(can))
    # show_images([can, can2, can3])
    # create binary image
    # can = np.where((can>0),1,0).astype(float)
    # cnts = find_contours(can, 0.8)
    cnts, hierarchy = cv2.findContours(can3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        cv2.drawContours(can,[c], -1, color=(255, 255, 255), thickness=cv2.FILLED)
    # print(cnts)
    # show_images([can])
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20,20))
    opening = cv2.morphologyEx(can, cv2.MORPH_OPEN, kernel, iterations=2)
    # Common_Functions.show_images([opening])
    # print(can.shape, opening.shape)
    # convet

    can = np.stack((can,)*3, axis=-1)
    opening = np.stack((opening,)*3, axis=-1)

    can = can.astype(np.float32)*0.7/255.0
    print(np.max(can))

    # convert to float and set 1
    return can, opening

# watershed
def watershed (image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
    se=np.ones((12,12),np.uint8)
    se2=np.ones((3,3),np.uint8)
    image=image.astype(np.uint8)
    # show_images([image])
    # can = canny(gray, low_threshold=20, high_threshold=180).astype(int)*244
    print(image.shape)
    can=cv2.Canny(gray,80,100).astype(np.uint8)
    can1=cv2.erode(can,se2,iterations=1)
    can2=cv2.dilate(can,se,iterations=3)
    can3=cv2.erode(can2,se,iterations=3)
    can4=cv2.erode(can2,se,iterations=2)
    dist_can2=cv2.distanceTransform(can4,cv2.DIST_L2,5)
    ret,sure_fg=cv2.threshold(dist_can2,0.3 * dist_can2.max(), 255, cv2.THRESH_BINARY)
    sure_bg=can2.astype(np.float32)
    unknown = cv2.subtract(sure_bg, sure_fg)
    # show_images([dist_can2,sure_fg])
    # show_images([sure_bg,unknown])
    sure_bg=sure_bg.astype( np.uint8)
    sure_fg=sure_fg.astype( np.uint8)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers += 1
    markers[unknown == 255] = 0
    # show_images([markers])
    markers = cv2.watershed(image, markers)
    # show_images([markers])

    # create binary image
    # can = np.where((can>0),1,0).astype(float)
    # cnts = find_contours(can, 0.8)
    cnts, hierarchy = cv2.findContours(can3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        cv2.drawContours(can,[c], -1, color=(255, 255, 255), thickness=cv2.FILLED)
    print(cnts)
    # show_images([can])
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20,20))
    opening = cv2.morphologyEx(can, cv2.MORPH_OPEN, kernel, iterations=2)
    # show_images([opening])
    #show_images([can, opening])

def ghaith (image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)

    # pixel_vals=image.reshape((-1,3))
    # pixel_vals = np.float32(pixel_vals)



    can=cv2.Canny(gray,20,60)
    show_images([can])

    # can=cv2.dilate(can,np.ones((1,1),np.uint8),iterations=3)
    # show_images([can])

    cnts, hierarchy = cv2.findContours(can, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        cv2.drawContours(can,[c], -1, color=(255, 255, 255), thickness=10)
    show_images([can])
    for i in range(2):
        cnts, hierarchy = cv2.findContours(can, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cnts, hierarchy = cv2.findContours(can, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            cv2.drawContours(can,[c], -1, color=(255, 255, 255), thickness=cv2.FILLED)
    show_images([can])
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    can = cv2.morphologyEx(can, cv2.MORPH_OPEN, kernel, iterations=2)
    # apply erosion
    show_images([can])
    can=cv2.erode(can,np.ones((5,5),np.uint8),iterations=3)
    show_images([can])

    can = np.stack((can.astype(np.float32)*0.6/255.0,)*3, axis=-1)

    return can