"""
J2扰动模型
"""

import numpy as np
from constants import MU,RE,J2

def J2_acceleration(r):

    x,y,z = r

    r_norm = np.linalg.norm(r)
    r2 = r_norm**2
    r5 = r_norm**5
    z2 = z**2

    factor = -1.5 * J2 * MU * RE**2 / r5

    ax = factor * x * (1 - 5 * z2 / r2)
    ay = factor * y * (1 - 5 * z2 / r2)
    az = factor * z * (3 - 5 * z2 / r2)

    return np.array([ax, ay, az])
