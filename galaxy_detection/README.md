# Galaxy Detection and Classification in SDSS using deep learning

The examples show how to detect and classify galaxies in SDSS images using [YOLO](https://github.com/astroCV/darknet).

Training was made using images from SDSS in r,g,i bands converted to RGB color scale using [make_lupton_rgb](http://docs.astropy.org/en/stable/api/astropy.visualization.make_lupton_rgb.html) method.
Galaxy classification was taken from [Galaxy Zoo](https://www.galaxyzoo.org/).
We train the network with nearly 20000 galaxies located in nearly 7000 SDSS images, with 5 classiffications: elliptical, spiral, edge-on, DK, merge.

##

Download trained network from [Here(200Mb)](https://drive.google.com/file/d/0B8RHInq4tQDvTTliOEt0SFViWDg/view?usp=sharing)


## Requeriments

Download [pyyolo](https://github.com/astroCV/pyyolo) wrapper.

## Install and run

Compile darknet from the original repository or from data/darknet using make. 
Notice that in data/darknet/Makefile you must set GPU=1 for CUDA usage and ARCH parameter depending on your graphics card.

Just run jupyter-notebook on examples

## Train your own Dataset

In training folder you will find the scripts to generate the training data for DARKNET.

Configuration files data/sdss.cfg, data/sdss.data and data/sdss.names can be used for the training, yust uncomment lines 5 & 6.

To begin the training using two GPU cards you can use a command like:

./darknet detector train cfg/sdss.data cfg/yolo.cfg darknet19_448.conv.23 -gpus 0,1

You can stop the training and restart using a command like:

./darknet detector train cfg/sdss.data cfg/yolo.cfg result/yolo.backup -gpus 0,1

Test on a single image:

./darknet detector test cfg/sdss.data cfg/yolo.cfg result/yolo_backup.weights image.jpg 

Using nearly 20000 galaxies we stopped training around 20000 iterations, and notice best convergence around 15000 iterations. However, for a custom dataset the only way to check convergence is compute the recall ration for different iterations.
