import numpy as np
import cv2
from skimage.exposure import match_histograms
import skimage.io as io

def color_transfer(content,style, type):
    if type == 'histogram':
        return match_histograms(content,style, channel_axis=-1)

    else:
        content=cv2.cvtColor(content.astype(np.float32), cv2.COLOR_BGR2LAB)
        style=cv2.cvtColor(style, cv2.COLOR_BGR2LAB)
        content[:,:,0] -=np.mean(content[:,:,0])
        content[:,:,1] -=np.mean(content[:,:,1])
        content[:,:,2] -=np.mean(content[:,:,2])
        content[:,:,0] *=(np.std(style[:,:,0])/(np.std(content[:,:,0])+0.00001))
        content[:,:,1] *=(np.std(style[:,:,1]/(np.std(content[:,:,1])+0.00001)))
        content[:,:,2] *=(np.std(style[:,:,2]/(np.std(content[:,:,2])+0.00001)))
        content[:,:,0] +=np.mean(style[:,:,0])
        content[:, :, 1] +=np.mean(style[:,:,1])
        content[:, :, 2] +=np.mean(style[:,:,2])
        return cv2.cvtColor(content.astype(np.float32), cv2.COLOR_LAB2BGR)
