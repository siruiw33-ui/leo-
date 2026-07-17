"""
磁强计
z = B_body + noise
"""

import numpy as np

class Magnetometer:

    def __init__(
        self,
        bias = None,
        noise_std = 1e-9,
        dt = 1.0):

        if bias is None:
            bias = np.zeros(3)
        self.bias = np.array(bias,dtype=float)

        self.noise_std=noise_std

        self.dt = dt


    def measure(self,magnetic_field_body):

        noise = (np.random.randn(3) * self.noise_std)

        B_measure = (magnetic_field_body + self.bias + noise)

        return B_measure