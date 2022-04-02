# obj_converter
Convert .obj file for WebGL development

This .obj file converter is to read .obj vertices info for WebGL development.

For WebGL vertex buffer and its pointer assignment, we need to know the several information from .obj file.

https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/vertexAttribPointer

```
void gl.vertexAttribPointer(index, size, type, normalized, stride, offset);
```

1. The meaning of a vertex unit structure (Offset)
2. The length of a vertex unit in vertex buffer array (Stride)

```
conda create --name OpenGL python=3.9 --file requirements.txt

conda activate OpenGL

```