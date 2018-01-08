#Installation guide AstroCV
The following steps have been tested with Ubuntu 16.04 and Python 2.7. The GPU used is Nvidia GTX1060. For every requisite for AstroCV, you can follow the respective installation guide, but the main steps will still be included here.

##Required packages
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

##Installing CUDA
