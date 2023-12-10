from patchify import patchify


def extract_patches(img, patch_size, sub_sampling_gaps):
    patches = patchify(img, patch_size, sub_sampling_gaps)
    return patches
