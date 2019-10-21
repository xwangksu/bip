'''
Created on Nov 15, 2018

@author: xuwang
'''
import argparse
import PhotoScan
import os
import errno

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
args = vars(ap.parse_args())
workingPath = args["wpath"]+"\\"
print("Working path is: %s" % workingPath)

try:
    os.makedirs(workingPath+"orthophotos")
    print("Creating Calibrated directory.")
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

project = workingPath+"ortho_dem_process.psx"

app = PhotoScan.Application()
doc = PhotoScan.app.document
doc.open(project)

chunk = doc.chunk
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")

chunk.exportOrthophotos(path=workingPath+"orthophotos\\{filename}.tif", cameras=chunk.cameras, raster_transform=PhotoScan.RasterTransformType.RasterTransformNone,
                        projection=chunk.crs, write_kml=False,
                        write_world=False, write_alpha=False, tiff_compression=PhotoScan.TiffCompression.TiffCompressionNone,
                        tiff_big=False, tiff_overviews=True, jpeg_quality=100, white_background=False)    

doc.save(path=project, chunks=[doc.chunk])