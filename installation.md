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
sudo apt-get install libxml2-dev libxslt-dev python-dev 
sudo pip install h5py beautifulsoup4 pyyaml lxml pytz scikit-image pandas objgraph setuptools mock bintrees*
sudo pip install astropy --no-deps
sudo pip install astroquery
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
```



## Installing CUDA

Now we will install CUDA 8.0 First, check that you have NVIDIA drivers installed with
```
nvidia-smi
```
Download the CUDA .dev files from [https://developer.nvidia.com/cuda-downloads]. You might want to sign up with an account, since you'll need it later for CUDNN installation. From the terminal, go to the path where you downloaded the files and run

```
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64.deb 
sudo apt-get update
sudo apt-get install cuda
```

Now, you need to create a file called _nvidia-persistenced.service_ (it doesn't matter where you create it, you can delete it later.). Paste the following text into that file:




## Installing CUDNN

## Installing OpenCV

## Installing PyYOLO

## Installing AstroCV
