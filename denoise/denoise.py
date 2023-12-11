import cv2 
import skimage.io as io
import matplotlib.pyplot as plot
import numpy as np


def denoise(img,d,sigma_s,sigma_c):

    img = io.imread("image.png") 
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
    bilateral = cv2.bilateralFilter(img, d, sigmaColor=sigma_c, sigmaSpace=sigma_s) 
    return bilateral