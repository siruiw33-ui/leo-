"""
地球引力模型
"""

import numpy as np
from constants import MU

def gravity_acceleration(r):
    norm_r = np.linalg.norm(r)
    a = -MU * r / norm_r**3
    return a