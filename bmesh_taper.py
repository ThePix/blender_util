
import bpy
import bmesh

# The top of the item will be modified, the bottom will not


# Change this value to modify the degree of taper
# 10 is just noticeable, while 100 will bring it to a point
# Negative values will make it flare out
taper = 25

# You can just modify the X or Y coords if required
taperX = True
taperY = False





# Get the active mesh
me = bpy.context.object.data


# Get a BMesh representation
bm = bmesh.new()   # create an empty BMesh
bm.from_mesh(me)   # fill it in from a Mesh


# First get the limits

xMax = None
xMin = None
yMax = None
yMin = None
zMax = None
zMin = None


for v in bm.verts:
    if xMax == None or v.co.x > xMax:
        xMax = v.co.x
    if xMin == None or v.co.x < xMin:
        xMin = v.co.x
    if yMax == None or v.co.y > yMax:
        yMax = v.co.y
    if yMin == None or v.co.y < yMin:
        yMin = v.co.y
    if zMax == None or v.co.z > zMax:
        zMax = v.co.z
    if zMin == None or v.co.z < zMin:
        zMin = v.co.z

xCentre = (xMax + xMin) / 2
yCentre = (yMax + yMin) / 2

# Now taper along z axis


# The base will be the same, the top each point will move "taper" percent towards the centre line in both x and y axes


for v in bm.verts:
    relativeHeight = (v.co.z - zMin) / (zMax - zMin)  # How far UP the thing we up, from zero at the bottom to one at the top
    adjustment = taper / 100 * relativeHeight # How far, as a proportion from zero to one, we need to move each point towards the centre

    if taperX:
        v.co.x = v.co.x + (xCentre - v.co.x) * adjustment
        
    if taperY:
        v.co.y = v.co.y + (yCentre - v.co.y) * adjustment







# Finish up, write the bmesh back to the mesh
bm.to_mesh(me)
bm.free()  # free and prevent further access
