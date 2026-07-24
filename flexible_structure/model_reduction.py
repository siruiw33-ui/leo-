"""
模态降阶
"""

import numpy as np


class ModalReduction:

    def __init__(
        self,
        M,
        C,
        K,
        Phi
    ):


        self.M=M
        self.C=C
        self.K=K
        self.Phi=Phi



    def reduce(self, modes):

        # 取低阶模态
        Phi_r = self.Phi[:,:modes]

        # 模态质量矩阵
        Mr = (Phi_r.T @ self.M @ Phi_r)

        # 模态阻尼矩阵
        Cr = (Phi_r.T @ self.C @ Phi_r)

        # 模态刚度矩阵
        Kr = (Phi_r.T @ self.K @ Phi_r)

        return (Mr, Cr, Kr, Phi_r)