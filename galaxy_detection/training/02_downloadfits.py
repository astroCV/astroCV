#!/usr/bin/env python
from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy.io import fits
import numpy as np
from PIL import Image
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from astropy.table import Table,vstack,Column,unique
import copy
import os.path

#DOWNLOAD SDSS FITS IMAGES WHERE WE FOUND AT LEAST 1 ZOO GALAXY 

xid = Table.read('zoospecnewall2.data',format='ascii')
xuniq = Table.read('unique.data',format='ascii')
ngal=len(xid)
nuniq=len(xuniq)
print(ngal,nuniq)

#1586 is corrupted!
istart=0
iend=1000 #number of images to download for training (~230k)

for k in range(iend-istart):
    i=k+istart
    run=xuniq['run'][i]
    rerun=xuniq['rerun'][i]
    camcol=xuniq['camcol'][i]
    field=xuniq['field'][i]
    fnamer='images/%s.r.fits'%(xuniq['imagename'][i])    
    fnameg='images/%s.g.fits'%(xuniq['imagename'][i])    
    fnamei='images/%s.i.fits'%(xuniq['imagename'][i])    
    if os.path.isfile(fnamer):    
	print('i=%d file exist %s'%(i,fnamer))
    if not os.path.isfile(fnamer):
        im = SDSS.get_images(run=run,rerun=rerun,camcol=camcol,field=field,band=['r','g','i'],timeout=120)
        if len(im) < 3:
		print('i=%d no data file skip!!!!!'%(i))
        if len(im) >= 3:
	        imr=im[0]
       		img=im[1]
        	imi=im[2]
        	imr.writeto(fnamer)
        	img.writeto(fnameg)
        	imi.writeto(fnamei)
		print('i=%d downloaded %s'%(i,fnamer))
#   if i%10==0:
#       print('i=%d'%i)
