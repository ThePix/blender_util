# https://docs.blender.org/api/current/info_quickstart.html

# To see error messages:
# Windows - Toggle System Console

import bpy
import bmesh
import random
import math
from mathutils import Matrix


print("Starting...")




gap = 0.05          # gap between slates
scale = 0.01        # How much every vertex is varied
slate_length = 1.2  # slate dimension
slate_width = 0.6
slate_depth = 0.4
step_depth = 0.07   # each row rises by this
randomness = 5      # 1 in this tiles will be shorter


def slate_roof(x_offset, y_offset, z_offset, length, height):
    z = 0

    for c in range(0, height):
        y = c * (slate_length / 2)
        z += step_depth
        x = 0 if c % 2 == 0 else (slate_width + gap) / 2
        while x < length:
            #x += slate_width
            #print(x)
            y_bonus = random.random() / 5 if random.randint(1, randomness) == 1 else 0
            print(y_bonus)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x + x_offset, y + y_offset + y_bonus, z + z_offset))
            cube = bpy.context.object
            S = Matrix.Diagonal((slate_width, slate_length, slate_depth)).to_4x4()
            cube.data.transform(S)
            for v in cube.data.vertices:
                v.co.x += scale * (random.random() - random.random())
                v.co.y += scale * (random.random() - random.random())
                v.co.z += scale * (random.random() - random.random())
            cube.data.update()
            x += slate_width + gap

    #bpy.ops.mesh.primitive_cube_add(size=2, location=(x_offset +length / 2, y_offset, height - 1 - gap / 2 + z_offset))
    #cube = bpy.context.object
    #S = Matrix.Diagonal((length / 2, 0.6, height * (1 + gap))).to_4x4()
    #cube.data.transform(S)
    #cube.data.update()









slate_roof( 25, 15, 10, 4, 8)


print("... Done")

