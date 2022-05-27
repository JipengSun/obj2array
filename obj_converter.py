import numpy as np

data_path = './obj_data/'
output_folder = './output/'

#file_name = 'TeddyBear01-n.obj'
#file_name = 'bunny.obj'
#file_name = 'UtahTeapot01-n.obj'
#file_name = 'tyra.obj'
file_name = 'smooth_sphere.obj'


def normalize_CVV(vertexArray):
    va = np.array(vertexArray).astype(float)
    vb = (va-np.min(va))*2/(np.max(va)-np.min(va))-1
    # Concate w
    vc = np.concatenate((vb,np.ones((va.shape[0],1)).astype(float)),axis = 1)
    vc = vc.tolist()
    return vc

def add_surface_normal(final_vertex_array):
    vf = np.array(final_vertex_array).astype(float)
    #print(vf.shape)
    edge1 = vf[1::3] - vf[0::3]
    edge2 = vf[2::3] - vf[1::3]
    normal = np.cross(edge1[:,:3],edge2[:,:3])
    normal_norm = (normal.T/np.linalg.norm(normal,axis=1).T).T
    vn = np.repeat(normal_norm,3,axis=0)
    #print(vn.shape)
    vcn = np.concatenate((vf,vn),axis = 1)
    vcn = vcn.tolist()
    return vcn


# Reading .obj file
file1 = open(data_path+file_name, 'r')
Lines = file1.readlines()
count = 0
vertexArray = []
vertexIndexArray = []
for line in Lines:
    count += 1
    #print("Line{}: {}".format(count, line.strip()))
    if line[:2] == 'v ':
        vertex = line[2:].split()
        #vertex.append('1.0')
        vertexArray.append(vertex)
    if line[:2] == 'f ':
        vIndex = line[2:].split()
        if '/' in vIndex[0]:
            vIA = []
            for vI in vIndex:
                vTemp = vI.split('/')
                vIA.append(vTemp[0])
            vertexIndexArray.append(vIA)
        else:
            vertexIndexArray.append(vIndex)


file1.close()
#print(vertexArray)

assert len(vertexIndexArray)!=0, 'No Vertices Found in .obj File. Please Use A Valid One.'
va = normalize_CVV(vertexArray)
final_vertex_array = []

assert len(vertexIndexArray)!=0, 'Please Use An .obj File With Valid Surface Info.'
for idx,triangle in enumerate(vertexIndexArray):
    for i in range(3):
        final_vertex_array.append(va[int(triangle[i])-1])

vertex_normal_array = add_surface_normal(final_vertex_array)

with open(output_folder+'vertex_normal_array_output_'+file_name+'.txt', 'w') as f:
    for idx,vertex in enumerate(vertex_normal_array):
        f.write(','.join(str(x) for x in vertex))
        if idx < len(vertex_normal_array)-1:
            f.write(',\n')
f.close()

#print('Number of Vertices: '+str(len(vertex_normal_array)))

with open(output_folder+'vertex_array_output_'+file_name+'.txt', 'w') as f:
    for idx,vertex in enumerate(final_vertex_array):
        f.write(','.join(str(x) for x in vertex))
        if idx < len(final_vertex_array)-1:
            f.write(',\n')
f.close()

print('Number of Vertices: '+str(len(final_vertex_array)))