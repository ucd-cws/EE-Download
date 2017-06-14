# Earth Engine Downloader
This code downloads all images in an image collection from Earth Engine to a specified folder. It can be called from the command line or a Python module.

## Installation
This library requires you have set up access to Earth Engine via its Python API and already authenticated your account. [See here for more information](https://developers.google.com/earth-engine/python_install) on how to do that.
If you're on Windows, I recommend using Bash on Windows for this project, but won't detail that further here - the installation instructions below assume a bash prompt.

### Dependencies
The only dependency for this script, besides the Earth Engine Python API is pycurl for downloading the images. pycurl requires some system setup.

```
sudo apt-get install libcurl-dev
sudo pip install pycurl
```

You have to install the development package for curl before pycurl will compile. The above commands should handle installation.

## Command line usage
If you call the script on the command line, it has three simple, positional parameters:

1. The path or identifier of the ImageCollection to downloading
2. The output folder on the local machine to save images into
3. The maximum number of images to download

```
python ee_download.py "users/yourusername/path/to/image/collection" "/mnt/c/myusername/path/to/outputs" 9999
```

## Usage in Python
After installation, you can import the module and call the main functions - parameters to the bulk downloader are the same
as the command line usage above

```
import ee_download
downloaded_images = ee_download.download_images_in_collection(
		collection_id = "users/yourusername/path/to/image/collection",
		output_folder = "/mnt/c/myusername/path/to/outputs",
		max_items = 9999
)
```

Alternatively, if you just want to use the single image downloading mechanism, you can run
```
downloaded_images = ee_download.download_image_by_asset_path(
		asset_path = "users/yourusername/some/single/image",
		output_folder = "/mnt/c/myusername/path/to/outputs",
)
```

Each function returns the full paths to the downloaded items as a list.