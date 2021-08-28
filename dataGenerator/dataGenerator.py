import os
import json
import xmltodict
import cv2
import numpy as np
import random
from datetime import datetime
from hash import *
from PIL import Image

dir = 'images/XML/'
imgPath = 'images/'
outputImagePath = "generatedImages/"

classes = ['Square', 'Rectanlge', 'Parallelogram', 'Trapezium',
           'Right Angle Triangle', 'Equilateral Triangle', 'Isosceles Triangle',
           'Scalene Triangle', 'Rhombus', '', 'Cube',
           'Cuboid', 'Cylinder', 'Cone', 'Hemisphere']

usedClass = []
Hash = HashTable()


def dataGenerator(dir, cls):

    bndBox, files = [], []
    for file in os.listdir(dir):
        with open(dir+file, 'rb') as f:
            data_dict = xmltodict.parse(f.read())
        f.close()
        json_data = json.dumps(data_dict)

        jsonData = json.loads(json_data)
        for i in jsonData['annotation']['object']:
            if i['name'] in cls:
                files.append(file.replace("xml","jpg"))
                bndBox.append(i['bndbox'])

    return bndBox, files


def getRandomClass():

    clss = []

    i = 0
    while i < 5:
        num = random.randint(0, 14)
        if classes[num] not in usedClass:
            if classes[num] != '':
                if classes[num] not in clss:
                    clss.append(classes[num])
                    i += 1

    for cl in clss:

        if Hash[cl] == 30:
            usedClass.append(cl)
            clss.remove(cl)
            i = 0
            while i < 1:
                num = random.randint(0, 14)
                if classes[num] not in usedClass:
                    if classes[num] != '':
                        if classes[num] not in clss:
                            clss.append(classes[num])
                            i += 1
        else:
            Hash[cl] = 1

        print(f"{cl} used total {Hash[cl]} times")

    return clss


def checkOverLap(R1, R2):
      if (R1[0]>=R2[2]) or (R1[2]<=R2[0]) or (R1[3]<=R2[1]) or (R1[1]>=R2[3]):
         return True
      else:
         return False


for i in range(420):

    cls = getRandomClass()
    boxes, files = dataGenerator(dir, cls)

    blank_image = np.zeros((4160, 3120, 3), np.uint8)
    blank_image[:, :] = (255, 255, 255)
    fileName = "image_" + str(int(datetime.now().timestamp())) + ".jpg"
    cv2.imwrite(outputImagePath + fileName, blank_image)
    blankImage = Image.open(outputImagePath + fileName)
    myCoordinates = []

    for i in range(len(boxes)):

        xMin = int(boxes[i]['xmin'])
        yMin = int(boxes[i]['ymin'])
        xMax = int(boxes[i]['xmax'])
        yMax = int(boxes[i]['ymax'])
        width = xMax - xMin
        height = yMax - yMin

        image = Image.open(os.path.join(imgPath + files[i]))
        croppedImage = image.crop((xMin, yMin, xMax, yMax))

        myCoordinates.append([xMin, yMin, width, height])

        if len(myCoordinates) == 2:
            if checkOverLap(myCoordinates[0], myCoordinates[1]):
                blankImage.paste(croppedImage.resize((int(croppedImage.size[0]), int(croppedImage.size[1]))), (xMin, yMin))
            myCoordinates.pop(0)
        else:
            blankImage.paste(croppedImage.resize((int(croppedImage.size[0]), int(croppedImage.size[1]))), (xMin, yMin))

    blankImage.save(outputImagePath + fileName)
    print("userClass ==> ", usedClass)
    
    if i == 20:
        print("break")
        break