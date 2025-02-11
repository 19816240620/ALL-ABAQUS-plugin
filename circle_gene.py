from abaqus import *
from abaqusConstants import *
import random

# initial variables
length = 100 # length of base
width = 50 # width of base
number = 1000
minsize = 0.5
maxsize = 3
if mdb.models.has_key("Model-1"):
    myModel = mdb.models["Model-1"]
else:
    myModel = mdb.Model(name="Model-1",modelType=STANDARD_EXPLICIT)

#生成基体
mySketch = myModel.ConstrainedSketch(name="sketch-1", sheetSize=2000)
myPart = myModel.Part(name="part-base", dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
mySketch.rectangle(point1=(0, 0), point2=(length, width))
myPart.BaseShell(sketch=mySketch)

# 交接函数
def interact(center, round):
    sign = True
    for each_center in center:
        if (round[0]-each_center[0])**2+(round[1]-each_center[1])**2 - (each_center[2]+round[2])**2 <= 0:
            sign = False
            break
    return sign

# random variables
mySketch2 = myModel.ConstrainedSketch(name="sketch-partition", sheetSize=200)
center = []
for i in range(number):
    radius = random.uniform(minsize, maxsize) # size of guliao(aggregate)
    x = random.uniform(radius, length-radius) # x coordinate of round
    y = random.uniform(radius, width-radius) # y coordinate of round
    if len(center)==0:
        center.append([x, y, radius])
    elif interact(center, [x, y, radius]):
        center.append([x, y, radius])
    else:
        pass

#生成随机半径圆
for each_center in center:
    x = each_center[0]
    y = each_center[1]
    radius = each_center[2]
    mySketch2.CircleByCenterPerimeter(center=(x, y), point1=(x+radius, y))

#
myPart.PartitionFaceBySketch(faces=myPart.faces[:], sketch=mySketch2)



