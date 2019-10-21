'''
Created on Apr 5, 2018

@author: Xu Wang
'''
import argparse
import PhotoScan

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
args = vars(ap.parse_args())
workingPath = args["wpath"]+"\\"
print("Working path is: %s" % workingPath)

dem = workingPath+"dem.tif"
orthomosaic = workingPath+"ortho.tif"
project = workingPath+"ortho_dem_process.psx"

app = PhotoScan.Application()
doc = PhotoScan.app.document
doc.open(project)

PhotoScan.app.gpu_mask = 1
# PhotoScan.app.cpu_enable = 8

chunk = doc.chunk
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")

chunk.buildDepthMaps(quality=PhotoScan.HighQuality, filter=PhotoScan.AggressiveFiltering)

chunk.buildDenseCloud()

chunk.buildModel(surface=PhotoScan.HeightField, interpolation=PhotoScan.DisabledInterpolation, face_count=PhotoScan.FaceCount.HighFaceCount)

doc.save(path=project, chunks=[doc.chunk])

doc = PhotoScan.app.document
doc.open(project)
app = PhotoScan.Application()

# PhotoScan.app.cpu_enable = 8

chunk = doc.chunk
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")

chunk.buildDem(source=PhotoScan.DataSource.DenseCloudData, interpolation=PhotoScan.Interpolation.DisabledInterpolation, projection=PhotoScan.CoordinateSystem("EPSG::4326"))

chunk.buildOrthomosaic(surface=PhotoScan.DataSource.ElevationData, blending=PhotoScan.BlendingMode.MosaicBlending, projection=PhotoScan.CoordinateSystem("EPSG::4326"))

chunk.exportDem(dem, image_format=PhotoScan.ImageFormatTIFF, projection=PhotoScan.CoordinateSystem("EPSG::4326"), nodata=-9999, write_kml=False, write_world=False, tiff_big=False)

chunk.exportOrthomosaic(orthomosaic, image_format=PhotoScan.ImageFormatTIFF, raster_transform=PhotoScan.RasterTransformType.RasterTransformNone, projection=PhotoScan.CoordinateSystem("EPSG::4326"), write_kml=False, write_world=False, tiff_compression=PhotoScan.TiffCompressionNone, tiff_big=False)

doc.save(path=project, chunks=[doc.chunk])