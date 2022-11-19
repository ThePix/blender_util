# https://docs.blender.org/api/current/info_quickstart.html

# To see error messages:
# Windows - Toggle System Console

import bpy
import bmesh
import random
import math
from mathutils import Matrix


print("Starting...")


#how many cubes you want to add
height = 8    # in bricks
length = 50   # in Blender units
gap = 0.2
y = 0
scale = 0.1




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
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x_offset +length / 2, y_offset, height * (1 + scale) - 1 - gap / 2 + z_offset))
    cube = bpy.context.object
    S = Matrix.Diagonal((length / 2, 0.6, height * (1 + scale))).to_4x4()
    cube.data.transform(S)
    cube.data.update()



stone_wall( 5, 15, 10, 10, 8)
#stone_wall(10, 10, 10, 20, 4)
#stone_wall(15, 10, 10, 20, 1)



def stone_arch(x_offset, y_offset, z_offset, radius, angle_of_arch, stone_depth, stone_height, stone_count, gap_angle = 0.1, bevel = True, keystone = 1.2, pentagons = True):
    # make collection
    new_collection = bpy.data.collections.new('new_collection')
    bpy.context.scene.collection.children.link(new_collection)

    # add object to scene collection
    for n in range(-stone_count, stone_count + 1):
    #for n in range(0, 1):
        new_collection.objects.link(stone_arch_stone(n, x_offset, y_offset, z_offset, radius, angle_of_arch, stone_depth, stone_height, stone_count, gap_angle, bevel, keystone, pentagons))


def stone_arch_stone(n, x_offset, y_offset, z_offset, radius, angle_of_arch, stone_depth, stone_height, stone_count, gap_angle, bevel, keystone, pentagons):
    bevel_angle = 1
    bevel_amount = 0.1
    #stone_angle = math.radians(n * angle_of_arch / stone_count)
    stone_angle_left = math.radians((n - 0.5) * angle_of_arch / stone_count + gap_angle / 2)
    stone_angle_left_bevel = math.radians((n - 0.5) * angle_of_arch / stone_count + gap_angle / 2 + bevel_angle)
    stone_angle_right = math.radians((n + 0.5) * angle_of_arch / stone_count - gap_angle / 2)
    stone_angle_right_bevel = math.radians((n + 0.5) * angle_of_arch / stone_count - gap_angle / 2 - bevel_angle)
    height = stone_height * keystone if n == 0 else stone_height
    
    # make mesh
    vertices = [
        ( x_offset + radius * math.sin(stone_angle_left), z_offset + radius * math.cos(stone_angle_left)),
        ( x_offset + (radius + height) * math.sin(stone_angle_left), z_offset + (radius + height) * math.cos(stone_angle_left)),
    ]
    if n < 0 and pentagons:
        vertices.append(( x_offset + (radius + height) * math.sin(stone_angle_left), z_offset + (radius + height) * math.cos(stone_angle_right)))
    elif n > 0 and pentagons:
        vertices.append(( x_offset + (radius + height) * math.sin(stone_angle_right), z_offset + (radius + height) * math.cos(stone_angle_left)))
    vertices.append(( x_offset + (radius + height) * math.sin(stone_angle_right), z_offset + (radius + height) * math.cos(stone_angle_right)))
    vertices.append(( x_offset + radius * math.sin(stone_angle_right), z_offset + radius * math.cos(stone_angle_right)))

    if bevel:
        bevel_vertices = [
            ( x_offset + (radius + bevel_amount) * math.sin(stone_angle_left_bevel), z_offset + (radius + bevel_amount) * math.cos(stone_angle_left_bevel)),
            ( x_offset + (radius + height - bevel_amount) * math.sin(stone_angle_left_bevel), z_offset + (radius + height - bevel_amount) * math.cos(stone_angle_left_bevel)),
        ]
        if n < 0 and pentagons:
            bevel_vertices.append(( x_offset + (radius + height - bevel_amount) * math.sin(stone_angle_left), z_offset + (radius + height - bevel_amount) * math.cos(stone_angle_right_bevel)))
        elif n > 0 and pentagons:
            bevel_vertices.append(( x_offset + (radius + height - bevel_amount) * math.sin(stone_angle_right_bevel), z_offset + (radius + height - bevel_amount) * math.cos(stone_angle_left_bevel)))
        bevel_vertices.append(( x_offset + (radius + height - bevel_amount) * math.sin(stone_angle_right_bevel), z_offset + (radius + height - bevel_amount) * math.cos(stone_angle_right_bevel)))
        bevel_vertices.append(( x_offset + (radius + bevel_amount) * math.sin(stone_angle_right_bevel), z_offset + (radius + bevel_amount) * math.cos(stone_angle_right_bevel)))
        new_mesh = generate_bevelled_mesh(vertices, bevel_vertices, y_offset, stone_depth)
    else:
        new_mesh = generate_mesh(vertices, y_offset, stone_depth)
        
    # make object from mesh
    new_object = bpy.data.objects.new('new_object', new_mesh)
    return new_object


# This will create the mesh for a block with the given coordinates in the x and z plane, with the give y coordinate and y depth
def generate_mesh(coords, y, depth):
    #print(coords)
    count = len(coords)
    vertices = []
    edges = []
    faces = []
    front_face = []
    back_face = []
    
    for i, el in enumerate(coords):
        vertices.append([el[0], y, el[1]])
        edges.append([i, 0 if i == count - 1 else i+1])
        front_face.append(i)
    for i, el in enumerate(coords):
        vertices.append([el[0], y + depth, el[1]])
        back_face.append(i + count)
        if i == count - 1:
            edges.append([i + count, count])
            faces.append([i, 0, count, i + count])
        else:
            edges.append([i + count, i + 1 + count])
            faces.append([i, i + 1, i + 1 + count, i + count])
    for i, el in enumerate(coords):
        edges.append([i, i + count])
        
    faces.append(front_face)    
    faces.append(back_face)

    new_mesh = bpy.data.meshes.new('new_mesh')
    new_mesh.from_pydata(vertices, edges, faces)
    new_mesh.update()
    return new_mesh


def generate_bevelled_mesh(coords, bevel_cords, y, depth):
    bevel = 0.1
    #print(coords)
    count = len(coords)
    vertices = []
    edges = []
    faces = []
    bevel_face = []
    back_face = []
    
    # Vertices 0.. are the front face
    for i, el in enumerate(coords):
        vertices.append([el[0], y, el[1]])
        if i == count - 1:
            edges.append([i, 0])
        else:
            edges.append([i, i + 1])

    
    # Vertices count.. are the back face
    for i, el in enumerate(coords):
        vertices.append([el[0], y - depth, el[1]])
        back_face.append(i + count)
        if i == count - 1:
            edges.append([i + count, count])
            faces.append([i, 0, count, i + count])
        else:
            edges.append([i + count, i + 1 + count])
            faces.append([i, i + 1, i + 1 + count, i + count])

    # Vertices 2xcount.. are the bevel face
    for i, el in enumerate(bevel_cords):
        vertices.append([el[0], y + bevel, el[1]])

        if i == count - 1:
            edges.append([i + 2 * count, 2 * count])
            faces.append([i, 0, 2 * count, i + 2 * count])
        else:
            edges.append([i + 2 * count, i + 1 + 2 * count])
            faces.append([i, i + 1, i + 1 + 2 * count, i + 2 * count])
        bevel_face.append(i + 2 * count)



    for i, el in enumerate(coords):
        edges.append([i, i + count])
        
    for i, el in enumerate(coords):
        edges.append([i, i + 2 * count])

    #print(vertices)

    faces.append(bevel_face)    
    faces.append(back_face)

    new_mesh = bpy.data.meshes.new('new_mesh')
    new_mesh.from_pydata(vertices, edges, faces)
    new_mesh.update()
    return new_mesh


def get_inset_coord(p1, p2, p3, inset):
    p4 = ((p2[0] + p3[0])/2, (p2[1] + p3[1])/2)   # point between the other two points
    p5 = (p4[0] - p1[0], p4[1] - p1[1])           # vector from p1 to p4
    distance = math.sqrt(p5[0] * p5[0] + p5[1] * p5[1])
    p6 = (p5[0] * inset / distance, p5[1] * inset / distance)   # vector from p1 to inset
    return p1[0] + p6[0], p1[1] + p6[1]
    
def get_recti_inset_coord(p1, p2, p3, inset):
    p4 = ((p2[0] + p3[0])/2, (p2[1] + p3[1])/2)   # point between the other two points
    p5 = (p4[0] - p1[0], p4[1] - p1[1])           # vector from p1 to p4
    return p1[0] + sign(p5[0]) * inset, p1[1] + sign(p5[1]) * inset
    
def get_angled_inset_coord(p1, p2, p3, inset, angle):
    p4 = ((p2[0] + p3[0])/2, (p2[1] + p3[1])/2)   # point between the other two points

    tries = []
    for i in range(0, 4):
        tries.append(get_point_in_direction(p1, angle + 45 + i * 90, inset))
    print(tries)
    return get_closest(p4, tries)


    
# angle in degrees, clockwise from north
def get_point_in_direction(p1, angle, distance):
    return (p1[0] + distance * math.cos(math.radians(angle)), p1[1] + distance * math.sin(math.radians(angle)))



def get_closest(p1, tries):
    closest = None
    distance = 0
    for el in tries:
        if closest == None:
            closest = el
            distance = get_distance(p1, el)
        elif get_distance(p1, el) < distance:
            closest = el
            distance = get_distance(p1, el)
    
    return closest



def get_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p1[1]) ** 2)



def sign(x):
    if x == 0:
        return 0
    return 1 if x > 0 else -1



# stone_arch(x_offset, y_offset, z_offset, radius, angle_of_arch, stone_depth, stone_height, stone_count, gap_angle = 0.1, bevel = True, keystone = 1.2):



#stone_arch(0, 0, 0, 34.4, 45, 3.8, 3.8, 14)
#stone_arch(0, 5, 0, 5.3, 45, 0.6, 0.6, 14, 0.2, keystone=1, pentagons=False, bevel=False)