"""
星传感器
q_m = q + bias + noise
"""

import numpy as np
from attitude.quaternion import normalize,multiply


class StarTracker:
    def __init__(
        self,
        attitude_bias=None,
        noise_std=1e-6,
        bias_random_walk=1e-8,
        dt=1.0):

        # 零偏
        if attitude_bias is None:
            attitude_bias = np.zeros(3)
        self.bias = np.array(attitude_bias,dtype=float)

        #白噪声标准差
        self.noise_std = noise_std

        # 零偏漂移系数
        self.bias_random_walk = bias_random_walk

        # 采样周期
        self.dt = dt


    # 更新偏置误差
    def update_bias(self):
        wb = (np.random.randn(3) * self.bias_random_walk)
        self.bias += (wb*np.sqrt(self.dt))


    def measure(self,q_true):
        # 更新偏置
        self.update_bias()
        # 小角度误差
        noise = (np.random.randn(3) * self.noise_std)
        # 总的三轴角度误差
        delta_theta = (self.bias + noise)

        #小角度误差转换得到的误差四元数
        dq = np.concatenate(([1.0], 0.5*delta_theta))
        dq = normalize(dq)

        # 最终输出的测量姿态四元数
        q_measure = multiply(dq, q_true)
        q_measure = normalize(q_measure )

        return q_measure