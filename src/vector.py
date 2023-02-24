from math import sin, cos, acos, atan2, degrees
from panda3d.core import *


def get_polar_angles_from_vec(vector):
    x, y, z = vector
    r = vector.length()
    if r:
        theta = acos(z / r)
        phi = atan2(y, x)
        return degrees(phi), 0, degrees(theta)
    else:
        return 0, 0, 0


def get_position_from_polar_angles(r, theta, phi):
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return Point3(x, y, z)


if __name__ == '__main__':
    vec = Vec3(7.885625454519641, -3490.1795084662567, 3580.3048021979466)
    # print(get_polar_angles_from_vec(vec))