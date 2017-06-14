import sys
import os
import errno
from zipfile import is_zipfile, ZipFile

import pycurl

import ee
import ee.mapclient

max_items = 99999

ee.Initialize()

def download_image_by_asset_path(asset_path, output_folder):
	"""
		Downloads an individual image, given its asset path, and saves it to output_folder.
		Returns a list of the downloaded image or images
	"""
	### Get the download URL from EE
	image = ee.Image(asset_path)  # this approach comes from https://github.com/google/earthengine-api/blob/master/python/examples/py/Image/download.py
	path = image.getDownloadUrl({
		#'scale': 30,
		#'crs': 'EPSG:3310',
		#'region': '[[-120, 35], [-119, 35], [-119, 34], [-120, 34]]'
	})
	
	### Do some name management things
	output_name = os.path.split(asset_path)[1]
	zipfile = output_name + ".zip"
	download_path = os.path.join(output_folder, zipfile)  # comes as a zip file with a .tfw
	output_path = os.path.join(output_folder, output_name + ".tif")
	
	# check that the output path exists - create it if not
	makedirs(output_folder)
	
	### Download the file
	with open(download_path, 'wb') as f:
		c = pycurl.Curl()
		c.setopt(c.URL, path)
		c.setopt(c.WRITEDATA, f)
		c.perform()
		c.close()
		
	### Extract the Zip and delete it
	if not is_zipfile(download_path):
		raise RuntimeError("Downloaded file was not a zip file!")
	
	with open(download_path, 'r') as zf:
		z = ZipFile(zf)
		downloaded_items = [os.path.join(output_folder,item) for item in z.namelist() if not item.endswith("tfw") ]
		z.extractall(path=output_folder)
		z.close()
		del z
	
	os.remove(download_path)
	
	return downloaded_items

	
def makedirs(path):
	"""
		Handles nice directory creation in Python 2.7 - see https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python/600612#600612
	"""
	try:
		os.makedirs(path)
	except OSError as exc:  # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

	
def download_images_in_collection(collection_id, output_folder, max_items=max_items):
	"""
		Downloads images in ImageCollection specified by collection_id and saves them into 
		the location specified in output folder, up to max_items downloads. Set max_items
		to a very high number to download all items.
		
		Returns a list with the full paths to the downloaded images.
	"""
	
	### Get all of the items in the collection
	collection = ee.ImageCollection(collection_id)
	collection_items = collection.toList(max_items).getInfo()
	
	downloaded_items = []
	for item in collection_items:
		downloaded_items += download_image_by_asset_path(item["id"], output_folder)  # extend the list with the new list that's produced - don't append
		
	return downloaded_items

if __name__ == "__main__":
	args = sys.argv[1:]
	collection_id = args[0]
	output_folder = args[1]
	max_items = int(args[2])

	download_images_in_collection(collection_id, output_folder, max_items=max_items)