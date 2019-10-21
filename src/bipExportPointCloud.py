'''
Created on Sep 5, 2019

@author: xuwang
'''
import argparse
import PhotoScan
import os
import errno

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
ap.add_argument("-pc", "--pointcolor", required=True, help="pointColorTrueFalse")
args = vars(ap.parse_args())
workingPath = args["wpath"]+"\\"
pcTF = args["pointcolor"]
print("Working path is: %s" % workingPath)

try:
    os.makedirs(workingPath+"pointcloud")
    print("Creating Point Cloud Directory.")
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

project = workingPath+"ortho_dem_process.psx"

app = PhotoScan.Application()
doc = PhotoScan.app.document
doc.open(project)

chunk = doc.chunk
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")

if int(pcTF) > 0:
    chunk.exportPoints(path = workingPath+"pointcloud\\dpc.txt", binary = False, precision = 8,
                       normals = False, colors = True, raster_transform = PhotoScan.RasterTransformType.RasterTransformNone,
                       format = PhotoScan.PointsFormat.PointsFormatXYZ, projection = PhotoScan.CoordinateSystem("EPSG::4326"))
else:
    chunk.exportPoints(path = workingPath+"pointcloud\\dpc.txt", binary = False, precision = 8,
                       normals = False, colors = False, raster_transform = PhotoScan.RasterTransformType.RasterTransformNone,
                       format = PhotoScan.PointsFormat.PointsFormatXYZ, projection = PhotoScan.CoordinateSystem("EPSG::4326"))

doc.save(path=project, chunks=[doc.chunk])