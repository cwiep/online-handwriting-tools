#!/usr/bin/env python

import sys
import argparse
import scipy.cluster.vq as vq
import numpy

from traj import trajimport
from traj import trajnorm
from traj import trajfeat
from traj import boof
from traj import spatialpyramid


NORM_ARGS = ["flip", "slope", "resample", "slant", "height", "origin"]
FEAT_ARGS = ["dir", "curv", "vic_aspect", "vic_curl", "vic_line", "vic_slope", "bitmap"]
SPATIAL_PYRAMID_LEVELCONF = [[6, 2], [3, 2]]
NUM_CLUSTERS = 128


def process_single_file(filename, outfilename, normalize=False, cluster_file=None):
    print("Importing {}...".format(filename))
    traj, word = trajimport.read_trajectory_from_file(filename)
    print("Read {} points for word '{}'.".format(len(traj), word))
    
    if normalize:
        print("Normalizing trajectory...")
        traj = trajnorm.normalize_trajectory(traj, NORM_ARGS)

    print("Calculating feature vector sequence...")
    feat_seq_mat = trajfeat.calculate_feature_vector_sequence(traj, FEAT_ARGS)

    if cluster_file is not None:
        print("Reading cluster file...")
        clusters = trajimport.read_traj_clusters(cluster_file)
        print("Read {} clusters.".format(len(clusters)))

        print("Quantizing feature vectors. This may take some time...")
        labels, _ = vq.vq(feat_seq_mat, clusters)

        print("Calculating bag-of-features representation...")
        spatial_pyramid = spatialpyramid.SpatialPyramid(SPATIAL_PYRAMID_LEVELCONF, NUM_CLUSTERS)
        gen = boof.BoofGenerator(spatial_pyramid)
        bof = gen.build_feature_vector(traj[:, :2], labels)
        print("Calculated bag-of-feature representation of length {}".format(len(bof)))
        print("Writing {}...".format(outfilename))
        numpy.savetxt(outfilename, bof)
    else:
        # otherwise we just save the feature vector sequence
        print("Writing {}...".format(outfilename))
        numpy.savetxt(outfilename, feat_seq_mat)


def main(argv):
    parser = argparse.ArgumentParser(description="Calculate feature vector sequences or bag-of-features representations for a online-handwritten trajectory.")
    parser.add_argument("trajectoryfile", help="path to trajectory file")
    parser.add_argument("-n", "--normalize", action="store_true", default=False, help="normalize input trajectory (default=False)")
    parser.add_argument("-b", "--bof", nargs=1, help="use given cluster file to calculate bag-of-features representation for input trajectory (default=False)", metavar="cluster_file")
    parser.add_argument("resultfile", help="resulting bag-of-feature representation or feature vector sequence (depending on other parameters) is written into outfile in numpy-txt format")
    
    if len(argv) == 1:
        # no parameters given
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    cluster_file = None if args.bof is None else args.bof[0]
    process_single_file(args.trajectoryfile, args.resultfile, normalize=args.normalize, cluster_file=cluster_file)
    

if __name__ == '__main__':
    main(sys.argv)
    
