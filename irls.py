from patchify import patchify
import numpy as np
#%%


def irls(X,z,r,Iirls,patch_size,subsampling_gap):
    Xp=patchify(X,patch_size,subsampling_gap)
    num_of_patches=(np.shape(Xp)[0]+1)*(np.shape(Xp)[1]+1)
    w=(np.ones((num_of_patches,1)))
    # z should be initialized with patch matching
    for i in range(0, Iirls):
        for x in range(0, np.shape(Xp)[0]):
            for y in range(0,np.shape(Xp)[1]):
                e=Xp[x,y,0,:,:,:]-z[x,y,0,:,:,:]
                e2=np.sum(e**2)**0.5+0.00001
                w[x*np.shape(Xp)[0]+y]=(e2**(r-2))
                Xp[x,y,0,:,:,:]+=(z[x,y,0,:,:,:]-Xp[x,y,0,:,:,:])*w[x*np.shape(Xp)[0]+y]