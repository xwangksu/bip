'''
Created on Apr 5, 2018

@author: Xu Wang
'''
import os
import argparse
import PhotoScan

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
args = vars(ap.parse_args())
workingPath = args["wpath"]
print("Working path is: %s" % workingPath)
srcImagePath = workingPath
project = workingPath+"\\ortho_dem_process.psx"

files = os.listdir(srcImagePath+"\\calibrated\\")
file_list=[]
for file in files:
    if file.endswith(".tif"):
        filePath = srcImagePath +"\\calibrated\\"+ file
        file_list.append(filePath)
app = PhotoScan.Application()
doc = PhotoScan.app.document

PhotoScan.app.gpu_mask = 1
# PhotoScan.app.cpu_enable = 8

chunk = PhotoScan.app.document.addChunk()
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")
# Import photos
chunk.addPhotos(file_list, PhotoScan.MultiplaneLayout)
chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.ReferencePreselection, keypoint_limit = 50000, tiepoint_limit = 30000)
# Align photos                 
chunk.alignCameras(adaptive_fitting=True)
# Save project
doc.save(path=project, chunks=[doc.chunk])
