# Galaxy Detection and Classification in SDSS using deep learning

The examples show how to detect and classify galaxies in SDSS images using [YOLO](https://github.com/astroCV/darknet).

Training was made using images from SDSS in r,g,i bands converted to RGB color scale using [make_lupton_rgb](http://docs.astropy.org/en/stable/api/astropy.visualization.make_lupton_rgb.html) method.
Galaxy classification was taken from [Galaxy Zoo](https://www.galaxyzoo.org/).
We train the network with nearly 20000 galaxies located in nearly 7000 SDSS images, with 5 classiffications: elliptical, spiral, edge-on, DK, merge.

##

Download trained network from [Here(200Mb)](https://drive.google.com/file/d/0B8RHInq4tQDvZUl3N0VGSklrOG8/view?usp=sharing)


## Requeriments

Download [pyyolo](https://github.com/astroCV/pyyolo) wrapper.

## Install and run

Compile darknet from the original repository or from data/darknet using make. 
Notice that in data/darknet/Makefile you must set GPU=1 for CUDA usage and ARCH parameter depending on your graphics card.

Just run jupyter-notebook on examples
