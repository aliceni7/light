import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    Iambient = calculate_ambient( ambient, areflect )
    Idiffuse = calculate_diffuse( light, dreflect, normal )
    Ispecular = calculate_specular( light, sreflect, view, normal )
    red = int(Iambient[0] + Idiffuse[0] + Ispecular[0])
    blue = int(Iambient[1] + Idiffuse[1] + Ispecular[1])
    green = int(Iambient[2] + Idiffuse[2] + Ispecular[2])
    return [red, green, blue]

def calculate_ambient(alight, areflect):
    Iambient = [ alight[0]*areflect[0], alight[1]*areflect[1], alight[2]*areflect[2] ]
    return limit_color(Iambient)

def calculate_diffuse(light, dreflect, normal):
    normalize( normal )
    normalize( light[LOCATION] )
    d = dot_product( normal, light[LOCATION] )
    Idiffuse = [ d*dreflect[0]*light[COLOR][0], d*dreflect[1]*light[COLOR][1], d*dreflect[2]*light[COLOR][2] ]
    return limit_color(Idiffuse)

def calculate_specular(light, sreflect, view, normal):
    normalize(normal)
    normalize(light[LOCATION])
    normalize(view)
    dt = dot_product(normal, light[LOCATION])
    t = [ normal[0]*dt, normal[1]*dt, normal[2]*dt ]
    r = [ 2*t[0] - light[LOCATION][0], 2*t[1] - light[LOCATION][1], 2*t[2] - light[LOCATION][2] ]
    normalize(r)
    cosa = dot_product( r, view )
    Ispecular = [ cosa*sreflect[0]*light[COLOR][0], cosa*sreflect[1]*light[COLOR][1], cosa*sreflect[1]*light[COLOR][1] ]
    return limit_color(Ispecular)

def limit_color(color):
    for i in range(3):
        color[i] = int(color[i])
        if color[i] > 255:
            color[i] = 255
        if color[i] < 0:
            color[i] = 0
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
