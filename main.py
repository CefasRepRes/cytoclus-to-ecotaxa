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


def get_root_name(filename):
    filename = os.path.basename(filename)
    pattern = r"^(.*?)_All"  # Matches everything before "_All"
    # pattern = r"([^/]+)All$"
    match = re.search(pattern, filename)
    if match:
        return match.group(1)
    else:
        return None


def convert(filename):
    df = pd.read_csv(filename)
    root = get_root_name(filename)
    # Row one contains tab separated field names
    print("object_id\timg_file_name")
    # Row two contains tab separated types [t] for text [f] for float
    print("[t]\t[t]")
    for i, row in df.iterrows():
        # Reference both the cropped and uncropped images of each
        # particle
        particle_id = int(row["Particle ID"])
        print(f"{particle_id}\t{root}_Cropped_{particle_id}.jpg")
        print(f"{particle_id}\t{root}_Uncropped_{particle_id}.jpg")


def main(args):
    convert(args.filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CytoClus to Ecotaxa")

    parser.add_argument(
        "filename",
        nargs="?",
        default="/mnt/c/data/cytobuoy-examples-20230524/Sea/pond 2023-05-24 11h49_All Imaged Particles_Listmode.csv",
        help="the name of the file to process (default: foo.txt)",
    )

    main(parser.parse_args())
