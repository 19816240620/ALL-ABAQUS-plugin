from abaqus import *
from abaqusConstants import *
from scipy.spatial import *
import numpy as np
import random

iii=0
if iii == 0:
    length = 100
    width = 100
    height =100
    point = 20
    ex = 3
    size = max(length, width, height)
    point_number = 4*point
    points = np.array([[random.uniform(0,length*ex),random.uniform(0,width*ex),random.uniform(0,height*ex)] for i in range(point_number)])
    vor = Voronoi(points)
    vertices = vor.vertices
    edges = vor.ridge_vertices
    for edge in edges:
        for number in edge:
            if number !=-1 :
                for coord in vertices[number]:
                    if coord >= size*10 or coord <= -size*10:
                        edges[edges.index(edge)].append(-1)
                        break
    face_points = []
    for edge in np.array(edges):
        edge = np.array(edge)
        temp = []
        if np.all(edge >= 0):
                for i in edge:
                    temp.append(tuple(vertices[i]))
                temp.append(vertices[edge[0]])
        if (len(temp)>0):
            face_points.append(temp)
    myModel = mdb.models['Model-1']
    myPart = myModel.Part(name='Part-vor3', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    for i in range(len(face_points)):
        wire = myPart.WirePolyLine(mergeType=SEPARATE, meshable=ON, points=(face_points[i]))
        face_edge = myPart.getFeatureEdges(name=wire.name)
        myPart.CoverEdges(edgeList = face_edge, tryAnalytical=True)
    faces = myPart.faces[:]
    myPart.AddCells(faceList = faces)
    myPart2 = myModel.Part(name='Part-core', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    mySketch2 = myModel.ConstrainedSketch(name="mysketch-2",sheetSize = 200)
    mySketch2.rectangle(point1=(0,0), point2=(length,width))
    myPart2.BaseSolidExtrude(sketch=mySketch2, depth=height)
    myPart3 = myModel.Part(name='Part-base', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    mySketch3 = myModel.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mySketch3.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    curve = mySketch3.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(size*10,0.0))
    mySketch3.Line(point1=(0.0, 10*size), point2=(0.0, -10*size))
    mySketch3.autoTrimCurve(curve1=curve, point1=(-size*10,0.0))
    myPart3.BaseSolidRevolve(sketch=mySketch3, angle=360.0, flipRevolveDirection=OFF)
    myAssembly = myModel.rootAssembly
    myAssembly.Instance(name='Part-base-1', part=myModel.parts["Part-base"], dependent=ON)
    myAssembly.Instance(name='Part-core-1', part=myModel.parts["Part-core"], dependent=ON)
    myAssembly.translate(instanceList=('Part-core-1', ), vector=(size*(ex-1)/2,size*(ex-1)/2,size*(ex-1)/2))
    myAssembly.InstanceFromBooleanCut(name='Part-base-cut',instanceToBeCut=myAssembly.instances['Part-base-1'],
                                      cuttingInstances=(myAssembly.instances['Part-core-1'], ), originalInstances=SUPPRESS)
    mdb.models['Model-1'].rootAssembly.features['Part-core-1'].resume()
    myAssembly.Instance(name='Part-cut-1', part=myModel.parts["Part-base-cut"], dependent=ON)
    myAssembly.Instance(name='Part-vor3-1', part=myModel.parts["Part-vor3"], dependent=ON)
    in2=myAssembly.InstanceFromBooleanCut(name='Part-vor3-cut',instanceToBeCut=myAssembly.instances['Part-vor3-1'],
                                  cuttingInstances=(myAssembly.instances['Part-cut-1'], ), originalInstances=DELETE)
    in1=myAssembly.InstanceFromBooleanCut(name='Part-Vor3_tianbu',instanceToBeCut=myAssembly.instances['Part-core-1'],
                                      cuttingInstances=(myAssembly.instances['Part-vor3-cut-1'], ), originalInstances=SUPPRESS)
    mdb.models['Model-1'].rootAssembly.features['Part-vor3-cut-1'].resume()
    All_Vor3 = myAssembly.InstanceFromBooleanMerge(name='all_Vor3', instances=(in1,in2),keepIntersections=ON,originalInstances=DELETE, domain=GEOMETRY)
    for key in myAssembly.instances.keys():
        del myAssembly.instances[key]
    for key in myModel.parts.keys():
        if key != "all_Vor3":
            del myModel.parts[key]
    myPart = mdb.models['Model-1'].parts['all_Vor3']
    for i in range(len(myPart.cells)):
        region = myPart.Set(cells = myPart.cells[i:i+1],name = "Set-{}".format(i))
