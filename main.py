#!/usr/bin/env python

# Use the export data from CytoClus to construct a metadata file to
# allow the upload of CytoSense images to EcoTaxa.
#
# This is a minimalist implementation. For more information, see
# https://ecotaxa.obs-vlfr.fr/prj/

import pandas as pd
import argparse
import logging
import re
import os
import analyse_images


def get_root_name(filename):
    filename = os.path.basename(filename)
    pattern = r"^(.*?)_All"  # Matches everything before "_All"
    # pattern = r"([^/]+)All$"
    match = re.search(pattern, filename)
    if match:
        return match.group(1)
    else:
        return None


def get_field(df, name):
    if df is None:
        return None
    try:
        return df.loc[0, name]
    except (KeyError, IndexError):
        return None


def convert(path, filename):
    df = pd.read_csv(filename)
    root = get_root_name(filename)
    # Row one contains tab separated field names
    print("object_id", end="")
    print("\timg_file_name", end="")
    print("\tobject_area", end="")
    # print("\tarea_filled", end="")
    print("\tobject_axis_minor_length", end="")
    print("\tobject_orientation", end="")
    print("\tobject_eccentricity", end="")
    print("\tobject_feret_diameter_max", end="")
    print("\tobject_centroid_local-0", end="")
    print("\tobject_centroid_local-1", end="")
    print("\tobject_centroid_weighted_local-0", end="")
    print("\tobject_centroid_weighted_local-1", end="")
    print()
    # Row two contains tab separated types [t] for text [f] for float
    print("[t]\t[t]\t[f]\t[f]\t[f]\t[f]\t[f]\t[f]\t[f]\t[f]\t[f]")
    for i, row in df.iterrows():
        # Reference both the cropped and uncropped images of each
        # particle
        particle_id = int(row["Particle ID"])
        image_name = f"{root}_Cropped_{particle_id}.jpg"
        props = analyse_images.analyse(os.path.join(path, image_name))
        if props is None:
            continue
        print(f"{particle_id}", end="")
        print(f"\t{image_name}", end="")
        print(f"\t{get_field(props,'area')}", end="")
        # print(f"\t{get_field(props,'area_filled')}", end="")
        print(f"\t{get_field(props,'axis_minor_length')}", end="")
        print(f"\t{get_field(props,'orientation')}", end="")
        print(f"\t{get_field(props,'eccentricity')}", end="")
        print(f"\t{get_field(props,'feret_diameter_max')}", end="")
        print(f"\t{get_field(props,'centroid_local-0')}", end="")
        print(f"\t{get_field(props,'centroid_local-1')}", end="")
        print(f"\t{get_field(props,'centroid_weighted_local-0')}", end="")
        print(f"\t{get_field(props,'centroid_weighted_local-1')}", end="")
        print()


def main(args):
    convert(args.path, args.filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CytoClus to Ecotaxa")

    parser.add_argument(
        "filename",
        nargs="?",
        default="/mnt/c/data/cytobuoy-examples-20230524/Sea/pond 2023-05-24 11h49_All Imaged Particles_Listmode.csv",
        help="the name of the file to process (default: foo.txt)",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default="/mnt/c/data/cytobuoy-examples-20230524/Sea/pond 2023-05-24 11h49_All Imaged Particles_Images/",
        help="the name of the file to process (default: foo.txt)",
    )

    main(parser.parse_args())
