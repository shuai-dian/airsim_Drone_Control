# In settings.json first activate computer vision mode:
# https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode
import setup_path
import airsim
import cv2
import time
import sys
import numpy as np
import airsim  # pip install airsim
import os
# # for car use CarClient()
client = airsim.MultirotorClient()

cameraType = "scene"

for arg in sys.argv[1:]:
  cameraType = arg.lower()

cameraTypeMap = {
 "depth": airsim.ImageType.DepthVis,
 "segmentation": airsim.ImageType.Segmentation,
 "seg": airsim.ImageType.Segmentation,
 "scene": airsim.ImageType.Scene,
 "disparity": airsim.ImageType.DisparityNormalized,
 "normals": airsim.ImageType.SurfaceNormals
}

if (cameraType not in cameraTypeMap):
    print("Usage: python camera.py [depth|segmentation|scene]")
    sys.exit(0)

print (cameraTypeMap[cameraType])

client = airsim.MultirotorClient()
help = False
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
thickness = 2
textSize, baseline = cv2.getTextSize("FPS", fontFace, fontScale, thickness)
textOrg = (10, 10 + textSize[1])
frameCount = 0
startTime = time.time()
fps = 0

while True:
    # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
    rawImage = client.simGetImage("1", cameraTypeMap[cameraType])
    if (rawImage == None):
        print("Camera is not returning image, please check airsim for error messages")
        sys.exit(0)
    else:
        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
        cv2.putText(png,'FPS ' + str(fps),textOrg, fontFace, fontScale,(255,0,255),thickness)
        cv2.imshow("Depth", png)

    frameCount = frameCount  + 1
    endTime = time.time()
    diff = endTime - startTime
    if (diff > 1):
        fps = frameCount
        frameCount = 0
        startTime = endTime

    key = cv2.waitKey(1) & 0xFF
    if (key == 27 or key == ord('q') or key == ord('x')):
        break
