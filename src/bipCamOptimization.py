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
Metashape.app.cpu_enable = False

chunk = doc.chunk
chunk.crs = Metashape.CoordinateSystem("EPSG::4326")

chunk.updateTransform()

chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=True, fit_b2=True, fit_k1=True, fit_k2=True, fit_k3=True, fit_p1=True, fit_p2=True)

doc.save(path=project, chunks=[doc.chunk])
