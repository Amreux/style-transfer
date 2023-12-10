from Patches_Functions.pca import pca
from sklearn.neighbors import NearestNeighbors


# This function is used to fit a KNN model to the style patches, and it returns the model
def fit_nn(style_patches):
    _, pca_style_patches = pca(style_patches)
    nn = NearestNeighbors(n_neighbors=1).fit(style_patches)
    return nn

samples = [[10, 10, 12], [12,10, 10], [0, 0, 1]]
nn = fit_nn(samples)
print(nn.kneighbors([[7.5, 10, 10]])) # euclidean

print(samples[nn.kneighbors([[9, 10, 12]])[1][0][0]], nn.kneighbors([[9, 10, 12]])[0][0][0])

