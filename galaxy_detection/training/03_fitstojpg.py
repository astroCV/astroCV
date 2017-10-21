#!/usr/bin/env python3
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
from astropy.visualization import make_lupton_rgb
from reproject import reproject_interp

#CONVERT FITS IMAGES TO RGB

istart=31000
iend=32300

nskip=0
xid = Table.read('zoospecnewall2.data',format='ascii')
xuniq = Table.read('unique.data',format='ascii')
ngal=len(xid)
nuniq=len(xuniq)
for k in range(iend-istart):
    i=k+istart
    fnamer='images/%s.r.fits'%(xuniq['imagename'][i])    
    fnameg='images/%s.g.fits'%(xuniq['imagename'][i])    
    fnamei='images/%s.i.fits'%(xuniq['imagename'][i])    
    fjpg = 'jpeg/%s.jpg'%(xuniq['imagename'][i]) 
    #fjpgb= 'jpeg/%s.bw.jpg'%(xuniq['imagename'][i])
    #print('i=%d current attemp %s '%(i,fnamer))
    if not os.path.isfile(fnamer):    
        print('i=%d file does not exist %s skipping...'%(i,fnamer))
        nskip=nskip+1
    if os.path.isfile(fjpg):
        print('i=%d jpg image already exist %s skipping...'%(i,fjpg))
        nskip=nskip+1
    if (os.path.isfile(fnamer) and not os.path.isfile(fjpg)):
        imrr=fits.open(fnamer)
        imgg=fits.open(fnameg)
        imii=fits.open(fnamei)
        imr=imrr[0]
        img=imgg[0]
        imi=imii[0]
        ir = imr.data
        w=ir.shape[1]
        h=ir.shape[0]
        ig, footprint1 = reproject_interp(img, imr.header)
        ii, footprint2 = reproject_interp(imi, imr.header)
        image = make_lupton_rgb(ii,ir,ig)
        #image2= make_lupton_rgb(ir,ir,ir)
        wimage = Image.fromarray(image)
        wimage.save(fjpg,'jpeg',quality=97) # 97% best background 350k
        #wimageb = Image.fromarray(image2)
        #wimageb.save(fjpgb,'jpeg',quality=92)        
        print('i=%d saved %s w=%d h=%d'%(i,fjpg,w,h))

print('skipped files = %d'%(nskip))
