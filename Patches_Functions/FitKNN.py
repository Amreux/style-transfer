from pca import*


# This function is used to fit a KNN model to the style patches, and it returns the model
def fit_nn(style_patches):
    _, pca_style_patches = pca(style_patches)
    nn = NearestNeighbors(n_neighbors=1).fit(pca_style_patches)
    return nn
