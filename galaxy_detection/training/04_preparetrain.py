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

#PREPARE TRAINING DATA SET FOR DARKNET
#CREATE IMAGES AND ANNOTATIONS IN DARKNET READABLE FORMAT.

#starting and ending galaxy image for training.
istart=0
iend=1000 #index of last image downloaded 

#in the outdir, you must create the images and labels subdirectories and inside them the train and val subdirectories.
outdir='/mnt/data2/sdss/yolo'
sample='train' #train or 'val' for generating the train and validation sample

xid = Table.read('zoospecnewall2.data',format='ascii')
print(xid.colnames)
xuniq = Table.read('unique.data',format='ascii')
ngal=len(xid)
nuniq=len(xuniq)
xidname = xid.group_by('imagename')

f1=open('%s/%s.txt'%(outdir,sample),'w')
nfiles=0
nann=0
n1=0 #yolo classes 5
n2=0
n3=0
n4=0
n5=0
for k in range(iend-istart):
    i=k+istart  
    imagename=xuniq['imagename'][i]
    fjpg = 'jpeg/%s.jpg'%(imagename) 
    ojpg = '%s/images/%s/%s.jpg'%(outdir,sample,imagename) 
    olab = '%s/labels/%s/%s.txt'%(outdir,sample,imagename) 
    mask = xidname.groups.keys['imagename'] == imagename
    xidn = xidname.groups[mask]
    nthis=len(xidn)
    if not os.path.isfile(fjpg):    
        print('i=%d file does not exist %s skip...'%(i,fjpg))
    if os.path.isfile(fjpg):
        image = Image.open(fjpg)
        #w=image.width
        #h=image.height
        w=image.size[0]
        h=image.size[1]
        #print('fff %d %d'%(w,h))
        maxprad=0
        for j in range(nthis):
            prad=xidn['petrorad_r'][j]/0.396127
            if prad > maxprad:
                maxprad=prad
        #if nthis<1:
		#print('i=%d file with no galaxy %s skip...'%(i,fjpg))
        #if maxprad<20:
		#if i%10==0:
                #	print('i=%d file with too tiny galaxies %s skip...'%(i,fjpg))
       
        if (nthis>=1 and maxprad>=20): # NOTICE WE DISCARD GALAXIES SMALLER THAN 20 PIXELS
		ff=open(olab,'w')
        	for j in range(nthis):
            		prad=2.1*xidn['petrorad_r'][j]/0.396127
            		colc=xidn['colc'][j]
            		rowc=xidn['rowc'][j]
			#'p_el', 'p_cw', 'p_acw', 'p_edge', 'p_dk', 'p_mg', 'p_cs'
			p_el =xidn['p_el'][j]
                        p_cw =xidn['p_cw'][j]
                        p_acw =xidn['p_acw'][j]
                        p_edge =xidn['p_edge'][j]
                        p_dk =xidn['p_dk'][j]
                        p_mg =xidn['p_mg'][j]
                        p_cs =xidn['p_cs'][j]
                        mylist=[p_el,p_cw+p_acw,p_edge,p_dk,p_mg]
                        mylist2=[p_cw+p_acw,p_edge,p_dk,p_mg]
                        if p_cs <= p_el:
				gtype = np.argmax(mylist)
			if p_cs > p_el:
				gtype = np.argmax(mylist2)+1
                                prad=prad*1.1 # extended obj
			if (gtype==0) and (prad>20):
				n1=n1+1
                        if gtype==1: 
                                n2=n2+1
                        if gtype==2: 
                                n3=n3+1
                        if gtype==3: 
                                n4=n4+1
                        if gtype==4: 
                                n5=n5+1
				prad=prad*1.2
#p_el fraction of votes for elliptical
#p_cw	float	8 	 	 	fraction of votes for clockwise spiral
#p_acw	float	8 	 	 	fraction of votes for anticlockwise spiral
#p_edge	float	8 	 	 	fraction of votes for edge-on disk
#p_dk	float	8 	 	 	fraction of votes for don't know
#p_mg	float	8 	 	 	fraction of votes for merger
#p_cs	float	8 	 	 	fraction of votes for combined spiral - cw + acw + edge-on
			if (prad > 20) or (gtype>0): 
	                	ff.write('%d %f %f %f %f\n'%(gtype,colc/w,rowc/h,prad/w,prad/h))
        	        	nann=nann+1
                ff.close()
        	image.save(ojpg,'jpeg',quality=97) # 97% best background 350k     
                f1.write('%s/images/%s/%s.jpg\n'%(outdir,sample,imagename))
		if i%50==0:
	        	print('i=%d %s w=%d h=%d nthis=%d maxprad=%f nfiles=%d anntot=%d'%(i,fjpg,w,h,nthis,maxprad,nfiles,nann))
		nfiles=nfiles+1

        if i%50==0:
                print('classes = %d %d %d %d %d'%(n1,n2,n3,n4,n5))


f1.close()
print('Final classes = %d %d %d %d %d tot=%d'%(n1,n2,n3,n4,n5,n1+n2+n3+n4+n5))
print('nfiles=%d nann=%d'%(nfiles,nann))
