from patchify import patchify
import numpy as np


def irls(X,z,r,Iirls,patch_size,subsampling_gap):
    Xp=patchify(X,patch_size,subsampling_gap)
    num_of_patches=(np.shape(Xp)[0])*(np.shape(Xp)[1])
    w=(np.ones((num_of_patches,1)))
    # z should be initialized with patch matching
    # print(num_of_patches)
    for i in range(0, Iirls):
        for x in range(0, np.shape(Xp)[0]):
            for y in range(0,np.shape(Xp)[1]):
                e=Xp[x,y,0,:,:,:]-z[x*np.shape(Xp)[1]+y]
                e2=np.sum(e**2)**0.5+0.00001
                w[x*np.shape(Xp)[1]+y]=(e2**(r-2))
                Xp[x,y,0,:,:,:]+=(z[x*np.shape(Xp)[1]+y]-Xp[x,y,0,:,:,:])*w[x*np.shape(Xp)[1]+y]
                overlap=patch_size[0]-subsampling_gap
                avgx=np.copy(Xp[x,y,0,:overlap,:,:])
                avgy=np.copy(Xp[x,y,0,:,:overlap,:])
                if(x>0 and overlap>0):
                    avgx+=Xp[x-1,y,0,-overlap:,:,:]
                    avgx/=2.0
                if(y>0 and overlap>0):
                    avgy+=Xp[x,y-1,0,:,-overlap:,:]
                    avgy/=2.0
                Xp[x,y,0,:overlap,:,:]=avgx
                Xp[x,y,0,:,:overlap,:]=avgy
