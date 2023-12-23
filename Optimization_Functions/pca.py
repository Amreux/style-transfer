import numpy as np
from sklearn.decomposition import PCA


def pca(style_patches):
    mean_patch = np.mean(style_patches, axis=0)
    centered_patches = style_patches - mean_patch
    cov_mat = np.cov(centered_patches.T)
    eig_vals, eig_vecs = np.linalg.eig(cov_mat)
    sorted_eig_vals = np.argsort(eig_vals)[::-1]
    sorted_eig_vecs = eig_vecs[:, sorted_eig_vals]
    cumulative_variance = np.cumsum(eig_vals[sorted_eig_vals]) / np.sum(eig_vals[sorted_eig_vals])
    num_components = np.argmax(cumulative_variance >= 0.95) + 1
    k_eig_vecs = sorted_eig_vecs[:, :num_components]
    ep = np.zeros((num_components, centered_patches.shape[1]))
    for i in range(num_components):
        ep[i] = k_eig_vecs[:, i].real
    pca_data = np.matmul(centered_patches, ep.T)
    return pca_data, ep
