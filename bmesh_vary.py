# This assumes we have a mesh object selected

import bpy
import bmesh
import random

# How much variation do you want? One seems a good starting point, 5 is to much for a brick
degree = 5


# Get the active mesh
me = bpy.context.object.data


# Get a BMesh representation
bm = bmesh.new()   # create an empty BMesh
bm.from_mesh(me)   # fill it in from a Mesh

random.seed()


def vary():
    return random.randint(-50, 50) / 500 * degree


# Modify the BMesh, can do anything here...
for v in bm.verts:
    v.co.x += vary()
    v.co.y += vary()
    v.co.z += vary()


# Finish up, write the bmesh back to the mesh
bm.to_mesh(me)
bm.free()  # free and prevent further access
