from abaqus import *
from abaqusConstants import * 
import random

#全局变量
length=100
wieth=100
height=100
min_size = 1
max_size = 30
number = 30

#基底模型
myModel = mdb.models["Model-1"]
mysketch_1 = myModel.ConstrainedSketch(name='mysketch_1', sheetSize=200.0)
mysketch_1.rectangle(point1=(0.0,0.0),point2=(length,wieth))
myPart = myModel.Part(name='Part-Base', dimensionality=THREE_D, type=DEFORMABLE_BODY) 
myPart.BaseSolidExtrude(sketch=mysketch_1, depth=height)
del mysketch_1 

#交接判断
def interact(point,center):
    sign=True 
    radius2= point[3]
    for p in center:
        radius1= p[3]
        if sqrt((point[0]-p[0])**2+(point[1]-p[1])**2+(point[2]-p[2])**2) <= (radius1+radius2): 
            sign = False
            break 
    return sign

# random variables
center = []
i = 0
while i <number:
    radius = random.uniform(min_size, max_size) # size of guliao(aggregate)
    x = random.uniform(radius, length-radius) # x coordinate of round
    y = random.uniform(radius, wieth-radius) # y coordinate of round
    z = random.uniform(radius, height-radius) # y coordinate of round
    if len(center)==0:
        center.append([x, y, z, radius])
        i +=1
    elif interact([x, y, z, radius], center):
        center.append([x, y, z, radius])
        i +=1
    else:
        i = i

#基底集合
myAssembly =myModel.rootAssembly
myAssembly.Instance(name='Part-shixin', part = myModel.parts["Part-Base"], dependent=ON) 

#生成球
i = 0
instancess=[]
for each_center in center:
    x = each_center[0]
    y = each_center[1]
    z = each_center[2]
    radius = each_center[3]
    print(radius,"is nnn")
    mysketch_2 = myModel.ConstrainedSketch(name='mysketch_2', sheetSize=200.0) 
    mysketch_2.ConstructionLine(point1=(0.0,-100.0),point2=(0.0,100.0))
    curve = mysketch_2.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(radius, 0.0)) 
    mysketch_2.autoTrimCurve(curve1=curve,point1=(-radius,0.0))
    mysketch_2.Line(point1=(0.0,radius),point2=(0.0,-radius))
    myPart2 = myModel.Part(name="partName-{}".format(i), dimensionality=THREE_D,type=DEFORMABLE_BODY) 
    myPart2.BaseSolidRevolve(sketch=mysketch_2,angle=360.0,flipRevolveDirection=OFF) 
    del mysketch_2
    Instance=myAssembly.Instance(name='Part-Ball-{}'.format(i),part=myPart2, dependent=ON) 
    myAssembly.translate(instanceList=('Part-Ball-{}'.format(i),), vector=(x, y, z))
    instancess.append(Instance)
    i += 1

myAssembly.InstanceFromBooleanMerge(name='all_Ball', instances=instancess, originalInstances=DELETE, domain=GEOMETRY)

#切割1
myAssembly.InstanceFromBooleanCut(cuttingInstances=(myAssembly.instances['all_Ball-1'], ), instanceToBeCut=myAssembly.instances['Part-shixin']
    , name='base_Instance1', originalInstances=SUPPRESS)
myAssembly.features['all_Ball-1'].resume()
del myAssembly.features['Part-shixin']
