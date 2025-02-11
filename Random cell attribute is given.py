from abaqus import *
from abaqusConstants import *
from scipy.spatial import *
import numpy as np
import random
import math
import itertools
from numpy import pi,sin,cos,arccos

def gude(part_name,properties_number,area):
    part_k=mdb.models['Model-1'].parts[part_name].PartFromMesh(copySets=True, name=
        '{}-mesh_part'.format(part_name))
    ele = part_k.elements
    nu = 0
    for el in ele:
        nu+=1
    nu1 = list(range(0, nu))
    po = list(range(1,properties_number+1))
    i = 0
    while i < nu:
        pii = int(random.choice(nu1))
        pop = int(random.choice(po))
        nu1.remove(pii)
        if (True):
            elele = mdb.models['Model-1'].parts['{}-mesh_part'.format(part_name)].elements[pii]
            node = elele.getNodes()
            if len(node)!=0:
                x = node[0].coordinates[0]
                y = node[0].coordinates[1]
                z = node[0].coordinates[2]
                if eval(area):
                    set_N = 'Set-{}'.format(i)
                    mdb.models['Model-1'].parts['{}-mesh_part'.format(part_name)].Set(elements=mdb.models['Model-1'].parts['{}-mesh_part'.format(part_name)].elements[pii:pii+1], name=set_N)
                    mdb.models['Model-1'].parts['{}-mesh_part'.format(part_name)].SectionAssignment(region=mdb.models['Model-1'].parts['{}-mesh_part'.format(part_name)].sets[set_N], sectionName='Section-{}'.format(pop), offset=0.0,offsetType=MIDDLE_SURFACE, offsetField='',thicknessAssignment=FROM_SECTION)
                    print (i,"/",nu,"number has been del")
                    i+=1

gude('Part-1',4,'z>=0')
