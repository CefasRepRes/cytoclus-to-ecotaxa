#!/usr/bin/env python3

import argparse
import numpy as np
import skimage
from skimage import io, filters, morphology, measure, color, feature
from scipy import ndimage
import pandas as pd
import matplotlib.pyplot as plt


def fast_particle_area(x):
    return np.sum(x._label_image[x._slice] == x.label)


def analyse(filename):
    im = io.imread(filename)

    # detect edges
    im_edges = filters.scharr(im)

    # identify the object
    # treshold edges
    edges_med = np.median(im_edges)
    edges_thresh = 3 * edges_med
    im_bin = im_edges >= edges_thresh
    # get a "nice" mask for the shape
    im_bin = morphology.binary_dilation(im_bin, morphology.disk(2))
    im_bin = morphology.binary_erosion(im_bin, morphology.disk(3))
    im_bin = ndimage.binary_fill_holes(im_bin)
    im_bin = morphology.binary_dilation(im_bin, morphology.disk(1))

    # label connected regions
    im_label = morphology.label(im_bin, connectivity=2, background=False)
    # and keep the largest one
    regions = skimage.measure.regionprops(label_image=im_label)
    if len(regions) > 0:
        areas = [fast_particle_area(r) for r in regions]
        i = np.argmax(areas)
        im_label_one = im_label == (i + 1)

        # get relevant properties for the largest object
        props = skimage.measure.regionprops_table(
            label_image=im_label_one.astype(np.uint8),
            intensity_image=im,
            properties=(
                "area",
                "area_filled",
                "axis_major_length",
                "axis_minor_length",
                "orientation",
                "eccentricity",
                "feret_diameter_max",
                "centroid_local",
                "centroid_weighted_local",
                "moments_hu",
                "moments_weighted_hu",
            ),
        )
        props = pd.DataFrame(props)

        # plt.figure()
        # io.imshow(im_label_one * im)
        # plt.show()

        return props
    else:
        return None


def main(args):
    props = analyse(args.filename)
    print(props)
    print(props.columns)
    print(props.loc[0, "area"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse image")

    parser.add_argument(
        "filename",
        nargs="?",
        default="./data/raw/example/pond-2023-05-24-11h49_Cropped_4297.jpg",
        help="the name of the file to process (default: foo.txt)",
    )

    main(parser.parse_args())
