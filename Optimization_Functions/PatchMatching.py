def patch_matching (flatten_Xp, patch_size, subsampling_gap, flatten_style_patches, nn_model, xp_shape):
    z = []
    sc = 0
    for Xpatch in flatten_Xp:
        flatten_Xpp = [Xpatch]

        if patch_size>=17 :
            unflattened_Xp=Xpatch.reshape(patch_size, patch_size, 3)
            if(sc%xp_shape[0]):
                unflattened_Xp[:,:patch_size-subsampling_gap,:]=z[sc-1][:,-(patch_size-subsampling_gap):,:]
            if(sc>=xp_shape[1]):
                unflattened_Xp[:patch_size-subsampling_gap,:,:]=z[sc-xp_shape[1]][-(patch_size-subsampling_gap):,:,:]
            flatten_Xpp = unflattened_Xp.reshape(-1, patch_size * patch_size * 3)
            sc+=1

        flatten_neighbour_patch = flatten_style_patches[nn_model.kneighbors(flatten_Xpp)[1][0][0]]
        z.append(flatten_neighbour_patch.reshape(patch_size, patch_size, 3))
    return z
