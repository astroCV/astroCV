#!/usr/bin/python

import sys,os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle
from astropy.table import Table, Column, vstack, join
import aplpy
import skimage
import skimage.io
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from pyavm import AVM
from tabulate import tabulate

class ArgumentError(Exception):
    pass

def main(argv):

	config_file=None
	list_file=None

	try:
		opts, args = getopt.getopt(argv,"hc:l:p:f:",["config=","list=","prefix=","filters="])
	except getopt.GetoptError:
		print 'make_rgb_image.py -c <configuration file> -l <image file list> -p <prefix> -f <filters>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'make_rgb_image.py -c <configuration file> -l <image file list> -p <prefix> -f <filters>'
			sys.exit()
		elif opt in ("-c", "--config"):
			config_file = arg
		elif opt in ("-l", "--list"):
			list_file = arg
		elif opt in ("-p", "--prefix"):
			prefix = arg
		elif opt in ("-f", "--filters"):
			filters = string.split(arg,',')

	if config_file is None or list_file is None:
		raise ArgumentError("You need to supply a configuration file and an image file list")

	print 'Configuration file is ', config_file
	print 'Image file list is ', list_file

	config_data = ConfigParser.ConfigParser()
	config_data.read(config_file)

	prefix=config_data.get('Stack','prefix')
	filters=string.split(config_data.get('Stack','filters'),',')
	stack_name=config_data.get('Stack','stack_name')
	stack_version=config_data.get('Stack','stack_version')
	stack_tile_ref=config_data.get('Stack','stack_tile_ref')
	stack_filter_ref=config_data.get('Stack','stack_filter_ref')

	list_data = np.loadtxt(list_file, dtype={'names': ('tile', 'image', 'catalog'), 'formats': ('S10', 'S50', 'S50')})

	stack_tile=np.unique(list_data['tile'])
	image_file=list_data['image']
	catalog_file=list_data['catalog']

	stack_filter=filters
	print "List of tiles: ", stack_tile
	print "List of filters: ", stack_filter_ref



	im_rgb_hd_file= '../catalogs/ngfs_tile1_rgb_asinh_v2.jpg'
	im_rgb_sd_file= '../catalogs/ngfs_tile1_rgb_asinh_v2_sd.png'
	cat_ngfs_nuc=ascii.read('../catalogs/NGFS_FCC_cat_nucleated.dat', format='fixed_width') #, fill_values=('', 'NA'))
	cat_ngfs_non=ascii.read('../catalogs/NGFS_FCC_cat_non_nucleated.dat', format='fixed_width') #, fill_values=('', 'NA'))

	decam_scale=0.263*u.arcsec
	fornax_distance=20.0*u.Mpc
	dwarf_zoom_radius=Angle(30*u.arcsec)

	#cat_ngfs_nuc.add_row()

	cat_ngfs=cat_ngfs_nuc
	cat_ngfs.add_column( Column( np.full(len(cat_ngfs),np.nan), name='mu_i' ) )
	cat_ngfs['mu_i']=cat_ngfs['m_i']+2.5*np.log10(2*np.pi* cat_ngfs['reff_arcsec']**2 )

	gv=cat_ngfs['Reference'].mask.nonzero()  # Look for the masked values
	cat_ngfs['Reference'][gv]=''  # Replace the masked values with a null string

	n=np.int(np.ceil(np.sqrt(len(cat_ngfs))))
	fig = plt.figure(figsize=(14.,14.), dpi=300)
	gs=gridspec.GridSpec(n, n)
	gs.update(left=0.03, right=0.97, bottom=0.03, top=0.97, wspace=0.2, hspace=0.2)

	# Now reading the HD rgb image

	im_data = np.flipud(skimage.io.imread(im_rgb_hd_file))
	im_size= im_data.shape
	avm=AVM.from_image(im_rgb_hd_file)
	w = avm.to_wcs()
	w.naxis1=im_size[1]
	w.naxis2=im_size[0]

	# Sort them by magnitude
	cat_ngfs.sort('M_i')
	cat_ngfs_coo = SkyCoord(cat_ngfs['RA'], cat_ngfs['DEC'], unit="deg")

	for i in np.arange(len(cat_ngfs)):
		print 'Processing NGFS dwarf ', cat_ngfs['ID'][i]

		ax=plt.subplot(gs[i])
		ax.set_aspect('equal')
		ax.axis('off')
		
		im_crop_coo=w.wcs_world2pix([[ cat_ngfs_coo.ra[i].deg,(cat_ngfs_coo.dec[i]+dwarf_zoom_radius).deg],[cat_ngfs_coo.ra[i].deg,(cat_ngfs_coo.dec[i]-dwarf_zoom_radius).deg]], 1)
		im_crop_size=(np.abs(im_crop_coo[0,1]-im_crop_coo[1,1])*np.asarray([1.,1.])).astype(int)
		im_crop_coo=(w.wcs_world2pix([[ cat_ngfs_coo.ra[i].deg, cat_ngfs_coo.dec[i].deg]], 1)[0]).astype(int)
		im_crop_data=im_data[im_crop_coo[1]-im_crop_size[1]/2:im_crop_coo[1]+im_crop_size[1]/2,im_crop_coo[0]-im_crop_size[0]/2:im_crop_coo[0]+im_crop_size[0]/2]
		skimage.io.imsave('dwarf_zoom.png', np.flipud(im_crop_data))

		im_crop_size= im_crop_data.shape
		w_crop=w[:]
		w_crop.naxis1=im_crop_size[1]
		w_crop.naxis2=im_crop_size[0]
		w_crop.wcs.crpix[0] -= (im_crop_coo[0]-im_crop_size[0]/2)
		w_crop.wcs.crpix[1] -= (im_crop_coo[1]-im_crop_size[1]/2)
		
		f = aplpy.FITSFigure(w_crop, figure=fig, subplot=list(ax.get_position().bounds) )
		f.axis_labels.hide()
		f.tick_labels.hide()
		f.ticks.hide()
		f.show_rgb('dwarf_zoom.png')
	#	f.add_label( (cat_ngfs_coo.ra[i]+dwarf_zoom_radius*1.).deg, (cat_ngfs_coo.dec[i]-dwarf_zoom_radius*0.8).deg, cat_ngfs['ID'][i], size=7, color='silver', horizontalalignment='left', alpha=0.8, family='sans-serif', style='italic' )
	#	f.add_label( (cat_ngfs_coo.ra[i]+dwarf_zoom_radius*1.).deg, (cat_ngfs_coo.dec[i]-dwarf_zoom_radius*0.95).deg, cat_ngfs['Reference'][i], size=7, color='silver', horizontalalignment='left', alpha=0.8, family='sans-serif', style='italic' )

	fig.savefig('../figures/NGFS_dwarfs_nucleated_tile1_SORT_total_magnitude_nolabels.pdf', dpi=300)
	sys.exit()

	cat_ngfs.sort('mu_i')
	cat_ngfs_coo = SkyCoord(cat_ngfs['RA'], cat_ngfs['DEC'], unit="deg")

	for i in np.arange(len(cat_ngfs)):
		print 'Processing NGFS dwarf ', cat_ngfs['ID'][i]

		ax=plt.subplot(gs[i])
		ax.set_aspect('equal')
		ax.axis('off')
		
		im_crop_coo=w.wcs_world2pix([[ cat_ngfs_coo.ra[i].deg,(cat_ngfs_coo.dec[i]+dwarf_zoom_radius).deg],[cat_ngfs_coo.ra[i].deg,(cat_ngfs_coo.dec[i]-dwarf_zoom_radius).deg]], 1)
		im_crop_size=(np.abs(im_crop_coo[0,1]-im_crop_coo[1,1])*np.asarray([1.,1.])).astype(int)
		im_crop_coo=(w.wcs_world2pix([[ cat_ngfs_coo.ra[i].deg, cat_ngfs_coo.dec[i].deg]], 1)[0]).astype(int)
		im_crop_data=im_data[im_crop_coo[1]-im_crop_size[1]/2:im_crop_coo[1]+im_crop_size[1]/2,im_crop_coo[0]-im_crop_size[0]/2:im_crop_coo[0]+im_crop_size[0]/2]
		skimage.io.imsave('dwarf_zoom.png', np.flipud(im_crop_data))

		im_crop_size= im_crop_data.shape
		w_crop=w[:]
		w_crop.naxis1=im_crop_size[1]
		w_crop.naxis2=im_crop_size[0]
		w_crop.wcs.crpix[0] -= (im_crop_coo[0]-im_crop_size[0]/2)
		w_crop.wcs.crpix[1] -= (im_crop_coo[1]-im_crop_size[1]/2)
		
		f = aplpy.FITSFigure(w_crop, figure=fig, subplot=list(ax.get_position().bounds) )
		f.axis_labels.hide()
		f.tick_labels.hide()
		f.ticks.hide()
		f.show_rgb('dwarf_zoom.png')
		f.add_label( (cat_ngfs_coo.ra[i]+dwarf_zoom_radius*1.).deg, (cat_ngfs_coo.dec[i]-dwarf_zoom_radius*0.8).deg, cat_ngfs['ID'][i], size=7, color='silver', horizontalalignment='left', alpha=0.8, family='sans-serif', style='italic' )
		f.add_label( (cat_ngfs_coo.ra[i]+dwarf_zoom_radius*1.).deg, (cat_ngfs_coo.dec[i]-dwarf_zoom_radius*0.95).deg, cat_ngfs['Reference'][i], size=7, color='silver', horizontalalignment='left', alpha=0.8, family='sans-serif', style='italic' )

	fig.savefig('../figures/NGFS_dwarfs_nucleated_tile1_SORT_surface_brightness.pdf', dpi=300)
