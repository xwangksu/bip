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

chunk.updateTransform()

chunk.optimizeCameras(fit_f=True, fit_cxcy=True, fit_b1=True, fit_b2=True, fit_k1k2k3=True, fit_p1p2=True)

doc.save(path=project, chunks=[doc.chunk])
