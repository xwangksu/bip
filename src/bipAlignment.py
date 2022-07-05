'''
Created on May 9, 2022

@author: Xu Wang
'''
import os
import argparse
import Metashape

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-wp", "--wpath", required=True, help="workingPath")
args = vars(ap.parse_args())
workingPath = args["wpath"]
print("Working path is: %s" % workingPath)
srcImagePath = workingPath
project = workingPath+"\\ortho_dem_process.psx"


files = os.listdir(srcImagePath+"\\renamed\\")
file_list=[]

for file in files:
    if file.endswith(".tif"):
        filePath = srcImagePath +"\\renamed\\"+ file
        file_list.append(filePath)

fileGroups = [5]*(len(file_list)//5)

app = Metashape.Application()
doc = Metashape.app.document

# PhotoScan.app.console.clear()

Metashape.app.gpu_mask = 3
Metashape.app.cpu_enable = True

chunk = Metashape.app.document.addChunk()
chunk.crs = Metashape.CoordinateSystem("EPSG::4326")

doc.save(path=project, chunks=[doc.chunk])


# Import photos
chunk.addPhotos(filenames = file_list, filegroups = fileGroups, layout = Metashape.MultiplaneLayout)

chunk.locateReflectancePanels()

# Panel info
albedo = {"Blue": "0.489", "Green": "0.490", "Red": "0.489", "NIR": "0.488", "Red edge": "0.486"}
for sensor in chunk.sensors:
    sensor.normalize_sensitivity = True
for camera in chunk.cameras:
    if camera.group and camera.group.label == "Calibration images":
        for plane in camera.planes:
            plane.meta["ReflectancePanel/Calibration"] = albedo[plane.sensor.bands[0]]
chunk.calibrateReflectance(use_reflectance_panels=True, use_sun_sensor=True)
doc.save(path=project, chunks=[doc.chunk])

chunk.matchPhotos(downscale=1, reference_preselection=True, keypoint_limit = 15000, tiepoint_limit = 8000)
# Align photos
chunk.alignCameras(adaptive_fitting=True)
# Save project
doc.save(path=project, chunks=[doc.chunk])
