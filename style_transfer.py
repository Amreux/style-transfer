from patchify import patchify
from Common_Functions.CommonFunctions import *
from sklearn.neighbors import NearestNeighbors
# from color_transfer import color_transfer
# from segmentation.FaceDetectionSegmentation import segement
import cv2
from skimage.transform import pyramid_gaussian
import imageio.v3 as iio
from Optimization_Functions.pca import pca
from Optimization_Functions.irls import irls
import Optimization_Functions.PatchMatching as pm
import Optimization_Functions.segmentation as seg
import color_transfer as ct

import importlib
importlib.reload(pm)
importlib.reload(seg)
importlib.reload(ct)

def style_transfer(content, style, r, L, Iirls, patch_sizes, subsampling_gaps, Ialg,color_transfer_type='histogram', segmentation_type = 'edge', seg_mask_weight = 0.8):
    # apply segmentation to the content
    # segmentation_type -> 'edge' applies edge segmentation
    # segmentation_type -> 'GrabCut' applies face segmentation
    con = content.copy()
    con = (con*255).astype(np.uint8)
    seg_mask = seg.segment(con, segmentation_type, seg_mask_weight)
    # show_images([seg_mask],["seg_mask"])

    # apply color_transfer from the style to the content
    # color_transfer_type -> 'histogram' applies match_histograms color transfer
    # color_transfer_type -> 'lab' applies lab color transfer
    # lab color transfer is better for less colorful images
    # show_images([content],["content"])
    content = ct.color_transfer(content,style, color_transfer_type)

    # build gaussian pyramids
    content_pyramid_tuple = tuple(pyramid_gaussian(content, channel_axis=-1, max_layer=L, downscale=2))
    style_pyramid_tuple = tuple(pyramid_gaussian(style, channel_axis=-1, max_layer=L, downscale=2))
    w_pyramid_tuple = tuple(pyramid_gaussian(seg_mask, channel_axis=-1, max_layer=L, downscale=2))
    content_pyramid = []
    style_pyramid = []
    w_pyramid = []
    for i in range (0,L):
        content_pyramid.append(content_pyramid_tuple[i])
        style_pyramid.append(style_pyramid_tuple[i])
        w_pyramid.append(w_pyramid_tuple[i])

    X = np.copy(content_pyramid[L-1])
    X = np.pad(X, ((0, patch_sizes[0]), (0, patch_sizes[0]), (0, 0)), mode='reflect')
    resized_style = cv2.resize(style, (np.shape(X)[1],np.shape(X)[0]))

    # apply the style to the padding
    X[-patch_sizes[0]:np.shape(X)[0], :, :] = resized_style[-patch_sizes[0]:np.shape(X)[0], :, :]
    X[:-patch_sizes[0], -patch_sizes[0]:, :] = resized_style[:-patch_sizes[0], -patch_sizes[0]:, :]

    for l in range (L-1,-1,-1):
        if l == L-1:
            X= random_noise(X, mode="gaussian",mean=0,var=50)
        else:
            X= random_noise(X, mode="gaussian",mean=0,var=0.01)
        content_pyramid[l] = np.pad(content_pyramid[l], ((0, patch_sizes[0]), (0, patch_sizes[0]), (0,0)), mode='constant', constant_values=(0,0))
        w_pyramid[l] = np.pad(w_pyramid[l], ((0, patch_sizes[0]), (0, patch_sizes[0]), (0, 0)), mode='constant', constant_values=(0,0))
        for s in range(0,len(patch_sizes)):
            style_patches =  patchify(style_pyramid[l],(patch_sizes[s], patch_sizes[s], 3),subsampling_gaps[s])
            flatten_style_patches = style_patches.reshape(-1, patch_sizes[s] * patch_sizes[s] * 3)
            projection_matrix = []

            # apply pca if the patch size is less than 17
            if (patch_sizes[s]<17):
                pca_flatten_style_patches, projection_matrix = pca(flatten_style_patches)
                # train the nearest neighbour model
                nn_model = NearestNeighbors(n_neighbors=2).fit(pca_flatten_style_patches)
            else:
                nn_model = NearestNeighbors(n_neighbors=2).fit(flatten_style_patches)

            for k in range(0,Ialg):
                # z is the matched style patches
                z=[]
                Xp=patchify(X,(patch_sizes[s], patch_sizes[s], 3),subsampling_gaps[s])
                flatten_Xp = Xp.reshape(-1, patch_sizes[s] * patch_sizes[s] * 3)

                # apply pca if the patch size is less than 17 using the projection matrix from the style patches
                if(patch_sizes[s]<17):
                    flatten_Xp = flatten_Xp - np.mean(flatten_Xp)
                    flatten_Xp = np.matmul(flatten_Xp, projection_matrix.T)

                # Patch Matching
                z = pm.patch_matching (flatten_Xp, patch_sizes[s], subsampling_gaps[s], flatten_style_patches, nn_model, Xp.shape)
                # Robust Aggregation
                irls(X,z,r,Iirls,(patch_sizes[s],patch_sizes[s],3),subsampling_gaps[s])
                # Color Transfer
                X = ct.color_transfer(X,style,color_transfer_type)
                # Content Fusion
                X =((1.0-w_pyramid[l])* X).astype(np.float32) + ((w_pyramid[l].astype(np.float32))*content_pyramid[l]).astype(np.float32)
                # Denoise
                X = cv2.bilateralFilter(X, 1, sigmaColor=5, sigmaSpace=10)

                # show_images([X])
        if l>0:
            padding_down=cv2.resize(X[-patch_sizes[0]:np.shape(X)[0], :, :], (np.shape(content_pyramid[l-1])[1]+patch_sizes[0], patch_sizes[0]))
            padding_right = cv2.resize(X[:-patch_sizes[0], -patch_sizes[0]:, :], (patch_sizes[0], np.shape(content_pyramid[l-1])[0]))

            # remove the padding
            X = X[0:-patch_sizes[0], 0:-patch_sizes[0], :]
            # resize the image to the size of the next content layer
            X = cv2.resize(X, (np.shape(content_pyramid[l-1])[1], np.shape(content_pyramid[l-1])[0]))
            # add the padding to the resized image
            X = np.pad(X, ((0, patch_sizes[0]), (0, patch_sizes[0]), (0, 0)), mode='constant', constant_values=(1,1))
            # add the previous padding to the resized image
            X[-patch_sizes[0]:np.shape(X)[0], :, :] = padding_down
            X[:-patch_sizes[0], -patch_sizes[0]:, :] = padding_right
    return X
