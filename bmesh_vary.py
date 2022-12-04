# Copyright 2022 Andy Joel

# Select an object, then run this script.
# Each vertice will be moved a small, random amount, giving brickwork, etc. a more realistic look.
# Save before using, just in case, but if you do not like the results just do [CTRL]-Z
# Change the value of degree to control the amount of variation.
# 2 is going to be quite significant, and seems a good starting point so you can see it works
# 5 is probably too much, remember you can use decimal values, so try 0.2.

import bpy
import bmesh
import random

# Change the number here to control how much variation there will be.
degree = 2


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
