"""
柔性结构梁单元建模
"""

import numpy as np

class BeamElement:

    def __init__(
        self,
        E,
        I,
        rho,
        A,
        length ):

        #弹性模量
        self.E = E
        #截面惯性矩
        self.I = I
        #质量密度
        self.rho = rho
        #截面积
        self.A = A
        #注意此处长度为单位梁的长度
        self.length = length


    def stiffness_matrix(self):

        l = self.length

        EI = self.E * self.I

        #单位刚度矩阵
        Ke = (EI / l**3 *np.array([
                    [12,     6*l,  -12,    6*l],

                    [6*l, 4*l**2, -6*l, 2*l**2],

                    [-12,   -6*l,   12,   -6*l],

                    [6*l, 2*l**2, -6*l, 4*l**2]]))

        return Ke


    def mass_matrix(self):

        l = self.length

        coefficient = (self.rho *self.A *l /420)

        #质量矩阵
        Me = (coefficient * np.array([
                        [156 , 22*l    ,   54 , -13*l   ],

                        [22*l, 4*l**2  , 13*l , -3*l**2 ],

                        [54  , 13*l    , 156  , -22*l   ],

                        [-13*l, -3*l**2, -22*l, 4*l**2]]))

        return Me



    def damping_matrix(self,alpha,beta):

        Ke = self.stiffness_matrix()

        Me = self.mass_matrix()

        #阻尼矩阵
        Ce = (alpha * Me + beta * Ke)

        return Ce