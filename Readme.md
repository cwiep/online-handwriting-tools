# Online Handwriting Tools

Python library and tool for calculating bag-of-features representations for online-handwritten trajectories. This project was designed to work with the [Online-Handwritten George Washington Dataset]. See there for more information about the expected trajectory file format.

Run ```./tool.py``` for basic usage and 
```./tool.py exampledata/company_traj.txt out.txt -n -b exampledata/clusters.txt```
for calculating a bof representation of the normalized example trajectory.

As of now, the following parameters of the processing pipeline can only be changed in code (see tool.py):
* normalization steps (see traj/trajnorm.py for documentation)
* online-handwritten features (see traj/trajfeat.py for documentation)
* configuration of the spatial pyramid (see traj/spatialpyramid for documentation)

The tool's output is written in numpy-text format and is either a sequence of feature vectors (one for each point of the given trajectory, one vector per line) or a bag-of-features representation of the trajectory (one bin-value per line).

## Dependencies
* numpy
* scipy

## Folders
* traj/ contains the online-handwritten trajectory library
* exampledata/ contains an exemplary online-handwritten trajectory (company_traj.txt) as well as some pre-calculated clusters (clusters.txt)

## TODO
* support for different choices of normalization steps and features
* ? supporting batch calculations for multiple trajectories ?

## Licence
Apache License, Version 2.0

[//]: #

   [Online-Handwritten George Washington Dataset]: <https://github.com/cwiep/gw-online-dataset>
