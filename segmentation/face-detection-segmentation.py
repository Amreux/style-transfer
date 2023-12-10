import numpy as np 
import cv2 
from matplotlib import pyplot as plt 


def segement(image):


    # initialize the mask
    mask = np.ones(image.shape[:2], np.uint8)

    # not sure what these are for in the algorithm
    backgroundModel = np.zeros((1, 65), np.float64) 
    foregroundModel = np.zeros((1, 65), np.float64) 


    # this is to initialize a rectangular mask to capture the core of the image
    div=12
    img_height=image.shape[0]
    img_width= image.shape[1]
    img_height_div=img_height//div
    img_width_div=img_width//div
    rectangle = (0,img_height_div,10*img_height_div,10*img_width_div)

    # run the grabcut algorithm for 2 iterations
    cv2.grabCut(image, mask, rectangle, backgroundModel, foregroundModel, 5, cv2.GC_INIT_WITH_RECT) 
    # cv2.grabCut(image, mask, rectangle, backgroundModel, foregroundModel, 2, cv2.GC_INIT_WITH_MASK) 

    # generate the forground mask
    mask_forground = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8') 

    # get the final image
    result_img = image * mask_forground[:, :, np.newaxis] 

    return result_img




