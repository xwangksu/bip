'''
Created on Apr 5, 2018

@author: Xu Wang
'''
import os
import argparse
from datetime import datetime
import errno
import exiftool
import shutil
import numpy

#------------------------------------------------------------------------
# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("fpath", help="main file path")
args = parser.parse_args()
filePath = args.fpath
#------------------------------------------------------------------------
# Define the output LogFile
logFile = 'LogCheck_'+datetime.now().strftime("%y%m%d_%H%M%S")+'.txt'
logname = os.path.join(filePath,logFile)
with open(logname, 'a') as logoutput:
    logoutput.write("File path is: %s\n" % filePath)
print("File path is: %s" % filePath)
#------------------------------------------------------------------------
# Create list of total images
exten = '.tif'
imList=[]
for dirpath, dirnames, files in os.walk(filePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(os.path.join(dirpath, name))
with open(logname, 'a') as logoutput:
    logoutput.write("Total images in the path: %d\n" % len(imList))
print("Total images in the path: %d" % len(imList))
#------------------------------------------------------------------------
# Remove questionable images
# Round I: check image file size
print("R1 check")
r2List=[]
for im in imList:
    fs = os.path.getsize(im)
    if fs > 2000000:
        r2List.append(im)
# Round II: check completeness
print("R2 check")
imNum = 99999
acc = 0
tempImList=[]
finalImList=[]
questionImList=[]
for im in r2List:
    # Check 1-5
    imObj = im.split("\\")
    numOfObj = len(imObj)
    # Only image file name with no extension
    imNumNext = int(imObj[numOfObj-1].split("_")[1])
    if imNum != imNumNext:
        imNum = imNumNext
        if acc == 5:
            for i in range(0,acc):
                finalImList.append(tempImList[i])
        else:
            for i in range(0,acc):
                questionImList.append(tempImList[i])
        acc = 1
        tempImList.clear()
        tempImList.append(im)
    else:
        acc += 1
        tempImList.append(im)
if acc ==5:
    for i in range(0,5):
        finalImList.append(tempImList[i])
with open(logname, 'a') as logoutput:
    logoutput.write("Total effective images in the path: %d\n" % len(finalImList))
    logoutput.write(''.join(questionImList)+"\n")
print("Total effective images in the path: %d" % len(finalImList))
#------------------------------------------------------------------------
# Create renamed path
try:
    os.makedirs(filePath+"\\renamed")
    print("Creating Renamed directory.")
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
# Rename and copy into Renamed directory
alti = [] # altitude
with exiftool.ExifTool() as et:
    for im in finalImList:
        imObj = im.split("\\")
        numOfObj = len(imObj)
        imFile = imObj[numOfObj-1]
        dtTags = et.get_tag('EXIF:DateTimeOriginal',im)
        exifAlti = float(et.get_tag('GPS:GPSAltitude',im))
        if exifAlti > 0:
            alti.append(exifAlti)
        dtTags = ''.join(dtTags.split(":")).replace(" ","_")
        tgFile = filePath+"\\renamed\\"+dtTags+"_"+imFile
        newFile = shutil.copy2(im,tgFile)
        print("Copying %s" % newFile)
#------------------------------------------------------------------------
# Calculate altitude
alti_min = numpy.min(alti)
alti_mean = numpy.mean(alti)
alti_th = alti_min + 0.5*(alti_mean-alti_min)
with open(logname, 'a') as logoutput:
    logoutput.write("Altitude threshold: %.3f\n" % alti_th)
print("Altitude threshold: %.3f" % alti_th)
# Create low path
try:
    os.makedirs(filePath+"\\low_altitude")
    print("Creating LOW directory.")
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
renamedIm = os.listdir(filePath+"\\renamed")
blueIm = []
for im in renamedIm:
    if im.find("_1.tif") != -1:
        blueIm.append(im)
acc = 0
with exiftool.ExifTool() as et:
    for im in blueIm:
        alti = float(et.get_tag('GPS:GPSAltitude',filePath+"\\renamed\\"+im))
        if alti < alti_th:
            # Move to low directory
            newFile = shutil.move(filePath+"\\renamed\\"+im, filePath+"\\low_altitude\\"+im)
            print("Moving %s" % newFile)
            newFile = shutil.move(filePath+"\\renamed\\"+im.replace("_1.tif","_2.tif"), filePath+"\\low_altitude\\"+im.replace("_1.tif","_2.tif"))
            print("Moving %s" % newFile)
            newFile = shutil.move(filePath+"\\renamed\\"+im.replace("_1.tif","_3.tif"), filePath+"\\low_altitude\\"+im.replace("_1.tif","_3.tif"))
            print("Moving %s" % newFile)
            newFile = shutil.move(filePath+"\\renamed\\"+im.replace("_1.tif","_4.tif"), filePath+"\\low_altitude\\"+im.replace("_1.tif","_4.tif"))
            print("Moving %s" % newFile)
            newFile = shutil.move(filePath+"\\renamed\\"+im.replace("_1.tif","_5.tif"), filePath+"\\low_altitude\\"+im.replace("_1.tif","_5.tif"))
            print("Moving %s" % newFile)
            acc += 5
print("%d files moved to low_altitude" % acc)
with open(logname, 'a') as logoutput:
    logoutput.write("%d files moved to low_altitude\n" % acc)
#------------------------------------------------------------------------