'''
Created on Apr 5, 2018
Updated on Dec 2, 2020

@author: Xu Wang
'''
import argparse
import Metashape

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
args = vars(ap.parse_args())
workingPath = args["wpath"]+"\\"
print("Working path is: %s" % workingPath)

dem = workingPath+"dem.tif"
orthomosaic = workingPath+"ortho.tif"
project = workingPath+"ortho_dem_process.psx"

app = Metashape.Application()
doc = Metashape.app.document
doc.open(project)

Metashape.app.gpu_mask = 15
Metashape.app.cpu_enable = True

chunk = doc.chunk
chunk.crs = Metashape.CoordinateSystem("EPSG::4326")

chunk.buildDepthMaps(downscale=1, filter_mode=Metashape.AggressiveFiltering)

chunk.buildDenseCloud()

chunk.buildModel(surface_type=Metashape.HeightField, interpolation=Metashape.DisabledInterpolation, face_count=Metashape.HighFaceCount)

doc.save(path=project, chunks=[doc.chunk])

doc = Metashape.app.document
doc.open(project)
app = Metashape.Application()

# PhotoScan.app.cpu_enable = 8

chunk = doc.chunk
chunk.crs = Metashape.CoordinateSystem("EPSG::4326")

proj = Metashape.OrthoProjection()
proj.crs = Metashape.CoordinateSystem("EPSG::4326")

chunk.buildDem(source_data=Metashape.DataSource.DenseCloudData, interpolation=Metashape.Interpolation.DisabledInterpolation, projection=proj)

chunk.buildOrthomosaic(surface_data=Metashape.DataSource.ElevationData, blending_mode=Metashape.BlendingMode.MosaicBlending, projection=proj)

compr = Metashape.ImageCompression()
compr.tiff_compression = Metashape.ImageCompression.TiffCompressionNone
compr.tiff_big = False
compr.tiff_overviews = False
compr.tiff_tiled = False

chunk.exportRaster(path=dem, image_format=Metashape.ImageFormatTIFF, projection=proj, nodata_value=-9999, save_kml=False, save_world=False, image_compression=compr, white_background=False, source_data=Metashape.ElevationData)

chunk.exportRaster(path=orthomosaic, image_format=Metashape.ImageFormatTIFF, projection=proj, save_kml=False, save_world=False, image_compression=compr, white_background=False, source_data=Metashape.OrthomosaicData)

doc.save(path=project, chunks=[doc.chunk])