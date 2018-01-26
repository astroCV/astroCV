## AstroCV

AstroCV (<http://astrocv.github.io>) is a package intended to contain computer vision algorithms and methods for processing and analyzing astronomical datasets. The main goal is developing and promoting the use of modern computer vision algorithms for solving scientific problems in Astronomy.

For installation instructions, see the online documentation or installation_guide.md in this source distribution.

## Contents

### galaxy_detection

Four examples can be found in this folder. These examples show detections in different images. The first and second example work with .jpg images. The third example downloads images from the web. The fourth example processes three .fits images for the same photo (i, r and g filters), then applies different filters to the rgb matrix (e.g. lupton, sqrt) and finally tests the detector with the images. 

In the traning folder, you can find .py codes to download the images from SDSS and prepare the training.

### tutorials

This folder contains introductive tutorials to computer vision, deep learning and creating a dataset from the NGFS survey.

### tools/color_image

In this folder you can find two .py scripts for making galaxy snapshots and creating .jpg images.

## Download data

[Download NGFS data](https://www.scidrive.org/scidrive/scidrive.html?share=OGDXRuYTNlgvgti)

[Download AstroCV data](https://www.scidrive.org/scidrive/scidrive.html?share=7YANf7V8SnBzIgi)


## License
Astropy is licensed under a 3-clause BSD style license - see the
``LICENSE`` file.
