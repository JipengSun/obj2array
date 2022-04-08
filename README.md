# obj2array

## Project Explanation
Convert .obj file into JS vertex Float32Array for WebGL development. The generated vertex array contains scaled vertex coordinates in canonical viewing volume(CVV) and the normalized surface normal vector for each surface. This converter tool is developed by Jipeng Sun and Prof. Jack Tumblin from Northwestern University for CS351-1 Intro to Computer Graphics course.

https://www.mccormick.northwestern.edu/computer-science/academics/courses/descriptions/351-1.html

An .obj file defines an object shape by its vertices and its surface triangle vertices index sets. See more .obj format explanation from Wiki.

https://en.wikipedia.org/wiki/Wavefront_.obj_file

For a valid .obj file which contains vertices information and surfaces information, the obj2array will generate two types of vertex array data in .txt files under ./output directory. You can then simply copy and paste the vertex data from the txt file into your Float32Array in .js file. And it would display the shapes in .obj file in WebGL (Example WebGL display code provided in WebGL_Demo_Code directory.)

1. vertex_array_output.txt
A ( 4 , n ) vertex array which includes x,y,z,w position in CVV for all vertices.

2. vertex_normal_array_output.txt
A ( 7, n ) vertex array which includes x,y,z,w coordinate position in CVV for vertices plus 3 dimensioins for the surface normal vector (vx,vy,vz)

For WebGL vertex buffer and its pointer assignment, we need to know the several information from .obj file.

https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/vertexAttribPointer

```
void gl.vertexAttribPointer(index, size, type, normalized, stride, offset);
```

1. The meaning of a vertex unit structure (Offset)
2. The length of a vertex unit in vertex buffer array (Stride)
3. The overall number of vertices

The first two parts of the information are provided by the .txt file and the number of the vertices of the array is printed out in the terminal after running the .py file.

## Code Setup

### Install conda

We use conda to manage the environment. For conda installation, please refer to the official docs link.

https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

### Set Up Environment 
(Skip this step if you have already configured a numpy+jupyter python evironment)

After installing conda, running lines below will set up the environment for the obj2array. Please clone the repo first and run these commands under the root directory of the repo.
```


conda create --name WebGL python=3.9 --file requirements.txt

conda activate WebGL

```

### Run obj_converter.py

Example .obj file is provided under obj_data foler, you can put your own .obj file under obj_data folder.

Simply set the file_name variable to your .obj file name in Line 6 (default is the Teddy Bear one) and use python to run obj_converter.py. It will return two .txt files under ./output folder and output the vertices number in the terminal.

If you prefer to use jupyter to see the process, we also provide jupyter notebook. Please run obj_test.ipynb

### Modify WebGL Code
Depends on your application, copy that vertex array txt info and assign it to your WebGL vertex array. Please make sure to also change the vertices number information. Two example WebGl code are provided under ./WebGL_Demo_Code folder. 



2.00.DotsAndLine will show object vertices by dots and lines using the vertex_array_output.txt. An expected output scene would be

![Dots And Line](https://github.com/JipengSun/obj2array/blob/main/readme_imgs/dots_lines.png)

ColoeredMultiObj will show object vertices and surfaces using the vertex_normal_array_output.txt. It is spinning and the spin speed can be controlled by the button.

![Spinning Surface 1](https://github.com/JipengSun/obj2array/blob/main/readme_imgs/spining_bear_1.png)


![Spinning Surface 2](https://github.com/JipengSun/obj2array/blob/main/readme_imgs/spining_bear_2.png)

![Spinning Surface 3](https://github.com/JipengSun/obj2array/blob/main/readme_imgs/bunny_1.png)

![Spinning Surface 4](https://github.com/JipengSun/obj2array/blob/main/readme_imgs/bunny_2.png)

![Spinning Surface 5](https://github.com/JipengSun/obj2array/blob/main/readme_imgs/teapot_1.png)

![Spinning Surface 6](https://github.com/JipengSun/obj2array/blob/main/readme_imgs/teapot_1.png)