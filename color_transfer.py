import numpy as np
import cv2

def color_transfer(content,style):
    content=cv2.cvtColor(content, cv2.COLOR_BGR2LAB).astype("float32")
    style=cv2.cvtColor(style, cv2.COLOR_BGR2LAB).astype("float32")
    content[:,:,0]-=np.mean(content[:,:,0])
    content[:,:,1]-=np.mean(content[:,:,1])
    content[:,:,2]-=np.mean(content[:,:,2])
    content[:,:,0]*=(np.std(content[:,:,0])/np.std(style[:,:,0]))
    content[:,:,1]*=(np.std(content[:,:,1]/np.std(style[:,:,1])))
    content[:,:,2]*=(np.std(content[:,:,2]/np.std(style[:,:,2])))
    content[:,:,0]+=np.mean(style[:,:,0])
    content[:,:,1]+=np.mean(style[:,:,1])
    content[:,:,2]+=np.mean(style[:,:,2])
    content=np.clip(content,0,255)
    return cv2.cvtColor(content.astype(np.float32), cv2.COLOR_LAB2BGR)
# def color_transfer(content, style):
#     transfered = np.copy(content)
#     # for each channel of the content, match the cum_histogram with the style's one
#     for i in range(0, content.shape[2]):
#         content_channel = content[:, :, i].flatten()
#         style_channel = style[:, :, i].flatten()
#         # calculate histogram for both content and style
#         content_values, content_indices, content_counts = np.unique(content_channel, return_inverse=True, return_counts=True)
#         style_values, style_counts = np.unique(style_channel, return_counts=True)
#         # calculate cummulative histogram
#         content_cumhist = np.cumsum(content_counts)
#         style_cumhist = np.cumsum(style_counts)
#         # normalize it
#         content_cumhist = content_cumhist / np.max(content_cumhist)
#         style_cumhist = style_cumhist / np.max(style_cumhist)
#         # match using interpolation
#         matched = np.interp(content_cumhist, style_cumhist, style_values)
#         transfered[:, :, i] = matched[content_indices].reshape(content[:, :, i].shape)
#     return transfered
