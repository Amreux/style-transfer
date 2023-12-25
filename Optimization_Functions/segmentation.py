import cv2
import numpy as np
from Common_Functions.CommonFunctions import *


def grab_cut(image, seg_mask_weight):
    mask = np.zeros(image.shape[:2], np.uint8)
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)
    img_height=image.shape[0]
    img_width= image.shape[1]
    rectangle = (1,1,img_width,img_height)
    cv2.grabCut(image, mask, rectangle, backgroundModel, foregroundModel, 10, cv2.GC_INIT_WITH_RECT)
    mask_forground = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
    result_img = image * mask_forground[:, :, np.newaxis]
    result_mask = np.where((result_img>0),seg_mask_weight,0).astype(float)
    return result_mask


def watershed (image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
    se=np.ones((12,12),np.uint8)
    can=cv2.Canny(gray,80,100).astype(np.uint8)
    can2=cv2.dilate(can,se,iterations=3)
    can3=cv2.erode(can2,se,iterations=3)
    can4=cv2.erode(can2,se,iterations=2)
    dist_can2=cv2.distanceTransform(can4,cv2.DIST_L2,5)
    ret,sure_fg=cv2.threshold(dist_can2,0.3 * dist_can2.max(), 255, cv2.THRESH_BINARY)
    sure_bg=can2.astype(np.float32)
    unknown = cv2.subtract(sure_bg, sure_fg)
    sure_fg=sure_fg.astype( np.uint8)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers += 1
    markers[unknown == 255] = 0
    cnts, hierarchy = cv2.findContours(can3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        cv2.drawContours(can,[c], -1, color=(255, 255, 255), thickness=cv2.FILLED)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20,20))
    opening = cv2.morphologyEx(can, cv2.MORPH_OPEN, kernel, iterations=2)
    return opening


def edge_segmentation (image, seg_mask_weight):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
    can=cv2.Canny(gray,20,60)
    cnts, hierarchy = cv2.findContours(can, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        cv2.drawContours(can,[c], -1, color=(255, 255, 255), thickness=10)
    for i in range(2):
        cnts, hierarchy = cv2.findContours(can, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            cv2.drawContours(can,[c], -1, color=(255, 255, 255), thickness=cv2.FILLED)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    can = cv2.morphologyEx(can, cv2.MORPH_OPEN, kernel, iterations=2)
    can=cv2.erode(can,np.ones((5,5),np.uint8),iterations=3)
    can = np.stack((can.astype(np.float32)*seg_mask_weight/255.0,)*3, axis=-1)
    return can


def segment (image, method, seg_mask_weight):
    if method == 'grabcut':
        return grab_cut(image, seg_mask_weight)
    elif method == 'watershed':
        return watershed(image)
    else:
        return edge_segmentation(image, seg_mask_weight)
