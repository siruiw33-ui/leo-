"""
地磁扰动力矩
"""
import numpy as np


class ResidualMagneticModel:

    def __init__(
        self,
        initial_magnetic,
        lambda_r,
        Gamma,
        noise_std=0
    ):

        # 初始剩磁
        self.mr=np.array(initial_magnetic)

        # 退磁系数
        self.lambda_r=lambda_r

        # 磁化增益
        self.Gamma=Gamma

        # 噪声
        self.noise_std=noise_std


    def update(self,current,dt):

        noise = np.random.normal(0,self.noise_std,3)

        dmr = (-self.lambda_r*self.mr + self.Gamma*np.tanh(current) + noise)

        self.mr += dmr*dt

        return self.mr