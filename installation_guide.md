# Installation guide AstroCV
The following steps have been tested with Ubuntu 16.04 and Python 2.7. The GPU used is Nvidia GTX1060. For every requisite for AstroCV, you can follow the respective installation guide, but the main steps will still be included here.

## Required packages
First, we download all packages required for the libraries. In terminal, input the following commands.


```
sudo apt-get -y install gcc gfortran python-dev libopenblas-dev liblapack-dev cython
sudo apt install python-pip*
sudo pip install --upgrade pip*
python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose 
sudo pip install pytest*
sudo apt-get install libxml2-dev libxslt-dev 
sudo pip install h5py beautifulsoup4 pyyaml lxml pytz scikit-image objgraph setuptools mock bintrees*
sudo pip install astropy --no-deps
sudo pip install astroquery
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavformat-dev libswscale-dev
sudo apt-get install curl m4 ruby texinfo libbz2-dev libcurl4-openssl-dev libexpat-dev libncurses-dev zlib1g-dev
sudo apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install --assume-yes unzip ffmpeg qtbase5-dev
sudo apt-get install --assume-yes libopencv-dev libgtk-3-dev libdc1394-22 libdc1394-22-dev libjpeg-dev
sudo apt-get install --assume-yes libxine2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
sudo apt-get install --assume-yes libv4l-dev libtbb-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev
sudo apt-get install --assume-yes libvorbis-dev libxvidcore-dev v4l-utils vtk6
sudo apt-get install --assume-yes liblapacke-dev libgdal-dev checkinstall
sudo apt-get install build-essential
sudo apt-get update && sudo apt-get upgrade
```



## Installing CUDA 8.0

Now we will install CUDA 8.0 First, check that you have NVIDIA drivers installed with
```
nvidia-smi
```
Download the CUDA .dev files from [https://developer.nvidia.com/cuda-80-download-archive]. You might want to sign up with an account, since you'll need it later for CUDNN installation. From the terminal, go to the path where you downloaded the files and run

```
echo -e "blacklist nouveau\nblacklist lbm-nouveau\noptions nouveau modeset=0\nalias nouveau off\nalias lbm-nouveau off\n" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
echo options nouveau modeset=0 | sudo tee -a /etc/modprobe.d/nouveau-kms.conf
sudo update-initramfs -u
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local_8.0.44-1_amd64.deb
sudo apt-get update
sudo apt-get install cuda
```
CUDA is installed. To verify that, run the following code:

```
nvcc --version
```

If Ubuntu doesn't find CUDA, run the next file:

```
export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}" into ~/.bashrc

```

## Installing cuDNN 5.1

Download Runtime Library, Developer Library and Code Samples .deb files from [https://developer.nvidia.com/rdp/cudnn-download]. You want to download cuDNN 5.1 for CUDA 8.0.

From terminal, go to the path where you downloaded cuDNN files and run

```
sudo dpkg -i libcudnn5_5.1.10-1+cuda8.0_amd64.deb 
sudo dpkg -i libcudnn5-dev_5.1.10-1+cuda8.0_amd64.deb 
sudo dpkg -i libcudnn5-doc_5.1.10-1+cuda8.0_amd64.deb 

```

If you want to test installation, run in terminal:

```
cp -r /usr/src/cudnn_samples_v7/ $HOME
cd  $HOME/cudnn_samples_v7/mnistCUDNN
$make clean && make
./mnistCUDNN

```
If the installation was successful, you will read a message similar to "Test passed!"


## Installing OpenCV 3.3.0

For both OpenCV and PyYOLO, I created the ~/git folder (in Home), where I'll download all clones from github. All path references will be done considering this.

Open a terminal where you want to download OpenCV and run

```
git clone --recursive https://github.com/astroCV/opencv

mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D FORCE_VTK=ON -D WITH_TBB=ON -D WITH_V4L=ON -D WITH_QT=ON -D WITH_OPENGL=ON -D WITH_CUBLAS=ON -D CUDA_NVCC_FLAGS="-D_FORCE_INLINES" -D WITH_GDAL=ON -D WITH_XINE=ON -D BUILD_EXAMPLES=ON ..
make -j8
```


Now you're ready to begin the installation. In the same directory (~/git/opencv/build) run in a terminal.

```
sudo make install
sudo /bin/bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'
sudo ldconfig
sudo apt-get update
```
You can check the installation by importing cv2 (import cv2) in any Python enviroment.

Reboot your computer.

## Installing PyYOLO

Open a terminal where you want to install PyYOLO and run

```
git clone --recursive https://github.com/astroCV/pyyolo.git
cd pyyolo
```
We need to modify the Makefile file before continuing. In the same folder run
```
sudo gedit Makefile
```
Set GPU=1, CUDNN=1, DEBUG=0 and OPENCV=0.

Replace NVCC = nvcc for NVCC = /usr/local/cuda-8.0/bin/nvcc

Save changes and close Makefile. Now run in terminal

```
sudo make
rm -rf build
python setup_gpu.py build
sudo python setup_gpu.py install
```

You can check the installation by importing pyyolo (import pyyolo) in any Python enviroment.

## Preparing AstroCV

Now we have all the prerequisites needed for running AstroCV. To download AstroCV, opoen a terminal in the path you want your download and run

```
git clone --recursive https://github.com/astroCV/astroCV.git

```
If you want to run the examples, you'll need the pre-trained weights. You can download them from [https://github.com/astroCV/astroCV/tree/master/galaxy_detection], in the Trained Networks section. You'll need to change the paths to the weights in the examples for them to run.
