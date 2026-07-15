'''
计算刚体质心总体的力
'''

import numpy as np

from gravity import gravity_acceleration
from J2 import J2_acceleration
from drag import drag_acceleration
from SRP import srp_acceleration

def dynamics(t,state):
    r = state[0:3]
    v = state[3:6]

    a_gravity = gravity_acceleration(r)
    a_J2 = J2_acceleration(r)
    a_drag = drag_acceleration(r,v)
    a_srp = srp_acceleration(r)

    a = a_gravity + a_J2 + a_drag + a_srp
    
    return np.concatenate((v,a))