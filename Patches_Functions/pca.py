import numpy as np


def pca(style_patches):
    mean_patch = np.mean(style_patches, axis=0)
    centered_patches = style_patches - mean_patch
    cov_mat = np.cov(centered_patches)
    eig_vals, eig_vecs = np.linalg.eig(cov_mat)
    sorted_eig_vals = np.argsort(eig_vals)[::-1]
    sorted_eig_vecs = eig_vecs[:, sorted_eig_vals]
    cumulative_variance = np.cumsum(eig_vals[sorted_eig_vals]) / np.sum(eig_vals[sorted_eig_vals])
    num_components = np.argmax(cumulative_variance >= 0.95) + 1
    k_eig_vecs = sorted_eig_vecs[:, :num_components]
    proj_mat = k_eig_vecs
    pca_data = np.dot(centered_patches, proj_mat)
    return proj_mat, pca_data
