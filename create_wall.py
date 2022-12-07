# Copyright 2022 Andy Joel


import bpy
import bmesh
import random
import math
from mathutils import Matrix


print("Starting...")


#how many cubes you want to add
height = 8    # in bricks
length = 50   # in bricks
gap = 0.2
y = 0
scale = 0.0   # How much the bricks vary




def stone_wall(x_offset, y_offset, z_offset, length, height):

    for c in range(0,height):
        z = c * (2 + gap)
        x = 0
        while x < length:
            width = (length - x) / 2 if (2 + x > length) else 0.5 + random.random()
        #    width = 0.5 + random.random()
            x += width
            #print(x)
            bpy.ops.mesh.primitive_cube_add(size=2, location=(x + x_offset, y + y_offset, z + z_offset))
            cube = bpy.context.object
            S = Matrix.Diagonal((width, 1, 1)).to_4x4()
            cube.data.transform(S)
            for v in cube.data.vertices:
                v.co.x += scale * (random.random() - random.random())
                v.co.y += scale * (random.random() - random.random())
                v.co.z += scale * (random.random() - random.random())
            cube.data.update()
            x += width + gap
            
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x_offset +length / 2, y_offset, height - 1 - gap / 2 + z_offset))
    cube = bpy.context.object
    S = Matrix.Diagonal((length / 2, 0.6, height * (1 + gap))).to_4x4()
    cube.data.transform(S)
    cube.data.update()



def brick_wall(x_offset, y_offset, z_offset, length, height):
    length = length * (4 + gap)

    width = 2
    for c in range(0,height):
        z = c * (2 + gap)
        x = 0 if c % 2 == 0 else (width + gap)
        while x < length:
            x += width
            #print(x)
            bpy.ops.mesh.primitive_cube_add(size=2, location=(x + x_offset, y + y_offset, z + z_offset))
            cube = bpy.context.object
            S = Matrix.Diagonal((width, 1, 1)).to_4x4()
            cube.data.transform(S)
            for v in cube.data.vertices:
                v.co.x += scale * (random.random() - random.random())
                v.co.y += scale * (random.random() - random.random())
                v.co.z += scale * (random.random() - random.random())
            cube.data.update()
            x += width + gap

    bpy.ops.mesh.primitive_cube_add(size=2, location=(x_offset +length / 2, y_offset, height - 1 - gap / 2 + z_offset))
    cube = bpy.context.object
    S = Matrix.Diagonal((length / 2, 0.6, height * (1 + gap))).to_4x4()
    cube.data.transform(S)
    cube.data.update()






def english_bond(x_offset, y_offset, z_offset, length, height):
    length = length * (4 + gap)

    for c in range(0,height):
        if c % 2 == 0:
            w = 2
            x = 0
        else:
            w = 1 - gap / 4
            x = w + gap / 2
        z = c * (2 + gap)
        while x < length:
            x += w
            print(x)
            bpy.ops.mesh.primitive_cube_add(size=2, location=(x + x_offset, y + y_offset, z + z_offset))
            cube = bpy.context.object
            S = Matrix.Diagonal((w, 1, 1)).to_4x4()
            cube.data.transform(S)
            for v in cube.data.vertices:
                v.co.x += scale * (random.random() - random.random())
                v.co.y += scale * (random.random() - random.random())
                v.co.z += scale * (random.random() - random.random())
            cube.data.update()
            x += w + gap

    bpy.ops.mesh.primitive_cube_add(size=2, location=(x_offset +length / 2, y_offset, height - 1 - gap / 2 + z_offset))
    cube = bpy.context.object
    S = Matrix.Diagonal((length / 2, 0.6, height * (1 + gap))).to_4x4()
    cube.data.transform(S)
    cube.data.update()



def flemish_bond(x_offset, y_offset, z_offset, length, height):
    length = length * (4 + gap)

    for c in range(0,height):
        if c % 2 == 0:
            x = 0
        else:
            x = 1 + gap / 2
        z = c * (2 + gap)
        count = 0
        while x < length:
            if (c + count) % 2 == 0:
                w = 2
            else:
                w = 1 - gap / 4
            x += w
            count += 1
            print(x)
            bpy.ops.mesh.primitive_cube_add(size=2, location=(x + x_offset, y + y_offset, z + z_offset))
            cube = bpy.context.object
            S = Matrix.Diagonal((w, 1, 1)).to_4x4()
            cube.data.transform(S)
            for v in cube.data.vertices:
                v.co.x += scale * (random.random() - random.random())
                v.co.y += scale * (random.random() - random.random())
                v.co.z += scale * (random.random() - random.random())
            cube.data.update()
            x += w + gap

    bpy.ops.mesh.primitive_cube_add(size=2, location=(x_offset +length / 2, y_offset, height - 1 - gap / 2 + z_offset))
    cube = bpy.context.object
    S = Matrix.Diagonal((length / 2, 0.6, height * (1 + gap))).to_4x4()
    cube.data.transform(S)
    cube.data.update()





flemish_bond( 5, 15, 10, 4, 8)
#stone_wall(10, 10, 10, 20, 4)
#stone_wall(15, 10, 10, 20, 1)

