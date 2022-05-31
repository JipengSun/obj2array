# obj_converter by Jipeng Sun
# Modified by Felipe Caldeira

import numpy as np
import sys, os
from collections import defaultdict

data_path = './obj_data/'
output_folder = './output/'

file_name = sys.argv[1] + '.obj'

def normalize_CVV(vertexArray):
    va = np.array(vertexArray).astype(float)
    vb = (va-np.min(va))*2/(np.max(va)-np.min(va))-1
    # Concate w
    vc = np.concatenate((vb,np.ones((va.shape[0],1)).astype(float)),axis = 1)
    vc = vc.tolist()
    return vc

def add_surface_normal(final_vertex_array):
    vf = np.array(final_vertex_array).astype(float)
    edge1 = vf[1::3] - vf[0::3]
    edge2 = vf[2::3] - vf[1::3]
    normal = np.cross(edge1[:,:3],edge2[:,:3])
    normal_norm = (normal.T/np.linalg.norm(normal,axis=1).T).T
    normal_norm = np.nan_to_num(normal_norm)
    vn = np.repeat(normal_norm,3,axis=0)
    vcn = np.concatenate((vf,vn),axis = 1)
    vcn = vcn.tolist()
    return vcn

def add_vertex_normal(final_vertex_array, vertexIndexArray, vertexNormalsDict):
    vertIdx = 0
    vcn = []
    for triangle in vertexIndexArray:
        for i in range(3):
            normals = [x[0] for x in vertexNormalsDict[triangle[i]]]
            angles = [x[1] for x in vertexNormalsDict[triangle[i]]]
            weights = [x / sum(angles) for x in angles]

            vertexNormal = np.average(normals, weights=weights, axis=0)
            vertexNormal = list(vertexNormal / np.linalg.norm(vertexNormal))
            vcn.append(final_vertex_array[vertIdx] + vertexNormal)
            vertIdx += 1
    return vcn

# Get angle formed by verts abc
def getAngle(a, b, c):
    return getAngle2(a-b, c-b)

# Get angle between vectors A and B
def getAngle2(A, B):
    angle = abs(np.arccos(np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))) )
    return angle if not np.isnan(angle) else 0

# Reading .obj file
file1 = open(data_path+file_name, 'r')
Lines = file1.readlines()
count = 0
vertexArray = []
vertexIndexArray = []
vertexNormalsDict = defaultdict(list)
for line in Lines:
    count += 1
    if line[:2] == 'v ':
        vertex = line[2:].split()
        vertexArray.append(vertex)
    if line[:2] == 'f ':
        vIndex = line[2:].split()
        vertexIndexArray.append(vIndex)


file1.close()
#print(vertexArray)

assert len(vertexIndexArray)!=0, 'No Vertices Found in .obj File. Please Use A Valid One.'
va = normalize_CVV(vertexArray)
final_vertex_array = []

assert len(vertexIndexArray)!=0, 'Please Use An .obj File With Valid Surface Info.'
for idx,triangle in enumerate(vertexIndexArray):
    v0 = np.array(va[int(triangle[0])-1][:-1])
    v1 = np.array(va[int(triangle[1])-1][:-1])
    v2 = np.array(va[int(triangle[2])-1][:-1])

    triangleNorm = np.cross(v1 - v0, v2 - v1) 
    triangleNorm = list(np.nan_to_num(triangleNorm / np.linalg.norm(triangleNorm)))

    angles = []
    angles.append(getAngle(v1, v0, v2)) 
    angles.append(getAngle(v0, v1, v2)) 
    angles.append(getAngle(v0, v2, v1)) 

    for i in range(3):
        vertexNormalsDict[triangle[i]].append((triangleNorm, angles[i]))
        final_vertex_array.append(va[int(triangle[i])-1])

# Create output folder
output_path = './'+output_folder+file_name[:-4]
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Array with hard normals (per surface)
vertex_normal_array = add_surface_normal(final_vertex_array)
with open(output_path+'/array_hard_normals.txt', 'w') as f:
    for idx,vertex in enumerate(vertex_normal_array):
        f.write(','.join(str(x) for x in vertex))
        if idx < len(vertex_normal_array)-1:
            f.write(',\n')
f.close()

# Array with soft (smooth) normals (per vertex, avg of adjacent surfaces)
vertex_normal_array_soft = add_vertex_normal(final_vertex_array, vertexIndexArray, vertexNormalsDict)
with open(output_path+'/array_soft_normals.txt', 'w') as f:
    for idx,vertex in enumerate(vertex_normal_array_soft):
        f.write(','.join(str(x) for x in vertex))
        if idx < len(vertex_normal_array_soft)-1:
            f.write(',\n')
f.close()

# Array with no normals
with open(output_path+'/array.txt', 'w') as f:
    for idx,vertex in enumerate(final_vertex_array):
        f.write(','.join(str(x) for x in vertex))
        if idx < len(final_vertex_array)-1:
            f.write(',\n')
f.close()

print('Number of Vertices: '+str(len(final_vertex_array)))